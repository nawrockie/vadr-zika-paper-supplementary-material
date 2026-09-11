#!/bin/bash
# Precise, single-threaded, single-node profile-vs-3model timing comparison.
# Fixes a noisier --cpu 4 --split, shared-node measurement from an earlier
# timing attempt.
#$ -N va117timing
#$ -o "<project-root>/timing-117/timing.out"
#$ -e "<project-root>/timing-117/timing.err"
#$ -cwd
#$ -V
#$ -j n
#$ -l h_rt=86400
#$ -m n
#$ -l excl=true
#$ -l m_mem_free=16G
#$ -l h_vmem=64G
#$ -l hostname=sge16*|sge17*

source $HOME/.bashrc
set -euo pipefail

RM="<project-root>/release-model"
WD081="<project-root>/profile-vs-3model-081"
LIB=$WD081/library
TIMING="<project-root>/timing-117"

DEVVADR="<devvadr-worktree-root>"
BE="<bio-easel-worktree-root>"
export VADRSCRIPTSDIR=$DEVVADR
export PERL5LIB="$BE/blib/lib:$BE/blib/arch:$DEVVADR:<sequip-root>:${PERL5LIB:-}"

MDIR=$RM/mdir-ere1.1-nnclass-test
SEQS=$TIMING/sample50.fa

echo "=== HOST INFO ==="
hostname
uptime
echo "--- qhost for this node ---"
qhost -h $(hostname -s) 2>&1 || qhost -h $(hostname) 2>&1 || true
echo "--- /proc/loadavg ---"
cat /proc/loadavg
echo ""

run_arm () {
  local label=$1
  local outbase=$2
  shift 2
  echo "=== RUN $label -> $outbase ==="
  rm -rf $TIMING/$outbase
  /usr/bin/time -v perl $DEVVADR/v-annotate.pl \
    -r --nosub --lowsim5ftr 15 --lowsim3ftr 15 \
    "$@" \
    $SEQS $TIMING/$outbase 2> $TIMING/$outbase.time.err
  echo "$label done, exit=$?"
}

# Replicate block structure: profile, 3model, 3model, profile  x3 = 6 runs/arm
# Block 1 = warm-up (discarded in warm-only analysis), blocks 2-3 = warm.
for block in 1 2 3; do
  echo "##### BLOCK $block: profile #####"
  run_arm "profile-b${block}a" "va-profile-b${block}a" \
    --r_file $MDIR/zikv-canonical.rpn.fa \
    --mkey zikv-canonical --mdir $MDIR

  echo "##### BLOCK $block: 3model (1st of pair) #####"
  run_arm "3model-b${block}a" "va-3model-b${block}a" \
    --mkey zikv-3model --mdir $LIB

  echo "##### BLOCK $block: 3model (2nd of pair) #####"
  run_arm "3model-b${block}b" "va-3model-b${block}b" \
    --mkey zikv-3model --mdir $LIB

  echo "##### BLOCK $block: profile (2nd of pair) #####"
  run_arm "profile-b${block}b" "va-profile-b${block}b" \
    --r_file $MDIR/zikv-canonical.rpn.fa \
    --mkey zikv-canonical --mdir $MDIR

  echo "--- load after block $block ---"
  cat /proc/loadavg
done

echo "=== ALL RUNS COMPLETE ==="
echo "--- final load ---"
uptime
