#!/usr/bin/perl

$zaucenje = $ARGV[0];  #uzimamo argument(postotak) iz komandne linije
$zaucenje =~ (s/%//);

my %klase = {};
my %pomocni = {}; 

open ULAZ, "<", "skup_svih_znacajki.txt" ;

while (<ULAZ>) {
	@razred = split;
	if (exists $klase{"@razred[0]"})  {
		$klase{"@razred[0]"} += 1;
	}
	else {
		$klase{"@razred[0]"} = 1;
		$pomocni{"@razred[0]"} = 0;
	}
}

close ULAZ;
open ULAZ, "<", "skup_svih_znacajki.txt" ;
open UCENJE, ">", "skup_za_ucenje.txt" ;
open TESTIRANJE, ">", "skup_za_testiranje.txt" ;

while (<ULAZ>)  {
	@razred = split;
	$pomocni{"@razred[0]"} +=1;
	if ($pomocni{"@razred[0]"}/$klase{"@razred[0]"} <= $zaucenje/100)   {
		print UCENJE;
	}
	else {
		print TESTIRANJE;
	}
}

close ULAZ;
close UCENJE;
close TESTIRANJE;

# pozivanje skripte: perl odvoji.pl 50%   ,pola uzoraka za uèenje, pola za testiranje 