# 00README.txt
# Eric Nawrocki
# 2026-08-23
#
# This directory contains supplementary data for the paper
# "Zika virus sequence and secondary structure analysis using VADR"
# covering six empirical results referenced in the Results section.
#
# =====================================================================
#
# VERSIONS
#
# The results in this package were produced with released VADR v1.7.1
# (https://github.com/ncbi/vadr, tag vadr-1.7.1) and the published model
# packages vadr-models-zika-1.7.1-2 and vadr-models-flavi-1.7-2, both
# available from the VADR FTP site
# (https://ftp.ncbi.nlm.nih.gov/pub/nawrocki/vadr-models/). The run scripts
# in the subdirectories below document these exact commands.
#
# TIMING RESULTS ARE NOT REPRODUCIBLE and were deliberately not re-run.
# The wall-clock figures in profile-vs-3model-files/ were measured on a
# shared, heterogeneous compute cluster, where repeat runs of the same
# command differ for reasons unrelated to the software.
#
# =====================================================================
#
# There are six subdirectories in this directory, one per result:
#
# benchmark-1254-files/       the locked headline annotation benchmark
#                              (1219 pass / 35 fail out of 1254 = 97.21%)
# partial-benchmark-files/    the partial-sequence benchmark
#                              (1013 pass / 13 fail out of 1026 = 98.73%)
# vigor4-files/                the VIGOR4 comparison
#                              (974/981=99.3% fully-concordant sequences;
#                               99.97% coords-match rate among shared features)
# profile-vs-3model-files/    the single-profile-model vs three-single-
#                              sequence-model-library comparison (99.3%
#                              pass/fail agreement, 99.96% feature-coordinate
#                              agreement, 97.5% clade agreement, ~5% faster
#                              runtime)
# seabra-files/                the Seabra et al. clade-classification agreement
#                              (754/754=100%)
# dcspk-files/                 the DCS-PK Rfam SEED alignment (RF04381,
#                              SEED alignment only, per scope decision)
#
# Each subdirectory includes its own 00README-*.txt explaining its files
# and any files deliberately excluded (and why).
#
# See README-processing-test-results.txt for step-by-step instructions
# to reproduce each result, with an explicit "RELEVANCE TO PAPER"
# annotation per step tying it to the specific claim/number it backs.
#
# Each section's exact run script(s) live inside that section's own
# subdirectory (e.g. benchmark-1254-files/va-full1254-bothlevers.sh) rather
# than a shared top-level scripts/ dir, since none of the six results share
# a script with another.
#
# make-tarball.sh builds the submission tarball of this whole directory.
# Run it from the PARENT of this directory (`sh make-tarball.sh` one level
# up), never from inside it -- running it from inside leaves a stray archive
# that a second run will sweep into itself.
#
# =====================================================================
#
# WHICH DIRECTORY BACKS WHICH TABLE
#
# The paper's four tables and the Results-text quantitative claims do not
# map one-to-one onto the six subdirectories above (a subdirectory can feed
# more than one table, and some Results numbers are covered by no table at
# all). This map is the authoritative cross-reference:
#
#   Table 1 (resource components)
#     -- pass rate figure: benchmark-1254-files/
#     -- Seabra agreement figure: seabra-files/
#     -- RF04381 GA/TC/NC: dcspk-files/
#   Table 2 (training sequences)
#     -- the 8 accessions are printed in the table itself; no separate
#        list is shipped. Country/year/length are read directly from the
#        GenBank record of each accession (public, no local data needed).
#   Table 3 (residual failures, 35 of 1254)
#     -- benchmark-1254-files/ (the .vadr.alc/.vadr.alt files back every
#        row and every accession in this table)
#   Table 4 (Seabra clade-classification agreement)
#     -- seabra-files/
#
#   Results-text claims NOT tied to a numbered table:
#     -- the partial-sequence benchmark (1013/1026, 98.73%, plus the
#        5 genuine / 7 legitimate-partial / 1 borderline breakdown of the
#        13 failures): partial-benchmark-files/
#     -- VIGOR4 comparison (974/981, 99.97% shared-feature coords-match):
#        vigor4-files/
#     -- single-profile-model vs three-single-sequence-model-library
#        comparison (99.3% pass/fail agreement, 99.96% feature-coordinate
#        agreement, 97.5% clade agreement, ~5% faster runtime):
#        profile-vs-3model-files/
#     -- DCS-PK seed alignment / RF04381 submission: dcspk-files/
#
#   Results-text claims WITH NO SHIPPED DATA in this package (internal audit,
#   contact the corresponding author for detail; source data exists on EPN's
#   own systems and could be packaged in a future revision):
#     -- the whole-genome cross-Rfam-family search (8 of 10 structural
#        elements recovered, with E-values)
#
# =====================================================================
# Questions/problems/feature requests? email eric.nawrocki@nih.gov
