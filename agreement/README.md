# Inter-rater agreement

Put the workbook returned by the second reviewer here as `Interrater_Agreement_HITL_SLR.xlsx`, then run

```
python scripts/05_kappa.py
```

The script recomputes Cohen's kappa for title/abstract screening (38 records, 20% stratified random sample, seed 20261020)
and for the coding of roles, intervention points and evaluation levels (20 included studies). Results go to `outputs/kappa.json`
and must match the `Kappa` sheet inside the workbook.
