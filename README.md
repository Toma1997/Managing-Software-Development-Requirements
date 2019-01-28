# Vođenje zahteva u razvoju softvera

Kratak opis:

Omogućiti vođenje zahteva prilikom izrade softvera. Potrebno je voditi zahteve koji mogu imati
različite labele (npr. novo, ažuriranje, greška). Labele uvodi korisnik. Zahteve takođe unosi
korisnik. Svaki zahtev ima i naslov (kratak) i opis. Omogućiti njihovo dodavanje, izmenu i
uklanjanje. Korisnik kada pogleda sve zadatke, može prihvatiti da radi zahtev i čime će on
postati dodeljen njemu. Kada korisnik koji je odabrao zahtev za rešavanje, reši dati zahtev,
može ga markirati kao rešenog, čime će se promeniti njegov status. Labele, zahteve čuvati u
bazi podataka ili tekstualnoj datoteci.


Funkcionalni zahtevi:

● Kreiranje labele zahteva naziv labele i odabir boje labele. Labele ne smeju imati isti
naziv.

● Brisanje labele vrši korisnik koji ju je kreirao, dakle labela ima podatak i o autoru.

● Izmena labele podrazumeva samo izmenu njene boje, naziv se ne može menjati.
Izmenu takođe može vršiti samo korisnik koji ju je i kreirao. Autor (korisnik) u osnovnom
delu aplikacije predstavlja samo njegovo ime i prezime.

● Kreiranje zahteva se vriši odabirom naziva i opisa samog zahteva. Zahtevu se može
pridodati i labela koja je već prethodno definisana, ili korisnik može u tom trenutku
kreirati novu labelu, pa izabrati nju. Kada korisnik kreira zahtev, podrazumeva se da je
on njen autor, a datum se izvodi na osnovu trenutnog datuma. Autor u osnovnom delu
aplikacije predstavlja samo njegovo ime i prezime.

● Pregled zahteva se vrši u tabelarnom prikazu, gde se prikazuje naziv, deo opisa (npr. 10
reči ili 100 karaktera) i ako je opis duži od tog dela, na kraj dodati tri tačke (...), zatim
labela koja je dodeljena, autor i datum kreiranja, datum prihvatanja (ako nije prihvaćen ni
od jednog korisnika, ovo polje je prazno), korisnik koji ga je prihvatio (ako nije prihvaćen
ni od jednog korisnika, ovo polje je prazno), status (neprihvaćen, prihvaćen, razrešen).

● Pregled ličnih (prihvaćenih) zahteva se vrši u tabelarnom prikazu koji ima iste podatke
kao i pregled zahteva.

● Detaljan pregled se vrši odabirom konkretnog zahteva iz pregleda zahteva, čime se
dobija prikaz svih podataka koji su uneti prilikom njegovog kreiranja, ali i podaci o autoru
i datumu kreiranja, korisniku koji ga je prihvatio (ako jeste) i datutmu prihvatanja (ako je
prihvaćen).

● Brisanje zahteva se vrši odabirom zahteva iz pregleda zahteva i odabirom opcije za
brisanje. Korisnik može obrisati zahtev samo ako je on njegov autor, i ako zahtev nije u
toku rada (prihvaćen da se radi na njemu).

● Dodavanje zahteva kao lični zahtev (prihvatanje zahteva), jeste prihvatanje odgovornosti
za rešavanje zahteva datog korisnika. Korisnik može da prihvati zahtev samo ako ga već
nije prethodno prihvatio. Ovom opcijom, zahtev se dodaje u lične zahteve korisnika.

● Razrešavanje zahteva predstavlja završetak zadatka korisnika koji ga je prihvatio da
odradi. Razrešavanje zadatka se vrši odabirom zahteva iz liste prihvaćenih (ličnih)
zahteva korisnika i odabirom opcije razreši. Time se ovaj zahtev uklanja iz liste
prihvaćenih (ličnih) zahteva. Razrešeni zadaci menjaju svoj status u prikazu svih zahteva
na razrešen.


Dodatni funkcionalni zahtevi:

● Omogućiti prijavu korisnika, čime svaki korisnik vidi sve zahteve koje niko još uvek nije
prihvatio da radi, ali i sve zahteve koje je sam prihvatio.

● Omogućiti prioretizaciju zahteva.

● Dodati kolonu za prikaz datuma razrešavanja zahteva. Ovaj datum se određuje spram
trenutnog datuma kada korisnik odabere opciju razreši nad ličnim zahtevom.
