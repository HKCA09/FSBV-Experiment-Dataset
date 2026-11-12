#!/usr/bin/env python3
r"""Full-posterior Bayesian logistic mixed model for RQ3 task correctness.

Data: 40 reviews, each with four binary correctness scores.
Model: task, condition, period, sequence fixed effects;
       participant, case, review-record random intercepts.
Inference: four-block elliptical-slice sampler for standard-normal latent
           coefficients/random effects + adaptive log-scale random-walk MH for
           random-effect SDs. After warmup, adaptation stops.
All MCMC draws are genuine posterior samples, not VB or Laplace samples.
Dependencies: numpy scipy numba (artifact_tool optional for XLSX input).

Usage:
    python -u RQ3_Total_Accuracy_FullPosterior.py RQ3_Total_Accuracy_Input.csv \
        --chains 4 --warmup 3500 --draws 7000 --fixed-sd 1.5 \
        --sd-prior 1.0 --seed 20261108
"""
import argparse, json, time, os, csv
from pathlib import Path
import numpy as np
from numba import njit
from scipy.special import expit, logsumexp
from scipy.stats import norm, rankdata
from numpy.polynomial.hermite import hermgauss
# XLSX input requires artifact_tool; supplied CSV input works with Python's standard library.

TASK_FIELDS = [
    'task1_scenario_identification_correct',
    'task2_violated_behavior_identification_correct',
    'task3_implementation_context_identification_correct',
    'task4_followup_verification_planning_correct',
]

@njit(cache=True)
def loglike(z, sigmas, prior_sd, conditions, periods, sequences, pi, ci, ri, yi, ki):
    b0=2*z[0]
    bcond=prior_sd*z[1]
    bperiod=prior_sd*z[2]
    bseq=prior_sd*z[3]
    bp2=prior_sd*z[4]
    bp3=prior_sd*z[5]
    bp4=prior_sd*z[6]
    out=0.
    for q in range(len(yi)):
        task=ki[q]
        fx=b0 + bcond*conditions[q] + bperiod*periods[q] + bseq*sequences[q]
        if task==1: fx+=bp2
        if task==2: fx+=bp3
        if task==3: fx+=bp4
        eta=fx + sigmas[0]*z[7+pi[q]] + sigmas[1]*z[27+ci[q]] + sigmas[2]*z[47+ri[q]]
        if eta>0:
            out+=yi[q]*eta - (eta + np.log1p(np.exp(-eta)))
        else:
            out+=yi[q]*eta - np.log1p(np.exp(eta))
    return out

def read_input(path, omit_task2=False):
    if str(path).lower().endswith('.csv'):
        with open(path,newline='',encoding='utf-8-sig') as f:
            rec=[r for r in csv.DictReader(f) if int(r['valid_record'])==1]
        number_keys=TASK_FIELDS + ['total_accuracy','review_case_order']
        for r in rec:
            for k in number_keys:r[k]=int(r[k])
    else:
        from artifact_tool import Blob, SpreadsheetFile
        wb=SpreadsheetFile.import_xlsx(Blob.load(str(path)))
        raw=wb.worksheets.get_item('Experiment_Data').get_range('A1:S41').values
        rec=[dict(zip(raw[0],rr)) for rr in raw[1:] if rr[17]==1]
    assert len(rec)==40
    participants=sorted(set(r['participant_id'] for r in rec))
    cases=sorted(set(r['case_id'] for r in rec))
    assert len(participants)==20 and len(cases)==20
    cond,period,sequence,pi,ci,ri,yi,ki=[],[],[],[],[],[],[],[]
    for j,r in enumerate(rec):
        assert sum(r[k] for k in TASK_FIELDS)==r['total_accuracy']
        for t,k in enumerate(TASK_FIELDS):
            cond.append(int(r['condition']=='Traceability-assisted'))
            period.append(int(r['review_case_order']==2))
            sequence.append(int(r['order_group']=='Traceability-first'))
            pi.append(participants.index(r['participant_id']))
            ci.append(cases.index(r['case_id']))
            ri.append(j)
            yi.append(int(r[k]));ki.append(t)
    arrs=[np.array(x,dtype=np.int64) for x in (cond,period,sequence,pi,ci,ri,yi,ki)]
    assert len(yi)==160 and sum(yi)==sum(r['total_accuracy'] for r in rec)
    if omit_task2:
        keep=arrs[7] != 1
        arrs=[arr[keep] for arr in arrs]
        assert len(arrs[7])==120
    return rec, arrs

def logprior_logsigma(eta, halfnormal_scale):
    sigma=np.exp(eta)
    return float(np.sum(eta - .5*(sigma/halfnormal_scale)**2))

def elliptical_block(z,start,end,sigmas,prior_sd,arrs,rng,oldll):
    v=rng.standard_normal(end-start)
    logy=oldll+np.log(rng.uniform())
    theta=rng.uniform(0,2*np.pi)
    tmin=theta-2*np.pi; tmax=theta
    old=z[start:end].copy()
    attempts=0
    while True:
        z[start:end]=old*np.cos(theta)+v*np.sin(theta)
        proposal=loglike(z,sigmas,prior_sd,*arrs)
        attempts+=1
        if proposal>logy:
            return proposal,attempts
        if theta<0:tmin=theta
        else:tmax=theta
        theta=rng.uniform(tmin,tmax)
        if attempts>30000:raise RuntimeError('Elliptical slice trapped; check finite log likelihood')

def one_chain(chain_id,arrs,prior_sd,halfnormal_scale,warmup,draws,seed,thin=1):
    rng=np.random.default_rng(seed)
    z=rng.normal(size=87)*0.15
    # Init at fixed odds from marginal data; z=0 implies baseline task1 p=.5.
    eta=np.log(np.array([0.6,0.6,0.6]))
    sigmas=np.exp(eta)
    ll=loglike(z,sigmas,prior_sd,*arrs)
    logpost=ll+logprior_logsigma(eta,halfnormal_scale)
    rw=np.array([0.25,0.25,0.25])
    accepted_window=np.zeros(3)
    attempted_window=np.zeros(3)
    block_attempts=np.zeros(4)
    total=warmup+draws*thin
    saved=np.empty((draws,10),dtype=float)
    k=0
    for iteration in range(total):
        for t,(a,b) in enumerate([(0,7),(7,27),(27,47),(47,87)]):
            ll,n=elliptical_block(z,a,b,sigmas,prior_sd,arrs,rng,ll)
            block_attempts[t]+=n
        for d in range(3):
            prop=eta.copy();prop[d]+=rng.normal(scale=rw[d])
            sig2=np.exp(prop)
            ll2=loglike(z,sig2,prior_sd,*arrs)
            lp2=ll2+logprior_logsigma(prop,halfnormal_scale)
            attempted_window[d]+=1
            if np.log(rng.uniform())<(lp2-(ll+logprior_logsigma(eta,halfnormal_scale))):
                eta=prop;sigmas=sig2;ll=ll2;accepted_window[d]+=1
        if iteration<warmup and (iteration+1)%100==0:
            acc=accepted_window/np.maximum(attempted_window,1)
            rw=np.clip(rw*np.exp(0.40*(acc-0.30)),.03,1.2)
            accepted_window[:]=0;attempted_window[:]=0
        if iteration>=warmup and (iteration-warmup)%thin==0:
            saved[k,:7]=z[:7]*np.array([2]+[prior_sd]*6)
            saved[k,7:]=sigmas
            k+=1
    assert k==draws
    return saved,{'chain':chain_id,'mean_EES_likelihood_evaluations_per_block':(block_attempts/total).tolist(),'proposal_scales_at_warmup_end':rw.tolist()}

def autocov_fft(x):
    n=len(x)
    y=x-x.mean()
    f=np.fft.rfft(y,n=2*n)
    ac=np.fft.irfft(f*np.conjugate(f),n=2*n)[:n]
    return ac/(n-np.arange(n))

def split_rhat(x):
    # rank-normalized split Rhat and folded rank normalized split Rhat
    chains,n=x.shape
    if n%2: x=x[:,:n-1]; n-=1
    y=np.concatenate([x[:,:n//2],x[:,n//2:]],axis=0)
    def _rhat(v):
        m,n=v.shape
        b=n*np.var(v.mean(axis=1),ddof=1)
        w=np.mean(np.var(v,axis=1,ddof=1))
        return float(np.sqrt(((n-1)*w/n+b/n)/w))
    ranks=rankdata(y.reshape(-1)).reshape(y.shape)
    normalized=norm.ppf((ranks-0.375)/(ranks.size+0.25))
    folded=np.abs(y-np.median(y))
    ranks_fold=rankdata(folded.reshape(-1)).reshape(y.shape)
    normalized_fold=norm.ppf((ranks_fold-0.375)/(ranks_fold.size+0.25))
    return max(_rhat(normalized),_rhat(normalized_fold))

def bulk_ess(x):
    # Split-chain autocorrelation, initial positive sequence and paired-lag truncation
    m,n=x.shape
    acov=np.stack([autocov_fft(v) for v in x])
    W=np.mean(acov[:,0])
    B=n*np.var(x.mean(axis=1),ddof=1)
    varplus=(n-1)*W/n+B/n
    rho=np.ones(n)
    for lag in range(1,n):rho[lag]=1-(W-np.mean(acov[:,lag]))/varplus
    sums=[]
    for lag in range(0,n-1,2):
        pair=rho[lag]+rho[lag+1]
        if pair<0: break
        sums.append(pair)
    tau=max(-1+2*np.sum(sums),1)
    return float(m*n/tau)

def diagnose(draws):
    names=['Intercept','Condition','Period','Sequence','Task2','Task3','Task4','SD_Participant','SD_Case','SD_Review']
    out=[]
    for j,name in enumerate(names):
        m=draws[:,:,j]
        flat=m.reshape(-1)
        ranks=rankdata(m.reshape(-1)).reshape(m.shape)
        rank_normal=norm.ppf((ranks-0.375)/(ranks.size+0.25))
        bulk=bulk_ess(rank_normal)
        qlo,qhi=np.quantile(flat,[.05,.95])
        tail=min(bulk_ess((m<qlo).astype(float)),bulk_ess((m>qhi).astype(float)))
        out.append({'parameter':name,'posterior_mean':float(flat.mean()),'posterior_median':float(np.median(flat)),
                    '95% CrI lower':float(np.quantile(flat,.025)), '95% CrI upper':float(np.quantile(flat,.975)),
                    'rank-split-Rhat':split_rhat(m),'bulk_ESS':bulk,'tail_ESS':tail})
    return out

def adjusted_score_draws(draws, omit_task2=False):
    flat=draws.reshape(-1,10)
    b0=flat[:,0];bc=flat[:,1];bp=flat[:,2];bs=flat[:,3]
    task=np.column_stack([np.zeros(len(flat)),flat[:,4:7]])
    if omit_task2:
        task=task[:,[0,2,3]]
    sig=np.sqrt(np.sum(flat[:,7:10]**2,axis=1))
    x,w=hermgauss(13)
    preds=[]
    for c in (0,1):
        cells=[(0,0),(1,1)] if c==0 else [(1,0),(0,1)]
        pp=[]
        for per,seq in cells:
            yy=b0[:,None] + bc[:,None]*c+bp[:,None]*per+bs[:,None]*seq+task
            marginal=np.zeros_like(yy)
            for xx,ww in zip(x,w):
                marginal+=ww*expit(yy+np.sqrt(2)*sig[:,None]*xx)/np.sqrt(np.pi)
            pp.append(np.sum(marginal,axis=1))
        preds.append(np.mean(pp,axis=0))
    return preds[0],preds[1],preds[1]-preds[0]

def run_inference(inp,outdir,draws,warmup,chains,fixed_sd,halfnormal_sd,seed,thin,omit_task2=False):
    output=Path(outdir);output.mkdir(parents=True,exist_ok=True)
    records,arrs=read_input(inp,omit_task2=omit_task2)
    tic=time.perf_counter()
    # initialize JIT before running chains
    loglike(np.zeros(87),np.ones(3),fixed_sd,*arrs)
    all_draws=[];chain_info=[]
    for c in range(chains):
        vals,diag=one_chain(c+1,arrs,fixed_sd,halfnormal_sd,warmup,draws,seed+10009*c,thin)
        all_draws.append(vals);chain_info.append(diag)
        print(f'Chain {c+1}/{chains} finished; elapsed={time.perf_counter()-tic:.1f}s',flush=True)
    samples=np.stack(all_draws)
    diagnostics=diagnose(samples)
    baseline,assisted,difference=adjusted_score_draws(samples,omit_task2=omit_task2)
    report={
      'model':'Task-level Bayesian logistic GLMM; participant, case, review random intercept',
      'input':str(inp),'fixed_effect_prior_sd':fixed_sd,
      'intercept_prior_sd':2.,'random_effect_sd_halfnormal_prior_scale':halfnormal_sd,
      'warmup_iterations_per_chain':warmup,'posterior_draws_per_chain':draws,
      'chains':chains,'thin':thin,'random_seed':seed,
      'elapsed_seconds':time.perf_counter()-tic,
      'data':{'n_reviews':len(records),'n_task_observations':len(arrs[6]),'omit_task2_all_correct':omit_task2,
              'correct_baseline':sum(r['total_accuracy'] for r in records if r['condition']=='Baseline'),
              'correct_assisted':sum(r['total_accuracy'] for r in records if r['condition']=='Traceability-assisted')},
      'posterior_adjusted_score':{
           'baseline_median':float(np.median(baseline)),'assisted_median':float(np.median(assisted)),
           'difference_median':float(np.median(difference)),
           'difference_mean':float(np.mean(difference)),
           'difference_95CrI':[float(a) for a in np.quantile(difference,[.025,.975])],
           'Pr_difference_positive':float((difference>0).mean())},
      'conditional_log_odds':{
           'coefficient_median':float(np.median(samples[:,:,1])),
           'coefficient_95CrI':[float(v) for v in np.quantile(samples[:,:,1],[.025,.975])],
           'OR_median':float(np.median(np.exp(samples[:,:,1]))),
           'OR_95CrI':[float(v) for v in np.quantile(np.exp(samples[:,:,1]),[.025,.975])]
        },
      'diagnostics':diagnostics,
      'chain_info':chain_info,
      'limitations': 'Normal random-intercept and conditional-independent Bernoulli assumptions; three random-effect SDs weakly identifiable at n=40 reviews; task2 had no errors; posterior intervals dependent on regularizing priors.'
    }
    name=f'bayes_glmm_prior{fixed_sd:.1f}_sigma{halfnormal_sd:.1f}' + ('_omitTask2' if omit_task2 else '')
    with open(output / f'{name}.json','w') as f:
        json.dump(report,f,indent=2,ensure_ascii=False)
    np.savez_compressed(output / f'{name}_draws.npz',
                        draws=samples,baseline_score=baseline,assisted_score=assisted,score_difference=difference)
    print('RESULT',json.dumps({'adjusted_score':report['posterior_adjusted_score'],
       'condition':report['conditional_log_odds'],
       'max_rhat':max(x['rank-split-Rhat'] for x in diagnostics),
       'min_bulk_ESS':min(x['bulk_ESS'] for x in diagnostics),
       'min_tail_ESS':min(x['tail_ESS'] for x in diagnostics)},ensure_ascii=False),flush=True)
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('input',nargs='?',default='/mnt/data/RQ3_experiment_analysis(2).xlsx')
    p.add_argument('--outdir',default='/mnt/data/rq3_accuracy_full_posterior')
    p.add_argument('--chains',type=int,default=4)
    p.add_argument('--warmup',type=int,default=3500)
    p.add_argument('--draws',type=int,default=7000)
    p.add_argument('--thin',type=int,default=1)
    p.add_argument('--fixed-sd',type=float,default=1.5)
    p.add_argument('--sd-prior',type=float,default=1.0)
    p.add_argument('--seed',type=int,default=20261108)
    p.add_argument('--omit-task2',action='store_true')
    args=p.parse_args()
    run_inference(args.input,args.outdir,args.draws,args.warmup,args.chains,args.fixed_sd,args.sd_prior,args.seed,args.thin,omit_task2=args.omit_task2)
