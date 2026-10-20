"""Step 5 (after the second reviewer returns the workbook). Cohen's kappa for screening and coding.

Input : agreement/Interrater_Agreement_HITL_SLR.xlsx (filled by the second reviewer)
Output: outputs/kappa.json
Usage : python scripts/05_kappa.py [path/to/workbook.xlsx]
The result must match the 'Kappa' sheet inside the workbook (independent check of the Excel formulas).
"""
import json, sys
from common import ROOT, OUT
from collections import Counter
from openpyxl import load_workbook

ROLES = ["Specifier", "Explorer", "Reviewer", "Editor", "Oracle", "Teacher"]
POINTS = ["Before", "Loop", "After"]


def kappa(r2, r1):
    pairs = [(str(a), str(b)) for a, b in zip(r2, r1) if a not in (None, "")]
    n = len(pairs)
    if n == 0:
        return dict(n=0)
    po = sum(a == b for a, b in pairs) / n
    c2, c1 = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(c2[k] * c1[k] for k in set(c2) | set(c1)) / n ** 2
    k = None if pe == 1 else (po - pe) / (1 - pe)
    return dict(n=n, po=round(po, 3), pe=round(pe, 3), kappa=None if k is None else round(k, 3))


def label(k):
    if k is None:
        return "n/a"
    return ("poor" if k < 0 else "slight" if k <= .2 else "fair" if k <= .4 else
            "moderate" if k <= .6 else "substantial" if k <= .8 else "almost perfect")


def col(ws, c, n, start=2):
    return [ws.cell(row=r, column=c).value for r in range(start, start + n)]


def main(path, out=None):
    wb = load_workbook(path, data_only=False)
    sa, r1s, sb, r1c = wb["A_Screening"], wb["R1_Screening"], wb["B_Coding"], wb["R1_Coding"]
    ns, nc = r1s.max_row - 1, r1c.max_row - 1
    res = {"screening": kappa(col(sa, 7, ns), col(r1s, 3, ns))}
    pooled = {"roles": ([], []), "points": ([], [])}
    for j, name in enumerate(ROLES + POINTS):
        a, b = col(sb, 6 + j, nc), col(r1c, 3 + j, nc)
        res[name] = kappa(a, b)
        grp = "roles" if name in ROLES else "points"
        pooled[grp][0].extend(a); pooled[grp][1].extend(b)
    res["roles_pooled"] = kappa(*pooled["roles"])
    res["points_pooled"] = kappa(*pooled["points"])
    res["evaluation_level"] = kappa(col(sb, 15, nc), col(r1c, 12, nc))
    for v in res.values():
        if "kappa" in v or v.get("n"):
            v["interpretation"] = label(v.get("kappa"))
    print(f"{'variable':22s} {'n':>4s} {'Po':>6s} {'Pe':>6s} {'kappa':>7s}  interpretation")
    for name, v in res.items():
        if v.get("n"):
            kk = "n/a" if v["kappa"] is None else f"{v['kappa']:.3f}"
            print(f"{name:22s} {v['n']:4d} {v['po']:6.3f} {v['pe']:6.3f} {kk:>7s}  {v['interpretation']}")
        else:
            print(f"{name:22s} not filled yet")
    if out:
        json.dump(res, open(out, "w"), indent=1)
    return res


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else ROOT / "agreement" / "Interrater_Agreement_HITL_SLR.xlsx"
    if not path or not __import__("os").path.exists(path):
        print(f"No agreement workbook found at {path}; skipped.")
    else:
        main(path, OUT / "kappa.json")
