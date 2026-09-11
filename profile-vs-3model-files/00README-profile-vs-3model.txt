# 00README-profile-vs-3model.txt
# Eric Nawrocki
# 2026-08-23
#
# This directory contains the files backing the paper's comparison of the
# single 8-sequence profile model against a library of three single-sequence
# models (one per clade: KY989511/ZA, MG807646/ZB.1, NC_035889/ZB.2),
# reported in Results as:
#
#   "the single profile model and the three-single-sequence-model library
#   agreed on the pass/fail verdict for 99.3% of sequences and on feature
#   coordinates for 99.96% of shared annotations, and on clade for 97.5%
#   ... the profile model ran about 5% faster."
#
# =====================================================================
#
# PART 1 -- AGREEMENT STATISTICS (pass/fail, feature coordinates, clade)
#
# Computed on the full 1254-sequence test set by compare.py, comparing the
# profile model's v-annotate.pl output against the 3-model library's:
#
#   result.seqconcord.txt   pass/fail agreement: 1245/1254 concordant
#                            (99.28%, rounds to the paper's 99.3%); the 9
#                            discordant sequences listed by accession
#   result.ftrconcord.txt   feature-coordinate agreement: 30987/31000 shared
#                            features match (identity_rate=0.9996, i.e.
#                            99.96%); every mismatch listed by accession/
#                            feature/both tools' coordinates
#   result.classconcord.txt clade-classification agreement: 1222/1254
#                            concordant (rate=0.9745, i.e. 97.5%); every
#                            discordant sequence listed with both libraries'
#                            clade call and %id
#
# compare.py is the script that produced these three files from:
#   profile.ftr / profile.pass.list / profile.fail.list   (profile-model run)
#   lib3.ftr / lib3.pass.list / lib3.fail.list             (3-model-library run)
# (both included below; usage is documented in compare.py's own header)
#
# =====================================================================
#
# PART 2 -- RUNTIME COMPARISON
#
# ** THIS IS THE ONE THING TO GET RIGHT WHEN REPRODUCING THIS RESULT. **
#
# The runtime figure is measured SEPARATELY from Part 1's concordance run --
# it does NOT come from a full-1254-sequence, multithreaded run (that kind of
# run exists elsewhere in this project's working files, is multithreaded and
# shares a cluster node with other jobs, and would not be a clean speed
# comparison). It comes instead from 12 single-threaded, back-to-back runs (2
# tools x 3 blocks x 2 sub-runs) on a 50-sequence clade-stratified subset (7
# African / 15 Asian / 28 American) on an EXCLUSIVE compute node, following
# the comparative-timing-shared-cluster methodology (repeated measurement to
# average out shared-cluster load noise that a single run cannot distinguish
# from a real speed difference).
#
# Files:
#   sample50.list, sample50.clades.tsv, sample50.fa
#                             the 50-sequence clade-stratified sample
#   run-timing-117.sh        the driver script for the 12 timed runs (SGE
#                             directives and internal paths redacted to
#                             placeholders, same convention as elsewhere in
#                             this package)
#   va-{profile,3model}-b{1,2,3}{a,b}.time.err
#                             12 files, GNU `time -v` output for each run
#                             ("User time (seconds)" is the field the ratio
#                             is computed from; the "Command being timed"
#                             line has had its internal paths redacted --
#                             every other line, including all timing/memory
#                             numbers, is untouched from the original run)
#   timing-ratios.tsv         per-block 3model/profile User-time ratio,
#                             computed directly from the 12 .time.err files
#                             above (added when this directory was packaged;
#                             no such summary file previously existed)
#
# Result: pairing each block's matching sub-run (b1a, b1b, b2a, b2b, b3a,
# b3b), the 3-model library used a median of 5.7% more User CPU time than
# the profile model (range across the 6 paired blocks: 5.3%-6.1% more),
# i.e. the profile model ran about 5-6% faster -- consistent with the
# paper's conservatively-rounded "about 5% faster".
#
# =====================================================================
#
# PART 3 -- MODEL DIRECTORIES
#
# Neither model directory is included in this package (large binary model
# files, same reasoning as the main package's mdir-ere1.1 -- see the
# top-level README for where the released profile model is hosted):
#   profile model: mdir-ere1.1-nnclass-test/ (the same release model used
#     throughout the rest of this package)
#   3-model library: a per-clade single-sequence model library built from
#     the three RefSeqs named above
#
# =====================================================================
#
# FILES IN THIS DIRECTORY
#
#   compare.py                    the concordance-comparison script (Part 1)
#   profile.ftr / profile.pass.list / profile.fail.list
#                                  profile-model v-annotate.pl output (input to compare.py)
#   lib3.ftr / lib3.pass.list / lib3.fail.list
#                                  3-model-library v-annotate.pl output (input to compare.py)
#   result.seqconcord.txt         output of compare.py (Part 1)
#   result.ftrconcord.txt         output of compare.py (Part 1)
#   result.classconcord.txt       output of compare.py (Part 1)
#   run-timing-117.sh             driver script for the 12 timed runs (Part 2)
#   sample50.list / sample50.clades.tsv / sample50.fa
#                                  the 50-sequence timing sample (Part 2)
#   va-{profile,3model}-b{1,2,3}{a,b}.time.err
#                                  12 GNU time -v output files (Part 2)
#   timing-ratios.tsv             per-block timing ratio summary (Part 2)
#
# =====================================================================
#
# RELEVANCE TO PAPER: the four run-comparison figures in the Results section
# (99.3% pass/fail agreement, 99.96% feature-coordinate agreement, 97.5%
# clade agreement, ~5% faster runtime), which motivate the paper's choice of
# a single profile model over a one-model-per-clade library.
#
# =====================================================================
# Questions/problems/feature requests? email eric.nawrocki@nih.gov
