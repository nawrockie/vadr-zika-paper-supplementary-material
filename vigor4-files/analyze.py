#!/usr/bin/env python3
# Analyze VADR-vs-VIGOR4 concordance from compare-two-ftrsums.pl output.
# Usage: analyze.py <compare.txt> <outprefix>
#   compare line types (arg1=VADR, arg2=VIGOR in compare-two-ftrsums.pl):
#     PRODUCT-COORDS-MATCH   seq:product coords: <vadr> <vigor>
#     PRODUCT-COORDS-MISMATCH seq:product coords: <vadr> <vigor>
#     PRODUCT-MISSING-2      seq:product coords1: <vadr>     (VADR-only)
#     PRODUCT-MISSING-1      seq:product coords2: <vigor>    (VIGOR-only)
import sys, re
from collections import defaultdict

compare_file, outpre = sys.argv[1], sys.argv[2]

def endpoints(coords):
    # coords may be 'a..b', 'a..>b', '<a..b', or multi-segment 'a..b,c..d'
    c = coords.replace('>', '').replace('<', '')
    segs = c.split(',')
    nums = []
    for s in segs:
        for tok in s.split('..'):
            tok = tok.strip()
            if tok != '':
                try: nums.append(int(tok))
                except ValueError: pass
    if not nums: return (None, None)
    return (nums[0], nums[-1])

# per (product): counts
prod_match=defaultdict(int); prod_mismatch=defaultdict(int)
prod_vadronly=defaultdict(int); prod_vigoronly=defaultdict(int)
# per (seq): lists
seq_match=defaultdict(int); seq_mismatch=defaultdict(int)
seq_vadronly=defaultdict(int); seq_vigoronly=defaultdict(int)
seqs=set()
mismatch_rows=[]  # (seq,product,vadr,vigor,dstart,dstop)
products=set()

with open(compare_file) as fh:
    for line in fh:
        line=line.rstrip('\n')
        if not line.strip(): continue
        f=line.split()
        tag=f[0]
        sp=f[1]
        seq, product = sp.split(':',1)
        seqs.add(seq); products.add(product)
        if tag=='PRODUCT-COORDS-MATCH':
            prod_match[product]+=1; seq_match[seq]+=1
        elif tag=='PRODUCT-COORDS-MISMATCH':
            prod_mismatch[product]+=1; seq_mismatch[seq]+=1
            # coords: <vadr> <vigor> are last two tokens
            vadr_c=f[-2]; vigor_c=f[-1]
            v0,v1=endpoints(vadr_c); g0,g1=endpoints(vigor_c)
            ds = (v0-g0) if (v0 is not None and g0 is not None) else None
            de = (v1-g1) if (v1 is not None and g1 is not None) else None
            mismatch_rows.append((seq,product,vadr_c,vigor_c,ds,de))
        elif tag=='PRODUCT-MISSING-2':
            prod_vadronly[product]+=1; seq_vadronly[seq]+=1
        elif tag=='PRODUCT-MISSING-1':
            prod_vigoronly[product]+=1; seq_vigoronly[seq]+=1
        else:
            sys.stderr.write("WARN unknown tag: %s\n"%tag)

# ---- per-product table ----
with open(outpre+'.per-product.tsv','w') as out:
    out.write("product\tn_vadr\tn_vigor\tn_both\tn_coords_match\tn_coords_mismatch\tn_vadr_only\tn_vigor_only\tpct_match_of_both\n")
    for p in sorted(products):
        m=prod_match[p]; mm=prod_mismatch[p]; vo=prod_vadronly[p]; go=prod_vigoronly[p]
        n_vadr=m+mm+vo; n_vigor=m+mm+go; both=m+mm
        pct = (100.0*m/both) if both>0 else float('nan')
        out.write("%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%.1f\n"%(p,n_vadr,n_vigor,both,m,mm,vo,go,pct))

# ---- per-sequence concordance ----
fully=0; partial_counts=defaultdict(int)
with open(outpre+'.per-seq.tsv','w') as out:
    out.write("seq\tn_shared\tn_match\tn_mismatch\tn_vadr_only\tn_vigor_only\tfully_concordant\n")
    for s in sorted(seqs):
        m=seq_match[s]; mm=seq_mismatch[s]; vo=seq_vadronly[s]; go=seq_vigoronly[s]
        shared=m+mm
        fc = (mm==0 and shared>0)
        if fc: fully+=1
        partial_counts[mm]+=1
        out.write("%s\t%d\t%d\t%d\t%d\t%d\t%s\n"%(s,shared,m,mm,vo,go,"yes" if fc else "no"))

# ---- mismatch offsets ----
with open(outpre+'.mismatch-offsets.tsv','w') as out:
    out.write("seq\tproduct\tvadr_coords\tvigor_coords\tdelta_start\tdelta_stop\n")
    for r in sorted(mismatch_rows):
        ds = '' if r[4] is None else r[4]
        de = '' if r[5] is None else r[5]
        out.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(r[0],r[1],r[2],r[3],ds,de))

# ---- headline summary ----
tot_match=sum(prod_match.values()); tot_mm=sum(prod_mismatch.values())
tot_vo=sum(prod_vadronly.values()); tot_go=sum(prod_vigoronly.values())
nseq=len(seqs)
with open(outpre+'.headline.txt','w') as out:
    out.write("=== Headline concordance (%d sequences) ===\n"%nseq)
    out.write("PRODUCT-COORDS-MATCH   (both, coords agree): %d\n"%tot_match)
    out.write("PRODUCT-COORDS-MISMATCH(both, coords differ): %d\n"%tot_mm)
    out.write("PRODUCT-MISSING-2      (VADR-only)          : %d\n"%tot_vo)
    out.write("PRODUCT-MISSING-1      (VIGOR-only)         : %d\n"%tot_go)
    both=tot_match+tot_mm
    out.write("\nShared features (both tools): %d\n"%both)
    if both>0:
        out.write("  coords-match rate among shared: %.2f%% (%d/%d)\n"%(100.0*tot_match/both,tot_match,both))
    out.write("\nFully-concordant sequences (all shared features coords-match): %d/%d (%.1f%%)\n"%(fully,nseq,100.0*fully/nseq if nseq else 0))
    out.write("\nDistribution of #coords-mismatch features per sequence:\n")
    for k in sorted(partial_counts):
        out.write("  %d mismatches: %d seqs\n"%(k,partial_counts[k]))
    # mismatch offset distribution
    if mismatch_rows:
        small=sum(1 for r in mismatch_rows if r[4] is not None and r[5] is not None and abs(r[4])<=3 and abs(r[5])<=3)
        out.write("\nMismatch boundary offsets: %d total; %d are |Δstart|<=3 AND |Δstop|<=3 (off-by-a-few-nt)\n"%(len(mismatch_rows),small))

print("wrote %s.{per-product,per-seq,mismatch-offsets,headline}.* "%outpre)
