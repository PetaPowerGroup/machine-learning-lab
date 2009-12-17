#!/usr/bin/perl

my @skup = <aaaa bbbb>;

opendir (DIR, "./") or die "$!";
my @files = grep {/.csv\b/}  readdir DIR;
close DIR;
foreach my $file (@files) {
   $pomocna = $file;
   $pomocna =~ (s/_vamp-.*//);
   $kljuc = 0;
   foreach my $testni (@skup) {
     if ($testni eq $pomocna) {
        $kljuc = 1;
     }
   }
 if ($kljuc == 0) {
   push (@skup,$pomocna);
   foreach my $druga (@files) {
	$trenutna = $druga;
	$trenutna =~ (s/_vamp-.*//);
	if ($pomocna eq $trenutna)  {  
		if ($file ne $druga)  {
			#otvoriti prvu datoteku i u nju dodati iz druge
			open PRVA, ">>", "$file";
			open DRUGA, "<", "$druga";
			print PRVA "1";
			while (<DRUGA>) {
				print PRVA;
			}
			close PRVA;
			close DRUGA;			
			# izbrisati /renameati/  drugu datoteku
			unlink("$druga");   #rename("$druga","$druga.1");
		}
	} 
   #osvježiti @files 
   #opendir (DIR, "./") or die "$!";
   #@files = grep {/.csv\b/}  readdir DIR;
   #close DIR;
   }
 }
}


$razred = 0;
open RAZREDI, "<", "uzorak_razred.txt";

open SVE, ">", "sve_znacajke.txt";
opendir (DIR, "./") or die "$!";
my @fileovi = grep {/.csv\b/}  readdir DIR;
close DIR;
foreach my $file (@fileovi) {
   open(FH,"./$file") or die "$!";
   $pomocna = $file;
   $pomocna =~ (s/_vamp_.*//);
   while (<RAZREDI>) {
	$razred = 0;
	chomp;
	@ime = split/.mp3>>/,$_;
	if ($pomocna == $ime[0])  {  # usporedi dali ima u tom redu.
		$razred = $ime[1];
		last;
	} 
   }
   close RAZREDI;
   open RAZREDI, "<", "uzorak_razred.txt";
   while (<FH>){ 
     #read file line by line here
     chomp;
     print SVE;
     print SVE "$razred \n";# ovdje æe još trebat dodati u koji razred spada
   }
   close(FH);
}

close RAZREDI;
close SVE;      # ovdje gore iz svih datoteka s nastavkom .csv èita i sprema u jednu
open ULAZ, "<", "sve_znacajke.txt";

$brojac = 0;
$zastavica = 0;
open IZLAZ, ">", "skup_svih_znacajki.txt" ;

while (<ULAZ>) {
	chomp;
	if (/^0/) {
		$brojac = 0;
		if ($zastavica) {
			print IZLAZ "\n";
		}
		else {
			$zastavica = 1;
		}
		my @oznakaklase = split/"/;
		print IZLAZ "@oznakaklase[-1]";
	}
	if (s/,5.0*,/intervali:/) {     # ako je interval 5 onda:
		(s/[^,]*//);  # da riješimo ovo s poèetka
		(s/,".*"/ /);   # ovdje mièemo ono s kraja
		(s/^,//);     # mièemo zarez koji je ostao na poèetku reda
		(s/,/ /g);    # zamjenjujemo sve zareze sa razmakom
		# sada æemo dodati brojeve ispred vrijednosti svake znaèajke
		my @lista = split;
		#print IZLAZ "@lista[-1] ";  # ovdje ispisujemo oznaku klase
		$br = 0;
		foreach $broj (@lista) {
			$br += 1;
			if ($br == $#lista +1) {
				last;
			}
			else {
				$brojac += 1; 
				if ($broj)  {    # ako je nula onda preskoèi
					print IZLAZ "$brojac:$broj ";
				}
			}
		}
	} 
}

close ULAZ;
close IZLAZ;


# primjer pozivanja:  perl uzorci.pl       , 
# u istom direktoriju moraju biti *.csv datoteke i "uzorak_razred.txt"

# 1.dio : provjera ako ima više vrsta znaèajki i sve sprema u isti file(tj. jedan file po
#  pjesmi)
# 2.dio : provjeri kojem razredu znaèajke pripadaju i zapiše sve u jedan file
# 3.dio : mijenja format kako bi bio prikladan za ulaz u svm
