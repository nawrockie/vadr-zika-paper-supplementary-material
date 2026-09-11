# 00README-vigor4.txt
# Eric Nawrocki
# 2026-08-23
#
# This file explains the contents of this directory, which contains the
# post-processed comparison of v-annotate.pl (VADR) and VIGOR4 annotations
# for the 981-sequence VIGOR4-comparable subset of the 1254-sequence test
# set (see top-level README for how the 981 relate to the 1254).
#
# =====================================================================
#
# WHAT THIS COMPARES
#
# 981 of the 1254 full-length test-set sequences (those with no run of 20
# or more consecutive ambiguous nucleotides -- VIGOR4 treats a longer run
# as a sequencing gap and splits the gene model spanning it) were annotated
# by both v-annotate.pl (mdir-ere1.1, the released "both levers"
# configuration -- see ../benchmark-1254-files/00README-benchmark-1254.txt)
# and VIGOR4 v4.1 (`vigor4 -i input.fa -o output -d zikv_db
# --overwrite-output`), and the two sets of CDS/mat_peptide feature
# coordinates were compared.
#
# RELEVANCE TO PAPER: the 974/981 (99.3%) fully-concordant-sequence figure,
# the 99.97% (11,709/11,712) shared-feature coordinate-match rate, and the
# "added value" panel of features VADR reports that VIGOR4's model does not.
#
# ⚠ KNOWN DISCREPANCY (2026-09-10, found when regenerating this arm under
# released VADR 1.7.1 + the published vadr-models-zika-1.7.1-2 package): the
# 974/981, 11,709/11,712, and 3-mismatch figures above all reproduce exactly
# (see va981.headline.txt), but the manuscript's "12,257 [VADR-only features]
# in total" figure (zika-article.tex, Results, "Comparing with VIGOR4") does
# NOT reproduce. Recount under the published package: 12,168 (3 extra
# mat_peptides x 981 = 2943, + 8336 stem_loop, + 889 ncRNA = 12168; the
# archived 12,257 used 978 ncRNA calls, not 889). The published package's
# zika.minfo redefines the ncRNA feature from "Flavivirus 5' UTR (Rfam
# 14.10)" at 1..162 to "sfRNA1" at 10395..10807; 92 of the 981 sequences that
# had an ncRNA call under the old 5'-UTR definition get no ncRNA call at all
# under the new sfRNA1 definition (3 sequences gained one), a net -89. This
# does not touch any CDS/mat_peptide comparison number (vadr-ftr-to-ftrsum.pl
# filters to CDS/mat_peptide only) or any pass/fail verdict. EPN's call on
# whether to update the manuscript's "12,257" to "12,168" -- NOT changed here
# per this brief's scope (no manuscript edits).
#
# =====================================================================
#
# HOW THE FOUR SCRIPTS CHAIN
#
# The four scripts in this directory form a fixed pipeline, run in this
# order (also documented in the top-level README-processing-test-results.txt
# step 2, which additionally covers how the 981-sequence VADR and VIGOR4
# inputs were assembled from two source runs each -- NOT reproducible from
# a single command; read that step before trying to rerun this from scratch):
#
#   1. vadr-ftr-to-ftrsum.pl <VADR .ftr output, 981-seq subset>
#        > va981.vadr.ftrsum
#      Converts VADR's per-feature .ftr output into a compact per-product
#      coordinate summary ("ftrsum"). Requires the 26-column .ftr row
#      format VADR emits (perl vadr-ftr-to-ftrsum.pl with no arguments
#      prints usage).
#
#   2. vigor-pep-to-ftrsum.pl <VIGOR4 .pep output, 981-seq subset>
#        > va981.vigor.ftrsum
#      Parses VIGOR4's .pep FASTA-header coordinate fields (location=...,
#      product=...) into the same ftrsum format as step 1, applying a
#      product-name synonym table (e.g. VIGOR4's "small_envelope_protein_M"
#      -> VADR's "membrane_glycoprotein_M") so the two tools' feature names
#      line up.
#
#   3. compare-two-ftrsums.pl va981.vadr.ftrsum va981.vigor.ftrsum
#        > va981.compare.txt
#      Pairs the two ftrsum files by sequence+product and emits one line per
#      pairing: PRODUCT-COORDS-MATCH, PRODUCT-COORDS-MISMATCH,
#      PRODUCT-MISSING-1 (VIGOR-only) or PRODUCT-MISSING-2 (VADR-only).
#      va981.compare.txt (1.2 MB) is included in this directory.
#
#   4. analyze.py va981.compare.txt va981
#      Reads va981.compare.txt and writes six summary files, all sharing the
#      "va981." prefix and all included in this directory:
#        va981.headline.txt               overall concordance counts (Table/
#                                          Results headline figures)
#        va981.per-seq.tsv                per-sequence match/mismatch counts
#        va981.per-product.tsv            per-product (CDS/mat_peptide) match
#                                          rates
#        va981.disagreement-categories.txt  the six-category breakdown of
#                                          every disagreement (boundary
#                                          shifts, scope differences, the
#                                          VIGOR4 pseudogene-refusal case,
#                                          etc.)
#        va981.mismatch-offsets.tsv       the 3 coordinate mismatches, with
#                                          |Δstart|/|Δstop|
#        va981.added-value-panel.txt      features/QC VADR reports that
#                                          VIGOR4's zikv_db model does not
#                                          (extra mat_peptides, stem_loops,
#                                          the ncRNA feature, and pass/fail
#                                          QC status)
#
# NOTE: va981.disagreement-categories.txt and va981.added-value-panel.txt as
# shipped carry more narrative detail (e.g. the 848+133 batch provenance,
# the PASS/FAIL QC breakdown) than analyze.py alone produces from
# va981.compare.txt -- some of that detail was added by hand from the
# underlying VADR .alc/.sqa output when the files were prepared. Treat these
# two files as an annotated report built on top of analyze.py's raw output,
# not as byte-for-byte re-derivable from a single script invocation; the
# .tsv/.txt files without added narrative (headline, per-seq, per-product,
# mismatch-offsets) ARE the direct output of analyze.py step 4.
#
# =====================================================================
#
# FILES IN THIS DIRECTORY
#
#   analyze.py                         script (step 4 above)
#   vadr-ftr-to-ftrsum.pl               script (step 1 above)
#   vigor-pep-to-ftrsum.pl              script (step 2 above)
#   compare-two-ftrsums.pl              script (step 3 above)
#   va981.compare.txt                  output of step 3 (input to step 4)
#   va981.headline.txt                 output of step 4
#   va981.per-seq.tsv                  output of step 4
#   va981.per-product.tsv              output of step 4
#   va981.disagreement-categories.txt  output of step 4, hand-annotated (see NOTE above)
#   va981.mismatch-offsets.tsv         output of step 4
#   va981.added-value-panel.txt        output of step 4, hand-annotated (see NOTE above)
#
# NOT included (large, primary tool output rather than summary product):
#   the 981-sequence VADR .ftr file and the VIGOR4 .pep files themselves
#   (inputs to steps 1-2). VADR's .ftr output can be regenerated by rerunning
#   the command in ../benchmark-1254-files/00README-benchmark-1254.txt and
#   filtering to the 981-sequence subset (see top-level walkthrough step 2
#   for the exact filtering criterion). VIGOR4's .pep output requires a
#   VIGOR4 v4.1 installation and its zikv_db reference database, which the
#   reader may not have; this is a legitimate reproducibility limit, not an
#   omission (the comparison inputs/outputs above let the comparison be
#   checked without rerunning VIGOR4).
#
# =====================================================================
# Questions/problems/feature requests? email eric.nawrocki@nih.gov
