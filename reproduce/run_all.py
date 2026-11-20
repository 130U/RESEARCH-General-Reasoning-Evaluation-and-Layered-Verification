"""Recompute every figure in the article and compare it with the text.

    python reproduce/run_all.py            # full sizes
    python reproduce/run_all.py --quick    # smaller sample sizes for the two sampling checks

Writes reproduce/results.md and exits with status 1 if any figure disagrees.
Standard library only (Python 3.12+).
"""

from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import acceptance_thresholds as thresholds  # noqa: E402
import certificates  # noqa: E402
import scoring  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()
    q = args.quick
    sections: list[tuple[str, list]] = []
    rows: list = []

    def section(title: str) -> None:
        nonlocal rows
        rows = []
        sections.append((title, rows))

    def check(label, value, article, tol, where, shown=None):
        rows.append((label, value, shown if shown is not None else article, where, abs(value - article) <= tol))

    def check_true(label, ok, where, shown="holds"):
        rows.append((label, None, shown, where, bool(ok)))

    th = thresholds.run()

    # ------------------------------------------------------------------ Section 1
    section("Scores, rankings and certified leads (Section 1)")
    r = scoring.ranking_example()
    check("Model A, true validity 72%, false acceptance 4%: observed score (%)", round(100 * r["s_A"], 2), 73.12, 1e-9, "§1")
    check("Model B, true validity 64%, false acceptance 36%: observed score (%)", round(100 * r["s_B"], 2), 76.96, 1e-9, "§1")
    check_true("The model with the lower true validity ranks first", r["weaker_model_ranks_first"], "§1")
    check("False acceptance for Model B above which the pair reverses (%)", 100 * th["reversal_alpha_B"], 25.3, 0.05, "§1")
    check("Lead of 3 points over a rival at 80%: certified below a false acceptance of (%)", 100 * th["certified_lead"]["lead 3 points, rival at 80%"], 15, 1e-9, "§1")
    check("Lead of 3 points over a rival at 50%: certified below (%)", 100 * th["certified_lead"]["lead 3 points, rival at 50%"], 6, 1e-9, "§1")
    check_true("Certified-lead condition is tight on 200,000 random cases", th["checks"]["certified lead rule"], "§1, D2")

    # ------------------------------------------------------------------ Section 2
    section("When a screen may decide (Section 2)")
    check("Sensitivity 52.87%, target 5%: share of unflagged work escalated (%)", 100 * thresholds.random_escalation(0.5287, 0.05), 89, 0.5, "§2")
    check("Sensitivity 0.80: share escalated (%)", 100 * th["random_escalation"]["sensitivity 0.80"], 75, 1e-9, "§2")
    check("Sensitivity 0.90: share escalated (%)", 100 * th["random_escalation"]["sensitivity 0.90"], 50, 1e-9, "§2")
    check("Sensitivity 0.95: share escalated (%)", 100 * th["random_escalation"]["sensitivity 0.95"], 0, 1e-9, "§2")
    check("Clean run that bounds false acceptance at 5% with 95% confidence", th["clean_run_needed"]["alpha 5%"], 59, 0, "§2")
    check("Clean run that bounds false acceptance at 1%", th["clean_run_needed"]["alpha 1%"], 299, 0, "§2")

    # ------------------------------------------------------------------ Section 4
    section("Task transformations (Section 4)")
    check_true("Tolerance rule aδ + 2ε holds on 20,000 random problems", scoring.tolerance_propagation(), "§4")
    t = scoring.tolerance_tight_example()
    check("The rule is attained by a two-point example", t["transformed_gap"], t["bound"], 1e-12, "D7", shown="equal")
    first = th["composition"]["convert, rescale, discretize"]
    second = th["composition"]["discretize, convert, rescale"]
    check("Discretization last: scaling a", first[0][0], 50, 1e-12, "§4")
    check("Discretization last: error ε", first[0][1], 0.003, 1e-12, "§4")
    check("Discretization last: tolerance owed", first[1], 0.506, 1e-12, "§4")
    check("Discretization first: scaling a", second[0][0], 50, 1e-12, "§4")
    check("Discretization first: error ε", second[0][1], 0.15, 1e-12, "§4")
    check("Discretization first: tolerance owed", second[1], 0.8, 1e-12, "§4")
    check_true("Composition law equals step-by-step application on 20,000 random chains", th["checks"]["composition law"], "§4, D7")

    # ------------------------------------------------------------------ Section 5
    section("What a grader does to training (Section 5)")
    draws = 200_000 if q else 1_000_000
    for p, a, b in ((0.8, 0.05, 0.2), (0.3, 0.3, 0.05)):
        s = scoring.prm_target_shift(p=p, alpha=a, beta=b, draws=draws)
        four_se = 4 * (2 / draws) ** 0.5
        regime = "false rejection dominates" if b * p > a * (1 - p) else "false acceptance dominates"
        check(f"Gradient shift p − p̃ by direct sampling, {regime} (p = {p}, α = {a}, β = {b})", s["mc_shift"], s["expected_shift"], four_se, "§5", shown=f"{s['expected_shift']:.4f}")
    c = scoring.noise_correction(reps=10_000 if q else 40_000)
    check("Noise-corrected estimate, mean over repeated samples (θ = 0.6)", c["mean"], 0.6, 0.002, "§5")
    check("Variance inflation against 1/(1 − α − β)²", c["variance_ratio"], c["predicted_ratio"], 0.06 if q else 0.04, "§5", shown=f"{c['predicted_ratio']:.4f}")
    path = th["model_B_path"]
    article_path = {0: (64.0, 77.0), 1: (74.9, 90.1), 2: (79.9, 96.1), 4: (82.7, 99.5)}
    for eta, (validity, score) in article_path.items():
        got = path[eta]
        check(f"Model B at optimization strength {eta}: true validity (%)", 100 * got[0], validity, 0.05, "§5 table")
        check(f"Model B at optimization strength {eta}: observed score (%)", 100 * got[1], score, 0.05, "§5 table")
    check("Model B: limit of true validity, the grader's positive predictive value (%)", 100 * th["ppv"]["model B, answer matching"], 83.2, 0.05, "§5")
    check("Model A: limit of true validity (%)", 100 * th["ppv"]["model A, answer matching"], 98.5, 0.05, "§5")
    check_true("The limit of the reweighted policy equals the positive predictive value", th["checks"]["tilt limit equals ppv"], "§5, D9")
    for eta, want in ((1, 26.9), (2, 11.9), (4, 1.8)):
        check(f"Share of valid work on a route the grader rejects, strength {eta} (%)", 100 * th["rejected_route_share"][eta], want, 0.05, "§5")

    # ------------------------------------------------------------------ Section 6
    section("A test set with exactly known verdicts (Sections 3 and 6)")
    bench = certificates.run()
    check("Task families", bench["families"], 600, 0, "§6")
    check("Submissions", bench["submissions"], 3600, 0, "§6")
    check("Valid certificates", bench["valid"], 1200, 0, "§6")
    check("Submissions with a controlled defect", bench["invalid"], 2400, 0, "§6")
    check("Invalid submissions that report the correct optimal value", bench["invalid_reporting_v_star"], 1800, 0, "§6")
    check("Their share of all invalid submissions (%)", 100 * bench["invalid_reporting_v_star"] / bench["invalid"], 75, 1e-9, "§6")
    article_table = {
        "final_answer": ("Final-answer matching", 75.0, 0.0, 40.0),
        "reference_path": ("Strict reference-path matching", 0.0, 50.0, 100.0),
        "certificate": ("Certificate verification", 0.0, 0.0, 100.0),
    }
    for key, (label, fa, fr, share) in article_table.items():
        row = bench["protocols"][key]
        check(f"{label}: false acceptance (%)", row["false_acceptance_percent"], fa, 1e-12, "§6 table")
        check(f"{label}: false rejection (%)", row["false_rejection_percent"], fr, 1e-12, "§6 table")
        check(f"{label}: valid share of accepted submissions (%)", row["valid_share_of_accepted_percent"], share, 1e-12, "§6 table")
    by = {k: bench["protocols"][k]["accepted_by_class"] for k in article_table}
    flawed = lambda k: by[k]["D1"] + by[k]["D2"] + by[k]["D3"] + by[k]["D4"]  # noqa: E731
    check("Final-answer matching: flawed solutions accepted", flawed("final_answer"), 1800, 0, "§6 table")
    check("Reference-path matching: valid elimination proofs rejected", 600 - by["reference_path"]["E"], 600, 0, "§6 table")
    check("Certificate verification: invalid proofs accepted, fewer than final-answer matching by", flawed("final_answer") - flawed("certificate"), 1800, 0, "§6")
    check("Certificate verification: valid alternative solutions kept, more than reference-path matching by", by["certificate"]["E"] - by["reference_path"]["E"], 600, 0, "§6")
    check("Certificate verification: submissions with a multiplier that fails stationarity accepted", by["certificate"]["D3"], 0, 0, "§6")
    check("Projected-residual bound holds at feasible perturbations (families)", bench["residual_bound_checks_passed"], 600, 0, "§3, §6")
    check("Valid share of the test set before training (%)", 100 * bench["valid"] / bench["submissions"], 100 / 3, 1e-9, "§6", shown="one third")
    check("Positive predictive value of final-answer matching on the test set (%)", 100 * th["ppv"]["test set, answer matching"], 40, 1e-9, "Summary, §6")
    check("Positive predictive value of certificate checking on the test set (%)", 100 * th["ppv"]["test set, certificate"], 100, 1e-9, "Summary, §6")

    # ------------------------------------------------------------------ Section 7
    section("Task families and the economics of certificates (Section 7)")
    check("Effective sample size of 50 families of 8 variants at ρ_w = 0.6", round(scoring.effective_sample_size()), 77, 0, "§7")
    check("Break-even volume (submissions)", scoring.break_even_volume(400, 1.0, 0.02, 0.15), 482, 0.5, "§7")
    check("Share of an expert review released per further submission (%)", 100 * (1 - 0.15 - 0.02), 83, 1e-9, "§7")
    check_true("Break-even volume separates the cheaper workflow from the dearer on 10,000 random cost settings", scoring.break_even_consistent(), "§7")

    total = sum(len(r) for _, r in sections)
    failed = sum(1 for _, r in sections for row in r if not row[4])

    def fmt(x):
        if x is None:
            return ""
        if isinstance(x, float):
            return f"{x:.4f}" if abs(x) < 1000 else f"{x:,.2f}"
        return f"{x:,}" if isinstance(x, int) else str(x)

    def art(x):
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            return str(x)
        return format(x, ",.10g")

    lines = [
        "# Results",
        "",
        "Every figure in the article, recomputed.",
        "",
        f"{total - failed} of {total} figures agree with the article" + (" · quick run" if q else ""),
    ]
    for title, section_rows in sections:
        lines += ["", f"## {title}", "", "| Quantity | Recomputed | Article | Where | Agrees |", "| --- | ---: | ---: | --- | :---: |"]
        for label, value, shown, where, ok in section_rows:
            lines.append(f"| {label.replace(chr(124), chr(92) + chr(124))} | {fmt(value)} | {art(shown)} | {where} | {'✓' if ok else '✗'} |")
    lines += ["", "## Accepted submissions by class", "", "600 submissions in each class.", "",
              "| Protocol | Lagrange (valid) | Elimination (valid) | Infeasible | Not stationary | Multiplier fails | Wrong value |",
              "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for key, (label, *_rest) in article_table.items():
        k = by[key]
        lines.append(f"| {label.replace(chr(124), chr(92) + chr(124))} | {k['L']} | {k['E']} | {k['D1']} | {k['D2']} | {k['D3']} | {k['D4']} |")
    report = "\n".join(lines) + "\n"
    (HERE / "results.md").write_text(report, encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
