#!/usr/bin/env perl
use strict;

my $usage = "perl compare-two-ftrsums.pl <.ftrsum file 1> <.ftrsum file 2>\n";

if(scalar(@ARGV) != 2) { 
  die $usage;
}
my ($ftrsum1_file, $ftrsum2_file) = (@ARGV);

my $line;
my $seq;
my $product;
my %coords1_H = ();
my %coords2_H = ();
my %ref1_H = ();
my %ref2_H = ();

open(FTRSUM1, $ftrsum1_file) || die "ERROR unable to open $ftrsum1_file for reading";
while($line = <FTRSUM1>) { 
  chomp $line;
  my @el_A = split(/\s+/, $line);
  foreach my $el (@el_A) { 
    if($el =~ /^coords\:(\S+)$/) { 
      $coords1_H{$seq.":".$product} = $1;
    }
    elsif($el =~ /^([^\:]+)\:([^\:]+)$/) { 
      my ($key, $value) = ($1, $2); 
      if($key eq "seq") { 
        $seq = $value; 
      }
      elsif($key eq "product") { 
        $product = $value; 
#        $product =~ s/^genome\_//;
#        $product =~ s/^capsid\_protein\_//;
      }
#      elsif($key eq "ref") { 
#        $ref1_H{$seq.":".$product} = $value; 
#      }
#      elsif($key eq "pf") { 
#        $pf1_H{$seq.":".$product} = $value; 
#      }
    }
    else { die "ERROR unable to parse element $el in line:\n$line"; }
  }
}
close(FTRSUM1);

open(FTRSUM2, $ftrsum2_file) || die "ERROR unable to open $ftrsum2_file for reading";
while($line = <FTRSUM2>) { 
  chomp $line;
  my @el_A = split(/\s+/, $line);
  foreach my $el (@el_A) { 
    if($el =~ /^coords\:(\S+)$/) { 
      $coords2_H{$seq.":".$product} = $1;
    }
    elsif($el =~ /^([^\:]+)\:([^\:]+)$/) { 
      my ($key, $value) = ($1, $2); 
      if($key eq "seq") { 
        $seq = $value; 
      }
      elsif($key eq "product") { 
        $product = $value; 
#        $product =~ s/^genome\_//;
#        $product =~ s/^capsid\_protein\_//;
      }
#      elsif($key eq "ref") { 
#        $ref2_H{$seq.":".$product} = $value; 
#      }
#      elsif($key eq "pf") { 
#        $pf2_H{$seq.":".$product} = $value; 
#      }
    }
    else { die "ERROR unable to parse element $el in line:\n$line"; }
  }
}
close(FTRSUM2);

foreach my $seqproduct (sort keys (%coords1_H)) { 
  if(defined $coords2_H{$seqproduct}) { 
    my $coords1 = $coords1_H{$seqproduct};
    my $coords2 = $coords2_H{$seqproduct};
    $coords1 =~ s/\>//;
    $coords1 =~ s/\<//;
    $coords2 =~ s/\>//;
    $coords2 =~ s/\<//;
    if($coords1 eq $coords2) { 
      printf("PRODUCT-COORDS-MATCH $seqproduct coords: $coords1_H{$seqproduct} $coords2_H{$seqproduct}\n");
    }
    else { 
      printf("PRODUCT-COORDS-MISMATCH $seqproduct coords: $coords1_H{$seqproduct} $coords2_H{$seqproduct}\n");
    }
  }
  else { 
    printf("PRODUCT-MISSING-2 $seqproduct coords1: $coords1_H{$seqproduct}\n");
  }
}
foreach my $seqproduct (sort keys (%coords2_H)) { 
  if(! defined $coords1_H{$seqproduct}) { 
    printf("PRODUCT-MISSING-1 $seqproduct coords2: $coords2_H{$seqproduct}\n");
  }
}

