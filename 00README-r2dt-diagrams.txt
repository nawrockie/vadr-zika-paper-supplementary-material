# 00README.txt
#
# R2DT secondary-structure diagram supplement for the Zika virus VADR paper.
#
# =====================================================================
#
# WHAT THIS IS
#
# This directory contains R2DT-drawn secondary-structure SVG diagrams for
# every sequence in the paper's headline full-length annotation benchmark
# (1254 Zika virus sequences; 1219 pass / 35 fail VADR's --alerts checks).
# Two diagrams are drawn per sequence, one per genome template layout:
#
#   <ACCESSION>-zika-linear.svg      linear-genome-layout template
#   <ACCESSION>-zika-circular.svg    circular-genome-layout template
#
# All 2504 SVGs (1254 linear + 1250 circular) are in r2dt-svgs/.
#
# WHY THE LINEAR AND CIRCULAR COUNTS DIFFER (1254 vs 1250)
#
# Every one of the 1254 input sequences gets a linear diagram. A circular
# diagram is only drawn when the sequence's covered range overlaps the
# circular template's declared range; 4 of the 1254 sequences do not, so
# only 1250 circular diagrams exist. This is not missing data -- it is
# expected given the input sequences, most of which are shorter than a
# complete Zika genome.
#
# EXACT COMMAND AND VERSIONS
#
# Produced with VADR v1.7.1 (https://github.com/ncbi/vadr, tag vadr-1.7.1;
# built from commit 4fb6192 shortly before tagging -- its annotation and
# drawing code is identical to the released tag, differing only in
# version/date strings). The command was run using the model key
# zikv-canonical (--mkey zikv-canonical below), the working name for the
# model package shipped as vadr-models-zika-1.7.1-2 on the VADR FTP site
# (https://ftp.ncbi.nlm.nih.gov/pub/nawrocki/vadr-models/):
#
#   export VADRSCRIPTSDIR=<path-to-vadr-develop-checkout>
#   export PERL5LIB=$VADRSCRIPTSDIR:<path-to-sequip-checkout>
#   export R2DT_DIR=<path-to-stock-R2DT-checkout>
#   perl $VADRSCRIPTSDIR/v-annotate.pl \
#     --cpu 4 --split --keep --draw_r2dt \
#     -r --r_file <mdir>/zikv-canonical.rpn.fa --nosub \
#     --lowsim5ftr 15 --lowsim3ftr 15 \
#     --mkey zikv-canonical --mdir <mdir> \
#     <1254-sequence-input.fa> <outdir>
#
# R2DT: stock (unmodified) checkout, commit 947f0842 ("Trivial commit to
#   trigger a build for testing", branch bump-pillow-py3.13, fork of
#   r2dt-bio/R2DT). This is a plain, unpatched R2DT install -- it carries
#   none of this project's temporary Zika-specific numbering workarounds
#   used to produce the paper's own figures.
#
# Both linear and circular numbering ticks are in SUBMITTED-SEQUENCE
# coordinates (i.e. position 1 is the first base of the submitted
# GenBank/RefSeq record), not template-fragment-offset coordinates.
#
# Each template covers two non-contiguous regions of the genome, near the
# 5' and 3' ends, and omits the long stretch between them. Where a
# sequence's drawn residues cross from one of those regions into the
# other, a "//" break marker is drawn, labeled with the number of the
# sequence's own nucleotides that were omitted at that point. A sequence
# that reaches both regions therefore carries a marker; one whose covered
# range lies entirely within a single region carries none.
#
# The omitted-nucleotide count is computed per sequence, not per template,
# so it varies between records. On the linear template most complete
# genomes give 10,169 nt, with values ranging from 10,085 to 10,169; on
# the circular template the most common value is 10,475. The variation
# reflects real length differences between isolates in the omitted region.
#
# Of the 1254 linear diagrams, 1109 carry a break marker and 145 do not;
# of the 1250 circular diagrams, 793 carry one and 457 do not. The
# circular template's two regions are narrower, so more sequences reach
# only one of them.
#
# NAMING CONVENTION
#
# <ACCESSION>-zika-linear.svg
# <ACCESSION>-zika-circular.svg
#
# where <ACCESSION> is the GenBank/RefSeq accession.version from the input
# FASTA header (e.g. NC_035889.1, KX879604.1).
#
# =====================================================================
