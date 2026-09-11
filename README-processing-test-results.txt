EPN, 2026-07-01

README-processing-test-results.txt

Notes on reproducing the four empirical results presented in the paper
"Zika virus sequence and secondary structure analysis using VADR"
(the locked headline annotation benchmark, the VIGOR4 comparison, the Seabra
et al. confirmatory results, and the DCS-PK Rfam SEED alignment).

(Lines of this file that are commands are prefixed with '$')

-------------
VERSIONS: these results were produced with released VADR v1.7.1
(https://github.com/ncbi/vadr, tag vadr-1.7.1), using the published model
packages vadr-models-zika-1.7.1-2 and vadr-models-flavi-1.7-2 (VADR FTP site,
https://ftp.ncbi.nlm.nih.gov/pub/nawrocki/vadr-models/). The commands below
are the exact commands used.

Step 3 (timing) is NOT reproducible and was deliberately not re-run: it
measures wall-clock on a shared, heterogeneous cluster.
-------------
To reproduce the data presented in the paper that corresponds to these four
results, perform steps 1-4 below. The RELEVANCE TO PAPER section in each step
explains its relevance to the data/claims presented in the paper. Because the
paper's table numbering is not yet finalized, each step cites the specific
claim/number rather than a table number.

----------------------------------------------------------------------

1. Reproduce the locked headline annotation benchmark (1219 pass / 35 fail
   out of 1254 = 97.21%).

   The documented v-annotate.pl command, which is the exact command that
   produced the shipped result files (see also
   benchmark-1254-files/va-full1254-bothlevers.sh):

$ perl v-annotate.pl --cpu 8 --split -r --keep --nosub --lowsim5ftr 15 --lowsim3ftr 15 \
    --r_file <package>/zika.rpn.fa --mkey zika \
    --mdir <package> zikv-test-2026-05-04.fa <outdir>

   This "both levers" config (--lowsim5ftr 15 AND --lowsim3ftr 15, on top of
   the ere-1.1 CM) was locked in as the release configuration after comparing
   it against single-lever and no-lever alternatives on this same test set.

   The 1254-sequence test-set FASTA file (zikv-test-2026-05-04.fa) is NOT
   included in this package (it is a large sequence file, not a small
   summary/analysis product). It can be regenerated from GenBank by fetching
   the 1254 accessions listed in
   benchmark-1254-files/zikv-test-2026-05-04.list (one accession per line,
   e.g. via NCBI edirect efetch; that list IS included in this package). The
   published vadr-models-zika-1.7.1-2 package used for --mdir is available
   from the VADR FTP site (see VERSIONS above).

   RELEVANCE TO PAPER: the locked headline 1219/35/1254=97.21% accuracy
   figure, and the residual 35-sequence failure-mode table (see
   benchmark-1254-files/00README-benchmark-1254.txt and the .vadr.alc file
   for the alert-type breakdown of the 35 failures).

----------------------------------------------------------------------

2. Reproduce the VIGOR4 comparison (974/981=99.3% fully-concordant sequences;
   99.97% coords-match rate among shared features).

   VADR annotations for this comparison are not from a separate run: they
   are the 981-sequence subset of the same full-1254-sequence v-annotate.pl
   run described in Step 1 above (same command, same both-levers config),
   filtered down to the 981 sequences of the 1254
   test set that contain no run of 20 or more consecutive ambiguous
   nucleotides. That is the selection criterion the paper uses and explains:
   VIGOR4 treats a run of that length as a sequencing gap and splits the
   affected gene model into independently scored fragments, which would
   otherwise distort the comparison.

   VIGOR4 was run separately (VIGOR4 run output is not included here; only
   the post-processed comparison summaries are), in two batches: 848 of the
   981 sequences were annotated in an earlier VIGOR4 run, and the remaining
   133 sequences (the ambiguous-run-rescued set) were annotated in a later,
   separate VIGOR4 run. VIGOR4 declined to produce any gene model at all for
   5 of those 133 sequences (they carry in-frame stop codons, and VIGOR4
   does not support pseudogene annotation), so those 5 sequences contribute
   zero shared features to the comparison and cannot be fully concordant.

   The comparison itself was generated with the same pipeline as before,
   applied to the merged 981-sequence inputs:

$ perl vadr-ftr-to-ftrsum.pl  <vadr .ftr output, 981-seq subset>  > va981.vadr.ftrsum
$ perl vigor-pep-to-ftrsum.pl <vigor .pep output, 981-seq subset> > va981.vigor.ftrsum
$ perl compare-two-ftrsums.pl va981.vadr.ftrsum va981.vigor.ftrsum > va981.compare.txt
$ python3 analyze.py va981.compare.txt   # produces va981.headline.txt,
                                          # va981.per-seq.tsv, va981.per-product.tsv,
                                          # va981.disagreement-categories.txt,
                                          # va981.mismatch-offsets.tsv,
                                          # va981.added-value-panel.txt

   (exact analyze.py invocation/options may need adjusting; see the script's
   argument parsing for details -- this is a reconstruction of the pipeline
   from the summary files present, not a verbatim transcript of the original
   interactive session.)

   NOTE ON REPRODUCIBILITY: the two steps that assemble the 981-sequence
   inputs above -- filtering the full-1254 VADR .ftr output down to the 981
   accessions, and combining the two VIGOR4 batches (848 + 133) into a
   single 981-sequence .vigor.ftrsum -- were run as one-off commands at the
   time and were not preserved as standalone scripts. Rather than guess at
   them, we are not reconstructing an exact command for that specific step;
   the inputs and outputs of each step are described above precisely enough
   to redo the filtering/merging in any scripting language. There is
   therefore no single script analogous to the earlier 848-sequence
   version's run script for reproducing the 981-sequence VADR/VIGOR4 inputs
   end to end.

   RELEVANCE TO PAPER: the 974/981 (99.3%) fully-concordant-sequence figure,
   the 99.97% (11,709/11,712) shared-feature coords-match rate, and the VADR
   "added value" panel (extra features/annotations VADR provides beyond
   VIGOR4's output).

----------------------------------------------------------------------

3. Reproduce the Seabra et al. clade-classification agreement (754/754=100%).

   The classification assigns each sequence to the clade of its nearest
   neighbor among the model's training sequences, and that assignment is
   compared against Seabra et al.'s published clade labels at the
   ZA/ZB.1/ZB.2 level.

   The per-sequence classification output for the 760-sequence set is
   included as seabra-files/seabra-clade-classification-754/
   va-nnclass-test-760.vadr.scn. This is the file Table 4's per-clade
   agreement and margin statistics were computed from; its 'subgrp1',
   'fract id1' and 'fid diff' columns hold the clade call, the identity to
   the nearest training sequence, and the margin to the nearest training
   sequence of a different clade.

   Counting the .scn's clade calls gives 7 African / 106 Asian / 647
   American across all 760 sequences. Excluding the six of the eight
   training sequences that occur in this set (they cannot serve as their own
   nearest neighbors) leaves 754 queries, distributed 7 / 101 / 646 -- which
   is the agreement the paper reports, and matches the per-clade rows of
   Table 4.

   Seabra et al.'s own published clade lists are included alongside it
   (seabra.african.list, seabra.asian.list, seabra.american.list; 759
   accessions in total), together with the corresponding VADR assignments
   (vadr.african.list, vadr.asian.list, vadr.american.list), so the
   agreement can be checked directly by comparing the two sets.

$ python3 seabra_compare.py   # regenerates seabra_compare.out

   (NOTE: seabra_compare.py is included as a record of how the comparison
   was performed, but its input paths point outside this package, so it
   cannot be re-run as shipped. The result it produced is included as
   seabra_compare.out, and the same counts can be derived independently
   from the .scn file and the clade lists described above.)

   RELEVANCE TO PAPER: the 100% (754/754) clade-classification agreement
   figure, which the paper reports in Results ("perfect agreement (754 of
   754 classified sequences, 100%)") and breaks down per clade in Table 4.

----------------------------------------------------------------------

4. DCS-PK Rfam SEED alignment (not a "reproduce" step -- this is an input
   artifact, not pipeline output).

   dcspk-files/SEED is the 19-sequence Stockholm-format seed alignment
   underlying the Rfam family submission Flavivirus_DCS-PK (Rfam accession
   RF04381), a cross-flavivirus alignment of a downstream conserved
   secondary-structure/pseudoknot element. The full family (SEED alignment,
   consensus CM, DESC description file, and Rfamseq search hits) will be
   publicly browsable at rfam.org/family/RF04381 once the family is released
   by Rfam curators; only the SEED alignment itself is included in this
   package (see dcspk-files/00README-dcspk.txt for what was deliberately
   excluded and why).

   RELEVANCE TO PAPER: the DCS-PK Rfam-submission claim.

----------------------------------------
Questions? email eric.nawrocki@nih.gov
----------------------------------------
