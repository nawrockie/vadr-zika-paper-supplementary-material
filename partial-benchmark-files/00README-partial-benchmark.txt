# 00README-partial-benchmark.txt
# Eric Nawrocki
# 2026-08-23
#
# This directory contains the files backing the paper's partial-sequence
# benchmark, reported in Results as:
#
#   "...and on the set of 1026 partial sequences they were 1013 pass and 13
#   fail (98.73%)."
#
# and the follow-up paragraph characterizing the 13 failures (5 genuine
# defects, 7 correctly-annotated legitimate partial sequences, 1 borderline
# case, AY326412).
#
# =====================================================================
#
# HOW THE 1026-SEQUENCE PARTIAL POOL WAS DEFINED
#
# Starting from the same 2477-sequence GenBank pull used for the full-length
# 1254-sequence benchmark (same 2026-05-04 date; no separate re-fetch from
# NCBI), everything BELOW the existing 10,267 nt "complete genome" cutoff
# (95% of RefSeq NC_035889's 10,808 nt length -- the same per-virus empirical
# "complete genome" threshold used to define the full-length set) was pooled,
# then 10 non-genuine PDB crystal-structure "Chain" records were excluded
# (caught by their non-standard accession format), leaving 1026. No
# additional universal length floor (e.g. a minimum-nt cutoff) was applied.
# The full derivation table, including intermediate record counts and a
# length-bin breakdown of the final 1026-sequence pool, is in
# funnel-partial.txt.
#
# =====================================================================
#
# THE V-ANNOTATE.PL RUN
#
# Same released "both levers" configuration as benchmark-1254-files/ (see
# ../benchmark-1254-files/00README-benchmark-1254.txt), applied to the
# 1026-sequence partial pool instead of the full-length 1254-sequence set.
# This is the exact command that produced the files shipped below: released
# VADR 1.7.1, the published vadr-models-zika-1.7.1-2 package.
#
#   perl v-annotate.pl --cpu 8 --split -r --keep --nosub --lowsim5ftr 15 \
#     --lowsim3ftr 15 --r_file <package>/zika.rpn.fa \
#     --mkey zika --mdir <package> \
#     zikv-partial-2026-05-04.fa <outdir>
#
#   CM: ere-1.1 (the same "both levers" release configuration used
#   throughout this package).
#   mdir: the published vadr-models-zika-1.7.1-2 package (see top-level
#   README for where to obtain it).
#
#   va-partial-2026-05-04.sh documents this command (with internal paths
#   redacted to placeholders, same convention as elsewhere in this package).
#
# =====================================================================
#
# THE 13 FAILURES
#
# The headline number (1013 pass / 13 fail) is a direct, mechanical count
# from the .vadr.pass.list and .vadr.fail.list files below, and can be
# reproduced by anyone by counting lines in those files or re-running the
# command above.
#
# The Results-section characterization of the 13 failures -- 5 genuine
# defects, 7 legitimate partial sequences that VADR is being conservatively
# strict on, and 1 borderline case (AY326412.1) -- is NOT a mechanical
# derivation from the .vadr.alt/.vadr.alc alert-code files alone. It is a
# manual assessment: distinguishing "genuine defect" from "correctly-flagged
# legitimate partial sequence" required inspecting each sequence's alert
# detail individually (in several cases, examining the underlying blastx HSP
# alignment behavior beyond what the alert code itself states) rather than
# reading off a single mechanical rule from the alert codes. It is included
# here as EPN's assessment, not as something a reader can independently
# re-derive from the alert codes alone.
#
# The alert code(s) triggered by each of the 13 failing accessions (readable
# directly from va-partial-2026-05-04.vadr.alt, included below) are:
#
#   accession     alert code(s)                          assessment
#   -----------   -------------------------------------  --------------------
#   KF383120.1    cdsstopn, cdsstopp, fsthicfi, peptrans  genuine defect
#   LR792671.1    cdsstopp, fsthicfi, fsthicft,           genuine defect
#                 indf3pst, indf5pst, peptrans
#   MH306202.1    fsthicfi, peptrans                      genuine defect
#   MK028862.1    deletinn, deletinp, fstlocfi,           genuine defect
#                 indf3pst, lowsimic, peptrans
#   MT478034.1    deletinn, fstlocfi, indf3pst,           genuine defect
#                 lowsimic, peptrans
#   KY561344.1    indf3pst, peptrans                      legitimate partial
#   KY765304.1    indf5pst, peptrans                      legitimate partial
#   MK216746.1    indf3pst, peptrans                      legitimate partial
#   MT482106.1    ambgnt5f, indf5lcn                       legitimate partial
#   MN938894.1    lowcovrg, lowsim3c                      legitimate partial
#   MN938899.1    lowcovrg                                legitimate partial
#   MN938900.1    lowcovrg                                legitimate partial
#   AY326412.1    indf3gap, indf3lcc, indf5gap,           borderline
#                 indf5lcn, lowcovrg, lowsimil
#
#   Totals: 5 genuine defect / 7 legitimate partial / 1 borderline, matching
#   the paper's 5/7/1 characterization.
#
# =====================================================================
#
# FILES IN THIS DIRECTORY
#
#   va-partial-2026-05-04.sh          documented v-annotate.pl command
#   va-partial-2026-05-04.vadr.alc    alert code summary (counts per alert type)
#   va-partial-2026-05-04.vadr.alt    per-sequence/feature alert instance listing
#                                      (source of the alert-code table above)
#   va-partial-2026-05-04.vadr.pass.list   1013 accessions that passed
#   va-partial-2026-05-04.vadr.fail.list   13 accessions that failed
#   va-partial-2026-05-04.vadr.sqa    per-sequence annotation summary
#   zikv-partial-2026-05-04.list      the 1026 accessions making up the
#                                      partial-sequence pool, one per line
#   funnel-partial.txt                the derivation of the 1026-sequence
#                                      pool from the source GenBank pull
#
# NOTE: va-partial-2026-05-04.vadr.ftr (feature-level per-sequence detail) is
# NOT included here, for the same package-size reason as
# benchmark-1254-files/ -- it is not needed to reproduce the headline
# pass/fail counts and can be regenerated by re-running the command above.
#
# =====================================================================
#
# RELEVANCE TO PAPER: the 1013/1026=98.73% partial-sequence headline figure
# and the accompanying 5/7/1 failure-mode characterization, both in the
# Results section.
#
# =====================================================================
# Questions/problems/feature requests? email eric.nawrocki@nih.gov
