#!/usr/bin/env perl
use strict;

my %syn_H = ();  # maps product names used by vigor to names used by vadr (and RefSeq)
$syn_H{"small_envelope_protein_M"} = "membrane_glycoprotein_M";

my $usage = "perl vigor-pep-to-ftrsum.pl <VIGOR .pep output file>";

if(scalar(@ARGV) != 1) { die $usage; }

my ($pep_file) = (@ARGV);

open(PEP, $pep_file) || die "ERROR unable to open $pep_file for reading";
while(my $line = <PEP>) { 
  if($line =~ s/^\>//) { 
    chomp $line;
    my @el_A = split(/\s/, $line);
    my $nel = scalar(@el_A);
    # CDS:
    #>KY075933.1.1 location=80..10351 codon_start=1 gene="GP1" product="genome polyprotein" ref_db="zikv_db" ref_id="KU647676"
    # mat_peptide
    #>KY075933.1.1.1 mat_peptide location=446..724 gene="GP1" product="protein pr" ref_db="zikv_mp" ref_id="KU647676_pr"
    my $coords = undef;
    my $product = undef;
    my $type = undef;
    my $idx = undef;
    my $seqname = $el_A[0];
    if($seqname =~ /^([^\.]+\.\d+).*$/) {
      $seqname = $1;
    }
    else {
      die "ERROR unable to parse seqname $seqname";
    }
     
    if($el_A[1] eq "mat_peptide") { 
      $type = "mat_peptide";
      $idx = 2;
    }
    else { # CDS
      $type = "CDS";
      $idx = 1;
    }
    if($el_A[$idx] =~ s/^location\=//) {
      $coords = $el_A[$idx];
    }
    else {
      die "ERROR (1) unable to parse line $line";
    }
    $idx = 4;
    if($el_A[$idx] =~ s/product\=\"//) {
      $product = $el_A[$idx];
      $idx++;
      while(($idx < $nel) && ($product !~ m/\"$/)) {
        $product .= "_" . $el_A[$idx];
        $idx++;
      }
      $product =~ s/\"$//;
    }
    else {
      die "ERROR (2) unable to parse line $line";
    }
    # product may have 'putative', and 'fragment/terminal', remove it so we can compare using equality with VADR output
    $product =~ s/genome\_//;
    #$product =~ s/^truncated //;
    $product =~ s/putative\_//;
    #$product =~ s/, fragment$//;
    #$product =~ s/, C\-terminal$//;
    # strip ,_C-terminal fragment suffix (symmetric with
    # ,_N-terminal below); 2 partial-genome seqs in the 848 set emit
    # "polyprotein,_C-terminal". Same feature (polyprotein), partial; let coords compare.
    $product =~ s/,\_C\-terminal$//;
    $product =~ s/,\_N\-terminal$//;

    if(defined $syn_H{$product}) {
      $product = $syn_H{$product};
    }
    print ("seq:$seqname product:$product coords:$coords\n");
  }
}

exit 0;

