"""Run the whole pipeline: python run_all.py"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "scripts"))
STEPS = ["01_prisma_counts.py", "02_synthesis.py", "03_prisma_figure.py", "04_supplementary_xlsx.py",
         "06_merge_scopus.py", "07_robustness.py"]

for step in STEPS:
    print(f"\n=== {step} ===")
    sys.argv = [step]
    runpy.run_path(str(HERE / "scripts" / step), run_name="__main__")
print("\nDone. Results are in outputs/.")
