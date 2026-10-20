"""Step 3. Draw the PRISMA 2020 flow diagram from outputs/prisma_counts.json.
Output: outputs/figures/prisma_flow.png (300 dpi)
"""
import json, matplotlib
from common import OUT, FIGURES, QA_THRESHOLD
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
P=json.load(open(OUT / "prisma_counts.json"))
plt.rcParams.update({"font.family":"DejaVu Serif","font.size":7})
fig,ax=plt.subplots(figsize=(6.3,7.2)); ax.set_xlim(0,100); ax.set_ylim(0,112); ax.axis("off")
def box(x,y,w,h,t,fc="white",bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="square,pad=0",lw=0.7,ec="black",fc=fc))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=6.6,wrap=True,fontweight="bold" if bold else "normal",linespacing=1.25)
def arr(x1,y1,x2,y2): ax.annotate("",xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle="-|>",lw=0.7,color="black",mutation_scale=7))
ex=P["excluded_full"]; sb=P["sb_excluded"]
# stage labels
for y,h,t in [(92,18,"Identification"),(38,52,"Screening"),(2,34,"Included")]:
    box(0,y,5,h,"",fc="#dce6f2"); ax.text(2.5,y+h/2,t,rotation=90,ha="center",va="center",fontsize=7,fontweight="bold")
# database column
box(7,94,32,14,f"Records identified from\nOpenAlex (n = {P['db_identified']})\n2021–2026, journal and\nconference papers")
box(43,94,22,14,f"Duplicates removed\nbefore screening\n(n = {P['duplicates']})"); arr(39,101,43,101)
box(7,78,32,10,f"Records screened\n(title and abstract)\n(n = {P['screened']})"); arr(23,94,23,88)
box(43,78,22,10,f"Records excluded\n(n = {P['excluded_ta']})"); arr(39,83,43,83)
box(7,64,32,10,f"Reports sought for retrieval\n(n = {P['sought']})"); arr(23,78,23,74)
box(43,64,22,10,f"Reports not retrieved\n(n = {P['not_retrieved']})"); arr(39,69,43,69)
box(7,46,32,14,f"Reports assessed for\neligibility (n = {P['assessed']})"); arr(23,64,23,60)
box(43,40,22,20,f"Excluded (n = {sum(ex.values())}):\nEC3 (n = {ex.get('EC3',0)})\nEC4 (n = {ex.get('EC4',0)})\nEC5 (n = {ex.get('EC5',0)})\nEC6 (n = {ex.get('EC6',0)})"); arr(39,53,43,53)
# other methods column
box(68,94,31,14,f"Records identified from\ncitation searching\n(backward and forward)\n(n = {P['sb_identified']})")
box(68,78,31,10,f"Excluded by title or already\nidentified (n = {P['sb_excluded_title']})"); arr(83.5,94,83.5,88)
box(68,64,31,10,f"Reports sought (n = {P['sb_sought']})\nnot retrieved (n = {P['sb_not_retrieved']})"); arr(83.5,78,83.5,74)
box(68,40,31,20,f"Reports assessed (n = {P['sb_assessed']})\nExcluded:\nEC3 (n = {sb.get('EC3',0)})\nEC4 (n = {sb.get('EC4',0)})\nEC6 (n = {sb.get('EC6',0)})"); arr(83.5,64,83.5,60)
# included
box(7,22,58,12,f"Studies eligible for quality assessment (n = {P['eligible_total']})\nBelow quality threshold of {QA_THRESHOLD} (n = {P['below_qa']})"); arr(23,46,23,34); arr(83.5,40,60,34)
box(7,4,58,12,f"Studies included in the synthesis (n = {P['included']})\nmean QA score {P['qa_mean']} (range {P['qa_min']:.1f}–{P['qa_max']:.1f})",fc="#eef3ea",bold=True); arr(36,22,36,16)
plt.savefig(FIGURES / "prisma_flow.png",dpi=300,bbox_inches="tight"); print("Saved", FIGURES / "prisma_flow.png")
