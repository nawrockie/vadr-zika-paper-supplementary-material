#!/bin/bash
#$ -N va-partial-2026-05-04
#$ -o <project-root>/release-model/validate-ere1.1/partial-seqs-2026-05-04/va-partial-2026-05-04.out
#$ -e <project-root>/release-model/validate-ere1.1/partial-seqs-2026-05-04/va-partial-2026-05-04.err
#$ -cwd
#$ -V
#$ -j n
#$ -l h_rt=86400
#$ -l h_vmem=64G
#$ -pe multicore 8
#$ -R y
#$ -m n

source $HOME/.bashrc
set -euo pipefail

# Released VADR 1.7.1 install.
VADRINSTALL="<vadr-1.7.1-install-root>"
export VADRSCRIPTSDIR=$VADRINSTALL/vadr
export PERL5LIB="$VADRINSTALL/vadr:$VADRINSTALL/sequip:${PERL5LIB:-}"

# Published vadr-models-zika-1.7.1-2 package, unpacked.
MDIR="<vadr-models-zika-1.7.1-2>"

OUTD=<project-root>/release-model/validate-ere1.1/partial-seqs-2026-05-04/va-partial-2026-05-04
rm -rf $OUTD     # v-annotate REFUSES to run if the outdir pre-exists

# Same released config as the locked full1254-bothlevers headline run
# (--lowsim5ftr 15 --lowsim3ftr 15, both levers), just retargeted at the
# non-full-length ("partial") sequence pool instead of the full-length
# 1254-seq test set. Expect a MUCH lower pass rate -- these sequences are
# deliberately shorter than the model's structural-completeness expectations.
#
# This is the exact command that produced the shipped result files
# (va-partial-2026-05-04.vadr.*): released VADR 1.7.1, the published
# vadr-models-zika-1.7.1-2 package.
perl $VADRSCRIPTSDIR/v-annotate.pl \
  --cpu 8 --split -r --keep --nosub --lowsim5ftr 15 --lowsim3ftr 15 \
  --r_file $MDIR/zika.rpn.fa \
  --mkey zika \
  --mdir $MDIR \
  "<project-root>/test-set-2026-05-04/zikv-partial-2026-05-04.fa" \
  $OUTD

echo "v-annotate partial-sequence 2026-05-04 validation done"
