00README-seabra.txt
Eric Nawrocki

This subdirectory contains the clade-classification agreement check against the
Seabra et al. published clade labels.

seabra-clade-classification-754/ -- CLADE-CLASSIFICATION agreement check
   Compares the canonical 8-seq CM's classification (mkey/subgroup assignment)
   against Seabra's published African/Asian/American clade labels, for the
   754 sequences present in both label sets.
   Result: 754/754 = 100.00% agreement (see seabra_compare.out confusion
   matrix -- perfect recall in all three clades: african 7/7, asian 101/101,
   american 646/646).

   va-nnclass-test-760.vadr.scn is v-annotate.pl's classification output for
   the 760-sequence run. The paper's clade-classification table (Table 4) is
   derived entirely from this file. Relevant columns:
     'sub grp1'  / 'fract id1' -- best clade and % identity to the nearest
                                  training sequence ('seq1')
     'sub grp2'  / 'fract id2' -- second-best clade and its % identity
     'fid diff'                -- the margin, id1 minus id2, i.e. the gap to
                                  the nearest training sequence of a DIFFERENT
                                  clade (grp2 differs from grp1 in all 760 rows)
   Table 4 excludes training sequences as queries. Only 6 of the model's 8
   training sequences occur in this 760-sequence set (KY989511 and PQ551088 do
   not), so 760 - 6 = 754 rows remain, which is the table's N.

   Counting the .scn's clade calls over all 760 sequences gives 7 African /
   106 Asian / 647 American; removing those 6 training sequences leaves
   7 / 101 / 646 = 754, matching Table 4's per-clade rows.

   The per-clade accession lists are included alongside it:
     seabra.<clade>.list -- Seabra et al.'s published clade labels
                            (759 accessions in total)
     vadr.<clade>.list   -- VADR's clade grouping of the same accessions
   so the agreement can be checked directly by comparing the two sets.

RELEVANCE TO PAPER: the 100% (754/754) clade-classification agreement result,
which the paper reports in Results ("perfect agreement (754 of 754 classified
sequences, 100%)") and breaks down per clade in Table 4.

NOTE ON REPRODUCING: seabra_compare.py's hardcoded input paths point outside
this package, so the script cannot be re-run as shipped. It is included as a
record of how the comparison was performed, and its output,
seabra_compare.out, is included; the same 754/754 (7/101/646 by clade) result
can be verified independently from va-nnclass-test-760.vadr.scn and the clade
lists described above. These files were regenerated under released VADR 1.7.1
with the published vadr-models-zika-1.7.1-2 package ("zika", not
"zikv-canonical" -- same CM, renamed only); the 754/754 clade-classification
result reproduces exactly.

NOTE ON A PASS/FAIL DIFFERENCE (does not affect Table 4): one sequence,
MW165882.1, is FAIL in va-nnclass-test-760.vadr.scn under the published
package (fatal indf5gap/INDEFINITE_ANNOTATION_START at the ncRNA sfRNA1
feature's 5' boundary), where an earlier, pre-release-model vintage of this
file recorded it as PASS. Table 4 reports clade assignment only, not
pass/fail, and MW165882.1's clade call is unaffected -- this is unrelated to
the classification result above. The published package's zika.minfo also
redefines the ncRNA feature (from "Flavivirus 5' UTR (Rfam 14.10)" at 1..162
to "sfRNA1" at 10395..10807); this alert is a consequence of that change, not
a v-annotate.pl code difference.

NOTE ON SCOPE: an earlier annotation pass-rate run on this same 760-sequence
set was previously distributed with this package. It has been removed. It was
produced with a different, earlier model than the canonical 8-seq CM that every
other result in this package uses, and the paper does not report a pass rate for
this sequence set. The pass rate the paper does report is for the 1254-sequence
test set, and is documented in benchmark-1254-files/.
