# Design notes

Why each piece of the design is the way it is, what it was chosen over, and what the review workflow has to supply
for the results to hold. Proofs are in [derivations](derivations.md); figures are recomputed in
[results](../reproduce/results.md).

## Choices and the alternatives they beat

| Choice | Alternative | Why | When I would switch |
| --- | --- | --- | --- |
| **Acceptance by proof obligations** | Final-answer matching | A matched answer accepts unsupported work: 75.0% of the invalid submissions in §6, and a policy trained on it stops at 40% valid | Tasks whose only deliverable is the answer, where answer checking is exactly right |
| **Obligations that do not name a route** | Reference-path matching | A fixed path rejects valid alternatives, 50.0% of the valid proofs in §6, and training against it removes those routes from the policy ([D9](derivations.md#d9-what-a-policy-learns-from-a-grader)) | Tasks that prescribe a method in the specification, where the method is itself an obligation |
| **Descendants of a failed node marked unverified** | Keep grading downstream steps as if the premise held | A false premise breaks the derivation, and downstream credit would reward a broken argument ([D3](derivations.md#d3-proof-obligations-soundness-and-failure-propagation)) | Training signals that want partial credit: recorded separately, never as acceptance |
| **Certificates that need no reference solution** | Compare against the reference | The check inherits none of the reference's errors and its cost is a few matrix products ([D5](derivations.md#d5-the-projected-residual-certificate), [D6](derivations.md#d6-the-certificate-template-for-other-task-types)) | Obligations with no residual to expose, which go to the semantic layers |
| **A claimed multiplier checked in full** | Check the projected residual alone | $`P_{\ker\,A}r`$ does not depend on $`\nu`$, so a wrong multiplier passes a partial check | Submissions that claim no multiplier |
| **Three layers with distinct standing** | One LLM judge for everything, or specialists for everything | Each obligation goes to the cheapest checker that can decide it; a judge screens until its measured sensitivity clears $`1 - \alpha^*`$ ([D4](derivations.md#d4-when-a-screen-may-decide)) | A judge with a clean run on the obligation type: 59 known-invalid items for 5%, 299 for 1% |
| **Displayed reasoning treated as an output** | Treat the displayed chain of thought as the model's reasoning | A claim needs observable support in tool calls, return values and intermediate outputs | No case |
| **Efficiency recorded apart from correctness** | Penalize slow or repetitive solutions | A slower solution is still a correct solution; only a limit fixed in advance can reject | No case |
| **Tolerances propagated through transformations** | Reuse the original tolerance | The tolerance owed is $`a\delta + 2\varepsilon`$, it is attained, and it depends on the order of the chain ([D7](derivations.md#d7-transformations-propagate-tolerances)) | Exact transformations with $`a = 1`$ |
| **Process rewards drawn from certified nodes** | Step labels from a learned or outcome-based grader | A certified node has $`\alpha = \beta = 0`$, so the reward has no ceiling below 100% and removes no route | No case on the families a certificate decides |
| **Splits by task family** | Splits by record | Variants are correlated; 400 responses count as 77 ([D10](derivations.md#d10-variants-of-one-template-are-not-independent-evidence)) | No case |

## What a task specification fixes before any response exists

```text
Γ_q        domain assumptions and execution constraints
A_q        permitted tools, environments and resources (hard limits only)
C_q        target conclusion and its claimed strength
obligations
  assumption validity      which assumptions the derivation may use
  method applicability     conditions for each method: uniformity, domains, exchanges of limits
  evidentiary support      what must be cited or computed
  compliant execution      T_comp(τ) = 1
  approximation bounds     parameter, domain of validity, uniform error bound
certificates
  per obligation type      residual, verified constant, inequality
```

For each submission the review record holds the dependency graph, the status of each node (verified, failed,
unverified or disputed), the first failed node, the layer that decided each node, and the execution evidence each
claim was checked against.

## Which layer decides what

| Obligation | Decided by | Standing of the verdict |
| --- | --- | --- |
| Feasibility, stationarity, claimed value, a claimed witness | Certificate verifier | Computation: $`\alpha = \beta = 0`$ on the family |
| Required deliverables, tool permissions, resource limits set in advance | Code and rule checks | Decisive against the written specification |
| Missing evidence, misapplied rules, conclusions beyond their premises | LLM-assisted screening, with random escalation of unflagged work | A screen, until its sensitivity is measured above $`1 - \alpha^*`$ |
| Method applicability, questions with several reasonable interpretations, disputes | Specialist scholars | Expert judgment; a question the evidence cannot settle stays open |

The randomly escalated share of unflagged work is also the calibration sample: it is where the screen's sensitivity
is measured.

## Method applicability has its own obligation

Pointwise convergence at a fixed parameter value does not justify using an approximation inside an optimization,
an integral or an exchange of limits. A claim about order of accuracy needs an approximation parameter, a domain of
validity and a uniform error bound. Where this cannot be decided programmatically, an LLM locates the concern and
a specialist reviews the assumptions and the derivation, and the record states which layer decided it.

## What the results need from the workflow

1. **Sound local checks.** D3 is as strong as the check at each node. The certificate layer supplies checks that
   are theorems; the semantic layers supply checks with measured error rates.
2. **A verified constant per certificate.** The curvature bound $`\mu`$, a lower bound on $`\sigma_{\min}(A)`$, a
   Lipschitz constant below one. These are the designer's obligations, verified once per task family.
3. **Exact or validated arithmetic.** The test set of §6 uses rationals. A floating-point verifier carries
   interval bounds on the residual, so that a certificate is never accepted on rounding.
4. **References withheld from the screening layer**, so that the screen does not favor one route.
5. **Measured error rates per obligation type.** The thresholds of D2 and D4 take a bound on false acceptance as
   input. It comes from a clean run on known-invalid items or from the randomly escalated sample.

## What to monitor

- **Share of nodes that reach specialists.** Obligations cut too fine make review slow and disputes common.
- **Unverified is not wrong.** Nodes downstream of a failure are excluded from capability reports as model errors.
- **Missing execution records.** A claim whose records are absent stays unverified. A rising rate is a pipeline
  failure, and it is reported as one.
- **Screen sensitivity over time.** Sensitivity moves with the judge's version and with the policy being judged,
  so it is re-measured on the escalated sample.

## Extensions

1. **Composing certified and adjudicated nodes.** A task with both kinds of obligation has a false-acceptance
   bound equal to the sum of the adjudicated nodes' bounds, by the union bound; a sharper rule would use the graph.
2. **Obligation graphs extracted from free-form proofs.** Reliable extraction would bring D3 to submissions that
   do not declare their structure.
3. **Certificates for further task types.** Any problem with a stable residual has one: ordinary differential
   equations with a posteriori error estimators and root-finding with interval enclosures are the next two.
