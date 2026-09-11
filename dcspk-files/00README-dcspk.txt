00README-dcspk.txt
Eric Nawrocki

This subdirectory contains ONLY the DCS-PK Rfam SEED alignment -- not the
full Rfamseq search-hit dump, which is not needed for the SEED alignment
claim (see below).

  SEED   Stockholm-format seed alignment underlying the Rfam family submission
         Flavivirus_DCS-PK (accession RF04381): a 19-sequence, 14-species
         cross-flavivirus alignment of the downstream conserved secondary
         structure/pseudoknot element. This matches the sequence count stated
         in the manuscript.
         Updated 2026-08-12 (was a 17-sequence alignment): the family grew
         17 -> 20 at the 2026-08-07 re-curation, then 20 -> 19 when
         NC_006551.1 (Usutu) was removed for being byte-identical to
         NC_000943.1 (Murray Valley encephalitis) across every alignment
         column. Usutu remains represented by OR141535.3, so the species
         count is unchanged.
         md5 d033e4e6ce7ea39c04b47edc97253806.

NOT included (out of scope, multi-MB search-hit dumps):
  outlist, species, revoutlist, seedoutlist -- Rfamseq search-hit output from
  the rfsearch.pl run that produced this family; not needed for the SEED
  alignment claim.

NOT included (available elsewhere, not duplicated here):
  DESC -- the Rfam family description file. Will be publicly available on
  the Rfam website (rfam.org/family/RF04381) once the family is released.
  Thresholds there are GA/TC/NC 38.00/41.30/34.70; TC and NC are locally
  derived pending EBI's re-curation of the 19-sequence family.

RELEVANCE TO PAPER: the DCS-PK Rfam-submission claim (the 19-seq SEED
alignment underlying the RF04381/Flavivirus_DCS-PK family).
