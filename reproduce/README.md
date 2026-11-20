# Reproduce

```bash
python reproduce/run_all.py           # every figure in the article, a few seconds
python reproduce/run_all.py --quick   # smaller sample sizes for the two sampling checks
```

Python 3.12 or later, standard library only. `run_all.py` rebuilds the test set of Section 6, recomputes every
figure in the article, compares each with the text, writes [`results.md`](results.md) and exits with status 1 if
any figure disagrees. The same command runs on every push.

| Script | Article | What it computes |
| --- | --- | --- |
| [`certificates.py`](certificates.py) | §3, §6 | 600 task families in exact rational arithmetic (`fractions.Fraction`): $`H = M^\top M + I`$, so that $`\mu = 1`$ is a verified curvature bound, an integer $`A`$ of full row rank, and $`b = Ax_0`$ for feasibility. Six submissions per family, three acceptance protocols, and the projected-residual bound at one feasible perturbation per family |
| [`scoring.py`](scoring.py) | §1, §4, §5, §7 | The ranking reversal; tolerance propagation on 20,000 random problems and a two-point example that attains the bound; the shift of the process-reward target in both regimes; the variance cost of noise correction; the effective sample size; the break-even volume |
| [`acceptance_thresholds.py`](acceptance_thresholds.py) | §1, §2, §4, §5 | The certified-lead condition and its tightness; the escalation rate and the clean-run sample sizes; the composition law for chains of transformations; the path of a policy reweighted by its grader, its limit and the share of a rejected route |

## How the test set is built

| Class | Submission | Reports $`v^*`$ |
| --- | --- | :---: |
| Lagrange (valid) | The KKT solution $`(x^*, \nu^*)`$ from the full system | ✓ |
| Elimination (valid) | A particular solution of $`Ax = b`$, then the reduced system $`Z^\top HZ\,y = -Z^\top(Hx_p + c)`$. It never touches the KKT solution, and the script asserts that it reaches the same $`x^*`$ | ✓ |
| Infeasible | $`x^* + k\,a_1`$ for a row $`a_1`$ of $`A`$, so $`Ax \ne b`$ | ✓ |
| Not stationary | $`x^* + k\,z_1`$ for a basis vector $`z_1`$ of $`\ker\,A`$: feasible and off the optimum | ✓ |
| Multiplier fails | $`x^*`$ with $`\nu^* + k e_1`$: the right point with a multiplier that fails stationarity | ✓ |
| Wrong value | $`(x^*, \nu^*)`$ with value $`v^* + k`$ | |

Here $`k \in \{1, 2, 3\}`$ is drawn per family. The three defect classes that report the correct final answer are
the 1,800 invalid submissions, 75% of all invalid submissions, that final-answer matching accepts. The arithmetic
is exact and the construction is determined by the seed, so the table of Section 6 is reproduced exactly.

## The three acceptance protocols

- **Final-answer matching** accepts when the reported value equals $`v^*`$.
- **Strict reference-path matching** accepts when the submission reproduces the reference Lagrange route.
- **Certificate verification** checks feasibility, the verified curvature on $`\ker\,A`$, a zero projected residual,
  the claimed value against $`f(x)`$, and the full stationarity equation for any claimed multiplier.
