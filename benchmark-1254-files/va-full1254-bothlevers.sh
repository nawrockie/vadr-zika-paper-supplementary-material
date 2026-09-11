#!/bin/bash
#$ -N va-full1254-bl
#$ -o <project-root>/release-model/validate-ere1.1/full1254-bothlevers/va-full1254-bothlevers.out
#$ -e <project-root>/release-model/validate-ere1.1/full1254-bothlevers/va-full1254-bothlevers.err
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

OUTD=<project-root>/release-model/validate-ere1.1/full1254-bothlevers/va-full1254-bothlevers
rm -rf $OUTD     # v-annotate REFUSES to run if the outdir pre-exists

# Settled release config = --lowsim5ftr 15 + --lowsim3ftr 15 (BOTH levers).
# NO --draw_r2dt (rendering add-on, no verdict effect).
#
# This is the exact command that produced the shipped result files
# (va-full1254-bothlevers.vadr.*): released VADR 1.7.1, the published
# vadr-models-zika-1.7.1-2 package.
perl $VADRSCRIPTSDIR/v-annotate.pl \
  --cpu 8 --split -r --keep --nosub --lowsim5ftr 15 --lowsim3ftr 15 \
  --r_file $MDIR/zika.rpn.fa \
  --mkey zika \
  --mdir $MDIR \
  "<project-root>/test-set-2026-05-04/zikv-test-2026-05-04.fa" \
  $OUTD

echo "v-annotate full-1254 ere-1.1 BOTH-LEVERS validation done"
