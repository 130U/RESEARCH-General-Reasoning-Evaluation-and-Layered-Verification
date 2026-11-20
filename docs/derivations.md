# Derivations

Full proofs of the article's results, in its notation and with its equation numbers. Section numbers (§) refer to
the [article](../manuscript/general-reasoning-evaluation-and-layered-verification.md); every figure quoted
here is recomputed in [results](../reproduce/results.md).

| | Result | Section |
| --- | --- | --- |
| [D1](#d1-grading-error-moves-scores-and-can-reverse-rankings) | Grading error moves scores and can reverse rankings | §1, eq. 1.1 |
| [D2](#d2-when-a-lead-is-certified) | When a lead is certified | §1, eq. 1.2 |
| [D3](#d3-proof-obligations-soundness-and-failure-propagation) | Proof obligations: soundness and failure propagation | §2, eq. 2.1 |
| [D4](#d4-when-a-screen-may-decide) | When a screen may decide | §2, eq. 2.2 |
| [D5](#d5-the-projected-residual-certificate) | The projected-residual certificate | §3, eqs. 3.1 to 3.4 |
| [D6](#d6-the-certificate-template-for-other-task-types) | The certificate template for other task types | §3 |
| [D7](#d7-transformations-propagate-tolerances) | Transformations propagate tolerances | §4, eqs. 4.1 to 4.4 |
| [D8](#d8-grading-error-shifts-the-process-reward-target) | Grading error shifts the process-reward target | §5, eqs. 5.1 to 5.4 |
| [D9](#d9-what-a-policy-learns-from-a-grader) | What a policy learns from a grader | §5, eq. 5.5 |
| [D10](#d10-variants-of-one-template-are-not-independent-evidence) | Variants of one template are not independent evidence | §7, eq. 7.1 |
| [D11](#d11-when-certificates-pay-for-themselves) | When certificates pay for themselves | §7, eq. 7.2 |

---

## D1. Grading error moves scores and can reverse rankings

For model $`m`$, let $`Z = 1`$ mark a fully valid solution and $`V = 1`$ acceptance. By total probability,

```math
s_m = P(V=1\mid Z=0)P(Z=0) + P(V=1\mid Z=1)P(Z=1) = \alpha_m(1-\theta_m) + (1-\beta_m)\theta_m , \qquad (D1.1)
```

which rearranges to $`s_m = \alpha_m + (1-\alpha_m-\beta_m)\theta_m`$ and
$`s_m - \theta_m = \alpha_m(1-\theta_m) - \beta_m\theta_m`$. ∎ More items shrink the variance of $`\hat s_m`$ and
leave $`s_m - \theta_m`$ unchanged.

**Reversal.** With $`\theta_A > \theta_B`$ and $`\beta = 0`$, the observed order flips when
$`\alpha_B(1-\theta_B) - \alpha_A(1-\theta_A) > \theta_A - \theta_B`$: the extra credit given to B's invalid work
exceeds the true gap. For $`\theta_A = 72\%`$, $`\alpha_A = 4\%`$ and $`\theta_B = 64\%`$ the threshold is
$`\alpha_B > [\theta_A - \theta_B + \alpha_A(1-\theta_A)]/(1-\theta_B) = 25.3\%`$. At $`\alpha_B = 36\%`$ the scores are 73.12% and 76.96%.

## D2. When a lead is certified

**Interval.** From $`s = \alpha + (1-\alpha-\beta)\theta`$, $`\theta = (s-\alpha)/(1-\alpha-\beta)`$. Its derivative in
$`\alpha`$ has the sign of $`s - (1-\beta)`$, which is nonpositive because $`s \le 1-\beta`$, and its derivative in
$`\beta`$ is nonnegative. Over $`0 \le \alpha \le \bar\alpha`$ and $`0 \le \beta \le \bar\beta`$ the smallest
admissible $`\theta`$ is at $`(\bar\alpha, 0)`$ and the largest at $`(0, \bar\beta)`$:

```math
\frac{s - \bar\alpha}{1 - \bar\alpha} \le \theta \le \frac{s}{1 - \bar\beta} . \qquad (D2.1)
```

**Certified order.** With $`\bar\beta = 0`$ the order $`\theta_A > \theta_B`$ holds for every admissible pair of
graders exactly when the lower end for A exceeds the upper end for B:

```math
\frac{s_A - \bar\alpha}{1 - \bar\alpha} > s_B \iff s_A - s_B > \bar\alpha(1 - s_B) \iff \bar\alpha < \frac{g}{1 - s_B} . \quad ∎ \qquad (D2.2)
```

**Tightness.** If $`\bar\alpha \ge g/(1-s_B)`$, take $`\alpha_A = \bar\alpha`$ and $`\alpha_B = 0`$. Both are
admissible, and they give $`\theta_A = (s_A - \bar\alpha)/(1-\bar\alpha) \le s_B = \theta_B`$. For a lead of three
points the bound is 15% over a rival at 80% and 6% over a rival at 50%. The code confirms the condition on 200,000
random cases.

## D3. Proof obligations: soundness and failure propagation

**Claim.** Let $`G`$ be a DAG of claims $`v_j`$. Suppose (i) every node satisfies
$`\Gamma_q \cup \{v_k : k \in \mathrm{pa}(j)\} \vdash v_j`$ in a sound inference system, (ii) the sinks
together with $`\Gamma_q`$ derive $`C_q`$, and (iii) $`𝒯_{\text{comp}}(\tau) = 1`$. Then $`C_q`$ follows
from $`\Gamma_q`$ by a compliant execution.

**Proof.** Order the nodes topologically. Roots have no parents, so (i) gives $`\Gamma_q \vdash v_j`$. If every node
before $`v_j`$ is derivable from $`\Gamma_q`$, then so are its parents, and (i) with transitivity of $`\vdash`$
gives $`\Gamma_q \vdash v_j`$. By induction every node is derivable, and (ii) gives $`\Gamma_q \vdash C_q`$.
Condition (iii) is checked independently of the logical graph. ∎

**Failure propagation.** If the local check fails at $`v_j`$, the induction cannot pass through $`v_j`$. Every node
in $`\mathrm{desc}(v_j)`$ loses its derivation in this submission even if its own local step is valid. Those
nodes are marked unverified, and not false: a claim downstream of a false premise may still be true, but the
submission has not shown it.

**Route independence.** Nothing in (i) to (iii) refers to the reference solution. Any graph whose nodes discharge
the task's obligations passes, which is why a valid elimination proof and a valid Lagrange proof pass on the same
terms.

## D4. When a screen may decide

An invalid step is flagged with probability $`\text{se}`$ and then reaches a specialist. If it is not flagged it
reaches a specialist with probability $`\rho`$. With the specialist's verdict as the reference, the step is
accepted only when it is neither flagged nor escalated:

```math
\alpha_{\text{sys}} = (1-\text{se})(1-\rho) \le \alpha^* \iff \rho \ge 1 - \frac{\alpha^*}{1-\text{se}} . \quad ∎ \qquad (D4.1)
```

When $`\text{se} \ge 1 - \alpha^*`$ the right side is nonpositive and no escalation is needed. At
$`\alpha^* = 5\%`$ the required share is 89% at a sensitivity of 52.87%, 75% at 0.80, 50% at 0.90 and zero at 0.95.

**Clean run.** If a checker's false acceptance is $`\alpha`$, it rejects $`n`$ known-invalid items in a row with
probability $`(1-\alpha)^n`$. A clean run of $`n`$ therefore rejects every $`\alpha`$ with
$`(1-\alpha)^n < 0.05`$, and the one-sided 95% bound is $`\alpha \le 1 - 0.05^{1/n}`$. The smallest $`n`$ with
$`(1-\alpha_0)^n \le 0.05`$ is $`\lceil \ln\,0.05/\ln(1-\alpha_0) \rceil`$: 59 for $`\alpha_0 = 5\%`$ and 299 for
$`\alpha_0 = 1\%`$. ∎

## D5. The projected-residual certificate

For feasible $`x`$ and any $`\nu`$, let $`r = Hx + c + A^\top\nu`$. For $`d \in \ker\,A`$ the term $`A^\top\nu`$ is
orthogonal to $`d`$, so $`r^\top d = \nabla f(x)^\top d`$. Writing $`d = Zy`$ with $`Z`$ an orthonormal basis of
$`\ker\,A`$, $`d^\top H d = y^\top Z^\top HZ\,y \ge \mu\|y\|^2 = \mu\|d\|^2`$, and the quadratic expands exactly:

```math
f(x+d) = f(x) + \nabla f(x)^\top d + \tfrac12 d^\top H d \;\ge\; f(x) + r^\top d + \tfrac{\mu}{2}\|d\|^2 . \qquad (D5.1)
```

Write $`P = P_{\ker\,A}`$. Over $`d \in \ker\,A`$, $`r^\top d = (Pr)^\top d`$, and $`(Pr)^\top d + \frac\mu2\|d\|^2`$ is
minimized at $`d = -Pr/\mu`$ with value $`-\|Pr\|^2/(2\mu)`$. Every feasible point is $`x + d`$ for some
$`d \in \ker\,A`$, so

```math
v^* \ge f(x) - \frac{\|P_{\ker\,A} r\|^2}{2\mu}, \qquad 0 \le f(x) - v^* \le \frac{\|P_{\ker\,A} r\|^2}{2\mu} . \quad ∎ \qquad (D5.2)
```

Curvature is used only along $`\ker\,A`$, so $`H`$ may be indefinite across the constraints.

**A multiplier needs its own check.** $`PA^\top = 0`$, so $`Pr`$ does not depend on $`\nu`$. The bound certifies
$`x`$ and is silent on whether a claimed $`\nu`$ is a KKT witness, which requires $`Hx + c + A^\top\nu = 0`$ in
full. The third defect class of §6 is a correct $`x`$ with a wrong $`\nu`$, and only a verifier that checks the full
equation rejects it.

**Sound and complete on this family.** If $`x`$ is feasible, $`Z^\top HZ \succ 0`$ is verified and $`Pr = 0`$,
the bound gives $`f(x) \le v^*`$, and strict convexity on the feasible set makes $`x`$ the unique minimizer.
Conversely the unique minimizer satisfies $`Pr = 0`$ by first-order optimality. The verifier accepts exactly the
valid submissions, so $`\alpha = \beta = 0`$ is a theorem for this family. The test set confirms it on 3,600
submissions in exact rational arithmetic.

## D6. The certificate template for other task types

Each certificate has three parts: a residual the submission exposes, a constant the task designer verifies, and an
inequality between them.

- **Convex program.** For primal-feasible $`x`$ and dual-feasible $`(\lambda, \nu)`$, weak duality gives
  $`g(\lambda, \nu) \le v^*`$, hence $`f(x) - v^* \le f(x) - g(\lambda, \nu)`$.
- **Linear system.** $`A(x - x^*) = Ax - b`$, so
  $`\|x - x^*\|_2 \le \|A^{-1}\|_2\,\|b - Ax\|_2 = \|b - Ax\|_2/\sigma_{\min}(A)`$.
- **Eigenpair of a symmetric matrix.** Expand $`\hat v = \sum_i c_i u_i`$ in an orthonormal eigenbasis. Then
  $`\|A\hat v - \hat\lambda\hat v\|^2 = \sum_i (\lambda_i - \hat\lambda)^2 c_i^2 \ge \min_i(\lambda_i - \hat\lambda)^2\,\|\hat v\|^2`$.
- **Fixed point of a contraction.**
  $`\|x - x^*\| \le \|x - g(x)\| + \|g(x) - g(x^*)\| \le \|g(x) - x\| + L\|x - x^*\|`$, so
  $`\|x - x^*\| \le \|g(x) - x\|/(1-L)`$. ∎

In every case the true solution appears only on the left side. The checker computes the right side from the
submission.

## D7. Transformations propagate tolerances

Given a bijection $`\Phi : F \to F'`$ with $`\left\vert J'(\Phi(u)) - aJ(u) - b\right\vert \le \varepsilon`$ and $`a > 0`$:

- Taking the infimum over $`u`$, and using that $`\Phi`$ is onto, gives
  $`av + b - \varepsilon \le v' \le av + b + \varepsilon`$.
- If $`J(u) - v \le \delta`$, then $`J'(\Phi(u)) \le a(v+\delta) + b + \varepsilon`$. Subtracting
  $`v' \ge av + b - \varepsilon`$ gives $`J'(\Phi(u)) - v' \le a\delta + 2\varepsilon`$. ∎

**The bound is attained.** Take two points with $`J = (v, v+\delta)`$ and set
$`J'(\Phi(u_1)) = av + b - \varepsilon`$ and $`J'(\Phi(u_2)) = a(v+\delta) + b + \varepsilon`$. Then
$`v' = av + b - \varepsilon`$ and the transformed gap of $`u_2`$ is exactly $`a\delta + 2\varepsilon`$. No smaller
tolerance is safe in general.

**Composition.** Apply a second transformation with parameters $`(a_2, b_2, \varepsilon_2)`$ to the output of the
first. Then

```math
\big|J'' - a_2a_1J - (a_2b_1 + b_2)\big| \le a_2\,\big|J' - a_1J - b_1\big| + \big|J'' - a_2J' - b_2\big| \le a_2\varepsilon_1 + \varepsilon_2 , \qquad (D7.1)
```

so the pair composes to $`(a_2a_1,\ a_2\varepsilon_1 + \varepsilon_2)`$. By induction a chain of $`k`$ steps has
$`a = \prod_j a_j`$ and $`\varepsilon = \sum_j \big(\prod_{l>j} a_l\big)\varepsilon_j`$. ∎ An exact conversion with
$`a = 100`$, an exact rescaling with $`a = 0.5`$ and a discretization with $`\varepsilon = 0.003`$ give
$`(50, 0.003)`$ with the discretization last and $`(50, 0.15)`$ with it first; at $`\delta = 0.01`$ the tolerances
owed are 0.506 and 0.8.

## D8. Grading error shifts the process-reward target

Given prefix $`h`$, $`E[V\mid h] = \alpha(h)(1-p(h)) + (1-\beta(h))p(h) = \tilde p(h)`$. For binary cross-entropy
with logit $`s`$, $`\partial\ell/\partial s = \sigma(s) - V`$, so

```math
E[\nabla_s\ell(s,V) - \nabla_s\ell(s,Z) \mid h] = E[Z\mid h] - E[V\mid h] = p(h) - \tilde p(h) . \qquad (D8.1)
```

The expected loss is minimized at $`\sigma(s^*) = \tilde p(h)`$, so the learned evaluator converges to the
corrupted target. $`\tilde p - p = \alpha(1-p) - \beta p`$: false rejection dominates when
$`\beta p > \alpha(1-p)`$ and pushes the target down, penalizing valid alternative proofs; false acceptance
dominates in the opposite case and pushes it up, rewarding flawed ones. ∎

**Correction.** $`E[\bar V] = \alpha + (1-\alpha-\beta)\theta`$, so
$`\hat\theta_{\text{corr}} = (\bar V - \alpha)/(1-\alpha-\beta)`$ is unbiased when $`\alpha + \beta < 1`$, with
variance $`\mathrm{Var}(\bar V)/(1-\alpha-\beta)^2`$ because it is an affine map of $`\bar V`$. ∎ A sound and
complete verifier (D5) has $`\alpha = \beta = 0`$ and pays neither the bias nor the variance.

## D9. What a policy learns from a grader

Split the starting policy's trajectories into four classes by validity $`Z`$ and verdict $`V`$:

| | Accepted ($`V = 1`$) | Rejected ($`V = 0`$) |
| --- | --- | --- |
| Valid | $`\theta(1-\beta)`$ | $`\theta\beta`$ |
| Invalid | $`(1-\theta)\alpha`$ | $`(1-\theta)(1-\alpha)`$ |

Optimizing the expected verdict under a penalty on divergence from the starting policy,
$`\max_\pi E_\pi[V] - \eta^{-1}\mathrm{KL}(\pi\,\|\,\pi_0)`$, has the solution $`\pi \propto \pi_0 e^{\eta V}`$:
accepted classes are multiplied by $`e^\eta`$ and the masses are renormalized. The valid share is then

```math
\theta_\eta = \frac{\theta(1-\beta)e^{\eta} + \theta\beta}{\big[\theta(1-\beta) + (1-\theta)\alpha\big]e^{\eta} + \theta\beta + (1-\theta)(1-\alpha)}
\ \longrightarrow\ \frac{\theta(1-\beta)}{\theta(1-\beta) + (1-\theta)\alpha} \quad (\eta \to \infty), \qquad (D9.1)
```

which is $`\Pr(Z = 1 \mid V = 1)`$ at the starting policy, the grader's positive predictive value. The accepted
share, which is the observed score, goes to one. ∎

**Ceiling.** With $`\alpha = 0`$ the limit is one for any $`\beta < 1`$. With $`\alpha > 0`$ it is below one: 83.2%
for $`\theta = 64\%`$ and $`\alpha = 36\%`$, 98.5% for $`\theta = 72\%`$ and $`\alpha = 4\%`$, and 40% on the test
set of §6, where one third of the submissions are valid and final-answer matching accepts 75% of the rest.

**Lost routes.** Let two valid routes start with equal mass and let the grader accept one and always reject the
other. After reweighting, the rejected route's share of valid work is $`1/(1 + e^{\eta})`$: 26.9%, 11.9% and 1.8%
at $`\eta = 1, 2, 4`$.

## D10. Variants of one template are not independent evidence

For $`F`$ independent families of $`K`$ variants with common variance $`\sigma^2`$ and within-family correlation
$`\rho_w`$, $`\mathrm{Var}(\bar Z) = \sigma^2[1+(K-1)\rho_w]/(FK)`$ and
$`n_{\text{eff}} = FK/(1+(K-1)\rho_w)`$. For $`F = 50`$, $`K = 8`$ and $`\rho_w = 0.6`$,
$`n_{\text{eff}} = 400/(1 + 7 \times 0.6)`$, which is 77. ∎

## D11. When certificates pay for themselves

Total cost with certificates is $`C_0 + N(c_v + uc_e)`$, and with full expert review it is $`Nc_e`$. The first is
smaller exactly when $`N[(1-u)c_e - c_v] > C_0`$, that is $`N > C_0/[(1-u)c_e - c_v]`$ when
$`(1-u)c_e > c_v`$. ∎ With $`C_0 = 400c_e`$, $`u = 15\%`$ and $`c_v = 2\%`$ of $`c_e`$ the break-even is 482
submissions, and each further submission releases $`(1 - u)c_e - c_v`$, 83% of an expert review.
