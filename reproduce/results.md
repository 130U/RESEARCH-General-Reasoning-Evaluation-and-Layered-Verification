# Results

Every figure in the article, recomputed.

68 of 68 figures agree with the article

## Scores, rankings and certified leads (Section 1)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Model A, true validity 72%, false acceptance 4%: observed score (%) | 73.1200 | 73.12 | §1 | ✓ |
| Model B, true validity 64%, false acceptance 36%: observed score (%) | 76.9600 | 76.96 | §1 | ✓ |
| The model with the lower true validity ranks first |  | holds | §1 | ✓ |
| False acceptance for Model B above which the pair reverses (%) | 25.3333 | 25.3 | §1 | ✓ |
| Lead of 3 points over a rival at 80%: certified below a false acceptance of (%) | 15.0000 | 15 | §1 | ✓ |
| Lead of 3 points over a rival at 50%: certified below (%) | 6.0000 | 6 | §1 | ✓ |
| Certified-lead condition is tight on 200,000 random cases |  | holds | §1, D2 | ✓ |

## When a screen may decide (Section 2)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Sensitivity 52.87%, target 5%: share of unflagged work escalated (%) | 89.3910 | 89 | §2 | ✓ |
| Sensitivity 0.80: share escalated (%) | 75.0000 | 75 | §2 | ✓ |
| Sensitivity 0.90: share escalated (%) | 50.0000 | 50 | §2 | ✓ |
| Sensitivity 0.95: share escalated (%) | 0.0000 | 0 | §2 | ✓ |
| Clean run that bounds false acceptance at 5% with 95% confidence | 59 | 59 | §2 | ✓ |
| Clean run that bounds false acceptance at 1% | 299 | 299 | §2 | ✓ |

## Task transformations (Section 4)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Tolerance rule aδ + 2ε holds on 20,000 random problems |  | holds | §4 | ✓ |
| The rule is attained by a two-point example | 1.2000 | equal | D7 | ✓ |
| Discretization last: scaling a | 50.0000 | 50 | §4 | ✓ |
| Discretization last: error ε | 0.0030 | 0.003 | §4 | ✓ |
| Discretization last: tolerance owed | 0.5060 | 0.506 | §4 | ✓ |
| Discretization first: scaling a | 50.0000 | 50 | §4 | ✓ |
| Discretization first: error ε | 0.1500 | 0.15 | §4 | ✓ |
| Discretization first: tolerance owed | 0.8000 | 0.8 | §4 | ✓ |
| Composition law equals step-by-step application on 20,000 random chains |  | holds | §4, D7 | ✓ |

## What a grader does to training (Section 5)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Gradient shift p − p̃ by direct sampling, false rejection dominates (p = 0.8, α = 0.05, β = 0.2) | 0.1501 | 0.1500 | §5 | ✓ |
| Gradient shift p − p̃ by direct sampling, false acceptance dominates (p = 0.3, α = 0.3, β = 0.05) | -0.1952 | -0.1950 | §5 | ✓ |
| Noise-corrected estimate, mean over repeated samples (θ = 0.6) | 0.6002 | 0.6 | §5 | ✓ |
| Variance inflation against 1/(1 − α − β)² | 1.7900 | 1.7778 | §5 | ✓ |
| Model B at optimization strength 0: true validity (%) | 64.0000 | 64 | §5 table | ✓ |
| Model B at optimization strength 0: observed score (%) | 76.9600 | 77 | §5 table | ✓ |
| Model B at optimization strength 1: true validity (%) | 74.9099 | 74.9 | §5 table | ✓ |
| Model B at optimization strength 1: observed score (%) | 90.0792 | 90.1 | §5 table | ✓ |
| Model B at optimization strength 2: true validity (%) | 79.9220 | 79.9 | §5 table | ✓ |
| Model B at optimization strength 2: observed score (%) | 96.1061 | 96.1 | §5 table | ✓ |
| Model B at optimization strength 4: true validity (%) | 82.7066 | 82.7 | §5 table | ✓ |
| Model B at optimization strength 4: observed score (%) | 99.4547 | 99.5 | §5 table | ✓ |
| Model B: limit of true validity, the grader's positive predictive value (%) | 83.1601 | 83.2 | §5 | ✓ |
| Model A: limit of true validity (%) | 98.4683 | 98.5 | §5 | ✓ |
| The limit of the reweighted policy equals the positive predictive value |  | holds | §5, D9 | ✓ |
| Share of valid work on a route the grader rejects, strength 1 (%) | 26.8941 | 26.9 | §5 | ✓ |
| Share of valid work on a route the grader rejects, strength 2 (%) | 11.9203 | 11.9 | §5 | ✓ |
| Share of valid work on a route the grader rejects, strength 4 (%) | 1.7986 | 1.8 | §5 | ✓ |

## A test set with exactly known verdicts (Sections 3 and 6)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Task families | 600 | 600 | §6 | ✓ |
| Submissions | 3,600 | 3,600 | §6 | ✓ |
| Valid certificates | 1,200 | 1,200 | §6 | ✓ |
| Submissions with a controlled defect | 2,400 | 2,400 | §6 | ✓ |
| Invalid submissions that report the correct optimal value | 1,800 | 1,800 | §6 | ✓ |
| Their share of all invalid submissions (%) | 75.0000 | 75 | §6 | ✓ |
| Final-answer matching: false acceptance (%) | 75.0000 | 75 | §6 table | ✓ |
| Final-answer matching: false rejection (%) | 0.0000 | 0 | §6 table | ✓ |
| Final-answer matching: valid share of accepted submissions (%) | 40.0000 | 40 | §6 table | ✓ |
| Strict reference-path matching: false acceptance (%) | 0.0000 | 0 | §6 table | ✓ |
| Strict reference-path matching: false rejection (%) | 50.0000 | 50 | §6 table | ✓ |
| Strict reference-path matching: valid share of accepted submissions (%) | 100.0000 | 100 | §6 table | ✓ |
| Certificate verification: false acceptance (%) | 0.0000 | 0 | §6 table | ✓ |
| Certificate verification: false rejection (%) | 0.0000 | 0 | §6 table | ✓ |
| Certificate verification: valid share of accepted submissions (%) | 100.0000 | 100 | §6 table | ✓ |
| Final-answer matching: flawed solutions accepted | 1,800 | 1,800 | §6 table | ✓ |
| Reference-path matching: valid elimination proofs rejected | 600 | 600 | §6 table | ✓ |
| Certificate verification: invalid proofs accepted, fewer than final-answer matching by | 1,800 | 1,800 | §6 | ✓ |
| Certificate verification: valid alternative solutions kept, more than reference-path matching by | 600 | 600 | §6 | ✓ |
| Certificate verification: submissions with a multiplier that fails stationarity accepted | 0 | 0 | §6 | ✓ |
| Projected-residual bound holds at feasible perturbations (families) | 600 | 600 | §3, §6 | ✓ |
| Valid share of the test set before training (%) | 33.3333 | one third | §6 | ✓ |
| Positive predictive value of final-answer matching on the test set (%) | 40.0000 | 40 | Summary, §6 | ✓ |
| Positive predictive value of certificate checking on the test set (%) | 100.0000 | 100 | Summary, §6 | ✓ |

## Task families and the economics of certificates (Section 7)

| Quantity | Recomputed | Article | Where | Agrees |
| --- | ---: | ---: | --- | :---: |
| Effective sample size of 50 families of 8 variants at ρ_w = 0.6 | 77 | 77 | §7 | ✓ |
| Break-even volume (submissions) | 481.9277 | 482 | §7 | ✓ |
| Share of an expert review released per further submission (%) | 83.0000 | 83 | §7 | ✓ |
| Break-even volume separates the cheaper workflow from the dearer on 10,000 random cost settings |  | holds | §7 | ✓ |

## Accepted submissions by class

600 submissions in each class.

| Protocol | Lagrange (valid) | Elimination (valid) | Infeasible | Not stationary | Multiplier fails | Wrong value |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Final-answer matching | 600 | 600 | 600 | 600 | 600 | 0 |
| Strict reference-path matching | 600 | 0 | 0 | 0 | 0 | 0 |
| Certificate verification | 600 | 600 | 0 | 0 | 0 | 0 |
