#!/usr/bin/perl

$razred = 0;
open RAZREDI, "<", "uzorak_razred.txt";

open SVE, ">", "sve_znacajke.txt";
opendir (DIR, "./") or die "$!";
my @files = grep {/.csv/}  readdir DIR;
close DIR;
foreach my $file (@files) {
   open(FH,"./$file") or die "$!";
   $pomocna = $file;
   $pomocna =~ (s/_vamp_.*//);
   while (<RAZREDI>) {
	chomp;
	@ime = split/.mp3>>/,$_;
	if ($pomocna == $ime[0])  {  # usporedi dali ima u tom redu.
		$razred = $ime[1];
	} 
   }
   close RAZREDI;
   open RAZREDI, "<", "uzorak_razred.txt";
   while (<FH>){ 
     #read file line by line here
     chomp;
     print SVE;
     print SVE "$razred \n";# ovdje �e jo� trebat dodati u koji razred spada
   }
   close(FH);
}

close RAZREDI;
close SVE;      # ovdje gore iz svih datoteka s nastavkom .csv �ita i sprema u jednu
open ULAZ, "<", "sve_znacajke.txt";

$brojac = 0;
$zastavica = 0;
open IZLAZ, ">", "skup_svih_znacajki.txt" ;

while (<ULAZ>) {
	$brojac = 0;
	chomp;
	if (/^0/) {
		if ($zastavica) {
			print IZLAZ "\n";
		}
		else {
			$zastavica = 1;
		}
	}
	if (s/,5.0*,/intervali:/) {     # ako je interval 5 onda:
		(s/[^,]*//);  # da rije�imo ovo s po�etka
		(s/,".*"/ /);   # ovdje mi�emo ono s kraja
		(s/^,//);     # mi�emo zarez koji je ostao na po�etku reda
		(s/,/ /g);    # zamjenjujemo sve zareze sa razmakom
		# sada �emo dodati brojeve ispred vrijednosti svake zna�ajke
		my @lista = split;
		print IZLAZ "@lista[-1] ";  # ovdje ispisujemo oznaku klase
		foreach $broj (@lista) {
			$brojac += 1; 
			if ($brojac <= $#lista)  {   
				if ($broj)  {    # ako je nula onda presko�i
					print IZLAZ "$brojac:$broj ";
				}
			}
		}
		#print IZLAZ;
	} 
}

close ULAZ;
close IZLAZ;


# primjer pozivanja:  perl uzorci.pl       , 
# u istom direktoriju moraju biti *.csv datoteke i "uzorak_razred.txt"