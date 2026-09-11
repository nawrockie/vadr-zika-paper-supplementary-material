#!/usr/bin/env perl
use strict;

my $usage = "perl vadr-ftr-to-ftrsum.pl <VADR .ftr output file>";

if(scalar(@ARGV) != 1) { die $usage; }

my ($ftr_file) = (@ARGV);

my $line; # a line of the .ftr file

my $line; # a line of the .at file

open(FTR, $ftr_file) || die "ERROR unable to open $ftr_file for reading";
while($line = <FTR>) { 
  if($line !~ m/^\#/) { 
    chomp $line;
    my @el_A = split(/\s+/, $line);
    if(scalar(@el_A) == 26) { 
      my ($idx, $seqname, $seqlen, $pf, $bestmdl, $ftrtype, $ftrname, $ftrlen, $ftridx, $paridx, $str, $n_from, $n_to, $n_instp, $trc, $n5, $n3, $p_from, $p_to, $p_instp, $p_sc, $nsa, $nsn, $seq_coords, $mdl_coords, $ftr_alerts) = (@el_A);
#      print ("seq:$seqname product:$ftrname coords:$seq_coords pf:$pf\n");
      $seq_coords =~ s/\:\+//g;
      if(($ftrtype eq "CDS") || ($ftrtype eq "mat_peptide")) { 
        print ("seq:$seqname product:$ftrname coords:$seq_coords\n");
      }
    }
  }
}
close(FTR);

exit 0;

