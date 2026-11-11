## Supplementary material for *Zika virus sequence and secondary structure analysis using VADR*, submitted September 2026

The files in this repository are also packaged as two gzipped tarballs, for
convenience.

`vadr-zika-paper-supplementary-material.tar.gz` contains the scripts and data
underlying the annotation benchmark, the VIGOR4 comparison, the Seabra
clade-classification confirmatory analyses, and the DCS-PK seed alignment.
These are the `benchmark-1254-files`, `partial-benchmark-files`,
`vigor4-files`, `seabra-files`, `profile-vs-3model-files` and `dcspk-files`
directories here, along with `00README.txt`, which describes them, and
`README-processing-test-results.txt`, which gives step-by-step instructions
for reproducing each result.

`vadr-zika-r2dt-diagrams-supplement.tar.gz` contains R2DT secondary-structure
diagrams for the test-set sequences, in both the linear and circular genome
conformations. These are the `r2dt-svgs` directory here. That package's own
`00README.txt` is included here as `00README-r2dt-diagrams.txt`, renamed only
to avoid colliding with the one above; it is otherwise unchanged.

To unpack either tarball:

```
tar xf <tarball.gz>
```

VADR is on github:
https://github.com/NLM-DIR/vadr

The Zika models are on bitbucket and on the VADR FTP site:
https://bitbucket.org/nawrockie/vadr-models-zika
https://ftp.ncbi.nlm.nih.gov/pub/nawrocki/vadr-models/zika/

Instructions for annotating Zika sequences with VADR:
https://github.com/NLM-DIR/vadr/wiki/Zika-virus-annotation

A snapshot of that page, taken 2026-11-11, is included here as
`vadr-wiki-Zika-virus-annotation.md`, so that the instructions cited by the
paper are preserved in the archived version of this repository. It is a loose
file, not part of either tarball above. The live page linked above may be
newer and is the one to use.

---
Questions/problems? email eric.nawrocki@nih.gov
