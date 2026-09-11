#!/usr/bin/env python3
"""Compare NN-classifier assignments on the 760-seq Seabra set to published Seabra clade labels.

Inputs:
  - step7-classifier/nn-760.tsv (our assignments)
  - Seabra clade lists at .../vadr_files/Z{A_african,B.1_asian,B.2_american}_id.txt

Output (stdout): confusion matrix, overall + per-clade agreement, list of disagreements.
"""

import sys
from collections import Counter, defaultdict

NN_TSV = "<project-root>/canonical-8seq-cm/step7-classifier/nn-760.tsv"
SEABRA_LISTS = {
    "african":   "<backup-dir>/vadr_files/ZA_african_id.txt",
    "asian":     "<backup-dir>/vadr_files/ZB.1_asian_id.txt",
    "american":  "<backup-dir>/vadr_files/ZB.2_american_id.txt",
}


def short(acc):
    return acc.split(".")[0].strip()


seabra = {}
for clade, path in SEABRA_LISTS.items():
    for line in open(path):
        a = short(line)
        if a:
            seabra[a] = clade

ours = {}
with open(NN_TSV) as f:
    next(f)
    for line in f:
        sid, nn, ident, clade = line.rstrip("\n").split("\t")
        ours[sid] = (clade, nn, float(ident))

print(f"Loaded {len(ours)} our assignments, {len(seabra)} Seabra labels")
overlap = set(ours.keys()) & set(seabra.keys())
print(f"Overlap: {len(overlap)} seqs")

# Confusion matrix: rows = our, cols = seabra
cm = defaultdict(lambda: defaultdict(int))
disagree = []
agree = 0
for sid in overlap:
    o_clade = ours[sid][0]
    s_clade = seabra[sid]
    cm[o_clade][s_clade] += 1
    if o_clade == s_clade:
        agree += 1
    else:
        disagree.append((sid, o_clade, s_clade, ours[sid][1], ours[sid][2]))

print()
print("=" * 60)
print("CONFUSION MATRIX (rows=our, cols=Seabra)")
print("=" * 60)
clades = ["african", "asian", "american"]
hdr = "our|seabra"
print(f"{hdr:<14}" + "".join(f"{c:>12}" for c in clades) + f"{'row_total':>12}")
for o in clades:
    row = [cm[o][s] for s in clades]
    print(f"{o:<14}" + "".join(f"{v:>12d}" for v in row) + f"{sum(row):>12d}")
col_totals = {s: sum(cm[o][s] for o in clades) for s in clades}
print(f"{'col_total':<14}" + "".join(f"{col_totals[s]:>12d}" for s in clades) + f"{sum(col_totals.values()):>12d}")

print()
print(f"Overall agreement: {agree}/{len(overlap)} = {100.0*agree/len(overlap):.2f}%")
print()
print("Per-clade (Seabra column -> our recall = TP / Seabra_total):")
for c in clades:
    tp = cm[c][c]
    st = col_totals[c]
    if st:
        print(f"  {c:<10}: TP={tp:>4} / Seabra_total={st:>4} = recall {100.0*tp/st:6.2f}%")
    else:
        print(f"  {c:<10}: 0 Seabra labels in overlap")

# Seqs in our NN but not in Seabra (and vice versa)
only_ours = set(ours.keys()) - set(seabra.keys())
only_seabra = set(seabra.keys()) - set(ours.keys())
print()
print(f"In our assignments but not in any Seabra list ({len(only_ours)}):")
for sid in sorted(only_ours)[:20]:
    print(f"  {sid}\t{ours[sid][0]}\t(nn={ours[sid][1]}, ident={ours[sid][2]:.2f}%)")
if len(only_ours) > 20:
    print(f"  ... and {len(only_ours)-20} more")

print()
print(f"Disagreements ({len(disagree)}):")
print("seq_id\tour\tseabra\tnearest_train\tidentity_pct")
for d in disagree:
    print("\t".join(str(x) for x in d))
