#!/usr/bin/env python3
"""
This script compares profile-model (1-CM) vs 3-single-seq-model
library annotation of the same 1254-seq test set.

Usage:
  compare.py <profile.ftr> <profile.pass.list> <profile.fail.list> <profile.scn> \
             <threemodel.ftr> <threemodel.pass.list> <threemodel.fail.list> \
             <outprefix>

Produces <outprefix>.seqconcord.txt, <outprefix>.ftrconcord.txt,
<outprefix>.classconcord.txt, plus headline numbers on stdout.
"""
import sys
from collections import defaultdict

CLADE_OF_GRP = {"african": "ZA", "asian": "ZB.1", "american": "ZB.2"}
CLADE_OF_MDL = {"KY989511": "ZA", "MG807646": "ZB.1", "NC_035889": "ZB.2"}


def parse_ftr(path):
    """Return dict seqname -> list of (ftrtype, ftrname, seq_coords, mdl_coords) and seqname -> bestmdl."""
    feats = defaultdict(list)
    bestmdl = {}
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            el = line.rstrip("\n").split()
            if len(el) != 26:
                continue
            (idx, seqname, seqlen, pf, bmdl, ftrtype, ftrname, ftrlen, ftridx, paridx,
             strand, n_from, n_to, n_instp, trc, n5, n3, p_from, p_to, p_instp, p_sc,
             nsa, nsn, seq_coords, mdl_coords, ftr_alerts) = el
            seq_coords = seq_coords.replace(":+", "").replace(":-", "")
            feats[seqname].append((ftrtype, ftrname, seq_coords, mdl_coords))
            bestmdl[seqname] = bmdl
    return feats, bestmdl


def parse_list(path):
    with open(path) as fh:
        return set(l.strip() for l in fh if l.strip())


def parse_scn(path):
    """Return dict seqname -> (grp1, id1) nearest-neighbor clade+identity.

    .scn columns (0-indexed): 0=idx 1=seqname 2=len 3=p/f 4=ant 5=model
    6=grp (e.g. "Zika", top-level group -- NOT the clade) 7=subgrp1 (the
    actual clade: african/asian/american) 8=fract_id1 9=seq1 ...
    Confirmed by reading a real .scn header+data row directly -- an earlier
    version of this script read el[6]/el[7] and silently got "Zika" for
    every row (0% classification concordance).
    """
    out = {}
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            el = line.split()
            if len(el) < 9:
                continue
            seqname = el[1]
            grp1 = el[7]
            id1 = el[8]
            out[seqname] = (grp1, id1)
    return out


def main():
    (prof_ftr, prof_pass, prof_fail, prof_scn,
     lib3_ftr, lib3_pass, lib3_fail, outpre) = sys.argv[1:9]

    prof_feats, _ = parse_ftr(prof_ftr)
    lib3_feats, lib3_bestmdl = parse_ftr(lib3_ftr)
    prof_pass_s = parse_list(prof_pass)
    prof_fail_s = parse_list(prof_fail)
    lib3_pass_s = parse_list(lib3_pass)
    lib3_fail_s = parse_list(lib3_fail)
    prof_scn = parse_scn(prof_scn)

    all_seqs = sorted(prof_pass_s | prof_fail_s | lib3_pass_s | lib3_fail_s)

    # --- 1. per-sequence pass/fail concordance ---
    concordant = 0
    discordant = []
    for s in all_seqs:
        p = "PASS" if s in prof_pass_s else ("FAIL" if s in prof_fail_s else "MISSING")
        l = "PASS" if s in lib3_pass_s else ("FAIL" if s in lib3_fail_s else "MISSING")
        if p == l:
            concordant += 1
        else:
            discordant.append((s, p, l))

    with open(f"{outpre}.seqconcord.txt", "w") as out:
        out.write(f"# total={len(all_seqs)} concordant={concordant} discordant={len(discordant)}\n")
        out.write("#seq\tprofile\t3model\n")
        for s, p, l in discordant:
            out.write(f"{s}\t{p}\t{l}\n")

    # --- 2. per-feature coordinate-identity rate ---
    ftr_match = 0
    ftr_mismatch = 0
    prof_only = 0
    lib3_only = 0
    mismatch_detail = []
    for s in all_seqs:
        pf_list = list(prof_feats.get(s, []))
        l3_list = list(lib3_feats.get(s, []))
        # match by (ftrtype, ftrname) with multiplicity; positional pairing
        # within same (ftrtype,ftrname) bucket, in file order
        pf_buckets = defaultdict(list)
        l3_buckets = defaultdict(list)
        for ftrtype, ftrname, seq_coords, mdl_coords in pf_list:
            pf_buckets[(ftrtype, ftrname)].append(seq_coords)
        for ftrtype, ftrname, seq_coords, mdl_coords in l3_list:
            l3_buckets[(ftrtype, ftrname)].append(seq_coords)
        keys = set(pf_buckets) | set(l3_buckets)
        for k in keys:
            pcoords = pf_buckets.get(k, [])
            lcoords = l3_buckets.get(k, [])
            n = min(len(pcoords), len(lcoords))
            for i in range(n):
                if pcoords[i] == lcoords[i]:
                    ftr_match += 1
                else:
                    ftr_mismatch += 1
                    mismatch_detail.append((s, k[0], k[1], pcoords[i], lcoords[i]))
            if len(pcoords) > n:
                prof_only += len(pcoords) - n
            if len(lcoords) > n:
                lib3_only += len(lcoords) - n

    with open(f"{outpre}.ftrconcord.txt", "w") as out:
        total_shared = ftr_match + ftr_mismatch
        rate = ftr_match / total_shared if total_shared else float("nan")
        out.write(f"# shared_features={total_shared} match={ftr_match} mismatch={ftr_mismatch} "
                  f"identity_rate={rate:.4f} profile_only={prof_only} lib3_only={lib3_only}\n")
        out.write("#seq\tftrtype\tftrname\tprofile_coords\tlib3_coords\n")
        for s, ftrtype, ftrname, pc, lc in mismatch_detail:
            out.write(f"{s}\t{ftrtype}\t{ftrname}\t{pc}\t{lc}\n")

    # --- 3. classification concordance ---
    class_concordant = 0
    class_total = 0
    class_discordant = []
    for s in all_seqs:
        if s not in prof_scn or s not in lib3_bestmdl:
            continue
        grp1, id1 = prof_scn[s]
        prof_clade = CLADE_OF_GRP.get(grp1, grp1)
        bmdl = lib3_bestmdl[s]
        lib3_clade = CLADE_OF_MDL.get(bmdl, bmdl)
        class_total += 1
        if prof_clade == lib3_clade:
            class_concordant += 1
        else:
            class_discordant.append((s, prof_clade, grp1, id1, lib3_clade, bmdl))

    with open(f"{outpre}.classconcord.txt", "w") as out:
        rate = class_concordant / class_total if class_total else float("nan")
        out.write(f"# total={class_total} concordant={class_concordant} rate={rate:.4f}\n")
        out.write("#seq\tprofile_clade\tprofile_grp1\tprofile_id1\tlib3_clade\tlib3_bestmdl\n")
        for row in class_discordant:
            out.write("\t".join(str(x) for x in row) + "\n")

    # --- headline to stdout ---
    print(f"PER-SEQUENCE: {len(all_seqs)} total, {concordant} concordant "
          f"({100.0*concordant/len(all_seqs):.2f}%), {len(discordant)} discordant")
    total_shared = ftr_match + ftr_mismatch
    rate = ftr_match / total_shared if total_shared else float("nan")
    print(f"PER-FEATURE: {total_shared} shared features, {ftr_match} match "
          f"({100.0*rate:.2f}%), {ftr_mismatch} mismatch, "
          f"profile_only={prof_only}, lib3_only={lib3_only}")
    rate = class_concordant / class_total if class_total else float("nan")
    print(f"CLASSIFICATION: {class_total} total, {class_concordant} concordant "
          f"({100.0*rate:.2f}%), {class_total - class_concordant} discordant")


if __name__ == "__main__":
    main()
