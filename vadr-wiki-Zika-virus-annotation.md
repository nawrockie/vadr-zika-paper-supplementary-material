> **This is an archived snapshot, not the live page.**
>
> Source: <https://github.com/NLM-DIR/vadr/wiki/Zika-virus-annotation>
> Copied: 2026-11-11, from wiki commit `c5b8a75` (the last change to this page).
>
> It is included here so that the instructions cited by the paper are preserved
> alongside the rest of the supplementary material. The live page may have been
> updated since; for current instructions, use the link above rather than this
> file. Below this note the text is unchanged.

---

## [How to annotate Zika virus (ZIKV) sequences with VADR](#howto)

## [Recommended command-line options](#options)
 * [Explanation of the recommended options](#optionsexplain)
 * [Nucleotide-level clade classification](#clade)
 * [A note on the INDEFINITE_CLASSIFICATION_NN alert for Zika](#nnindfcl)

## [Structure drawing with R2DT](#r2dt)

## [Additional VADR documentation](#docs)

---
## <a name="howto"></a>How to annotate Zika virus sequences with VADR

**GenBank is not currently using VADR to
automatically process Zika sequence submissions like it does for
[SARS-CoV-2](https://github.com/ncbi/vadr/wiki/Coronavirus-annotation)**.
GenBank Zika sequence submissions are still all manually reviewed, but
curators may use VADR as part of that review, running `v-annotate.pl` on the
command line with options like those below.

Steps for using VADR for Zika annotation:

1. Download and install VADR **v1.7.1 or later**, following the instructions on this
   [page](https://github.com/ncbi/vadr/blob/master/documentation/install.md).
   **v1.7.1 is the first version that works with the Zika models**; earlier versions
   cannot parse the model info file at all.

2. The Zika models are installed automatically by `vadr-install.sh` as of v1.7.1.
   To download them separately, the current package (version 1.7.1-2, gzipped tarball) is
   [here](https://ftp.ncbi.nlm.nih.gov/pub/nawrocki/vadr-models/zika/1.7.1-2/vadr-models-zika-1.7.1-2.tar.gz).
   Unpack it (`tar xfz <tarball.gz>`) and note the directory it creates
   (`<zika-models-dir>`).

3. <a name="trim">Remove terminal ambiguous nucleotides from your
   input fasta sequence file using the `fasta-trim-terminal-ambigs.pl`
   script in `$VADRSCRIPTSDIR/miniscripts/`. GenBank processing of
   viral sequences typically includes removing ambiguous nucleotides from
   the beginning and ends of sequences, and also removing sequences
   that are less than 50nt or more than 12,000nt (after trimming).
   Zika sequences that are more than 12,000nt are longer than expected
   (the RefSeq NC_035889 is 10,808nt).

   ***WARNING: the `fasta-trim-terminal-ambigs.pl` script will not
   exactly reproduce the trimming that the GenBank pipeline does in
   some rare cases, but should fix the large majority of the
   discrepancies you might see between local VADR results and GenBank
   results.***

   To remove terminal ambiguous nucleotides from your sequence file
   `<input-fasta-file>` and to remove short and long sequences to create a new trimmed file
   `<trimmed-fasta-file>`, execute:

```
$VADRSCRIPTSDIR/miniscripts/fasta-trim-terminal-ambigs.pl --minlen 50 --maxlen 12000 <input-fasta-file> > <trimmed-fasta-file>
```

4. Run `v-annotate.pl` on the trimmed fasta file, with the options in the
   next section.

---
## <a name="options"></a>Recommended command-line options

```
v-annotate.pl -r --r_file <zika-models-dir>/zika.rpn.fa --nosub \
    --lowsim5ftr 15 --lowsim3ftr 15 \
    --mkey zika --mdir <zika-models-dir> \
    <trimmed-fasta-file> <output directory>
```

This matches the recommended usage in the model package's own `00README.txt`.

### <a name="optionsexplain"></a>Explanation of the recommended options

| option | what it does |
|---|---|
| `-r --r_file <dir>/zika.rpn.fa` | seeds the alignment from the 8 model sequences in "replaced-N" form, which speeds up and stabilizes alignment of full-length genomes |
| `--nosub` | disables subgroup-based model selection; the package contains a single model, so there is nothing to select between |
| `--lowsim5ftr 15 --lowsim3ftr 15` | raises the low-similarity thresholds at feature 5' and 3' ends, which suppresses spurious low-similarity alerts in the UTRs |
| `--mkey zika --mdir <dir>` | selects the `zika` model from the unpacked package |

### <a name="clade"></a>Nucleotide-level clade classification

The Zika package enables VADR's nearest-neighbor classification, so `v-annotate.pl`
additionally writes a `.scn` file assigning each sequence to an African, Asian or
American clade, together with the percent identity to its nearest and second-nearest
training sequences and the gap between them.

### <a name="nnindfcl"></a>A note on the INDEFINITE_CLASSIFICATION_NN alert for Zika

**Expect this alert on nearly every Zika sequence. It is not an error and it is not fatal.**

`INDEFINITE_CLASSIFICATION_NN` (`nnindfcl`) fires when the fractional identity gap
between a sequence's best and second-best clade falls below a threshold, `0.05` by
default. **Zika's clades are far more compact than that default anticipates**, so almost
every sequence trips it. On a 754-sequence benchmark spanning all three clades, 753
sequences (99.9%) were flagged. The median gap was `0.0049`, and even the most divergent
clade in the set (African) had gaps of only `0.031` to `0.049`.

The alert is **never fatal**. It does not change the annotation, the pass/fail status, or
the clade assignment itself, and on that benchmark the clade assignments were 100%
concordant with published assignments despite essentially every one carrying the alert.

If the alert is not useful for your application, the threshold can be lowered with
`--nn_indefclass <x>`. **We do not recommend a specific value.** The gap distribution for
Zika is narrow enough that the flag rate is very sensitive to the exact threshold chosen
(on the benchmark above, `0.005` flagged 54% of sequences while `0.002` flagged 2%), and
we have no dataset containing genuine Zika clade misclassifications against which a
tighter threshold could be shown not to miss real cases. **The default reports a true
property of the data**, which is that Zika's clades are separated by very little
divergence.

---
## <a name="r2dt"></a>Structure drawing with R2DT

VADR v1.7.1's `--draw_r2dt` option renders the annotated secondary structure of each
sequence using [R2DT](https://github.com/r2dt-bio/R2DT). The Zika package ships the two
required R2DT templates (`zika-linear`, `zika-circular`) under `r2dt-templates/`, and
`vadr-install.sh` installs them so that `--draw_r2dt` works without any manual step.

Add `--draw_r2dt` to the command above to produce the drawings. See
[r2dt-drawing.md](https://github.com/ncbi/vadr/blob/master/documentation/r2dt-drawing.md)
and [r2dt-templates.md](https://github.com/ncbi/vadr/blob/master/documentation/r2dt-templates.md)
for details.

---
## <a name="docs"></a>Additional VADR documentation

* [VADR README](https://github.com/ncbi/vadr/blob/master/README.md)
* [Alert and error message documentation](https://github.com/ncbi/vadr/blob/master/documentation/alerts.md)
* [`v-annotate.pl` documentation](https://github.com/ncbi/vadr/blob/master/documentation/annotate.md)
