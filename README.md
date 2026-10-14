# Sustav preporuke šahovskih otvaranja

## Opis projekta

Cilj projekta je razvoj sustava preporuke šahovskih otvaranja na temelju stila igre pojedinog igrača. Sustav analizira šahovske partije zapisane u PGN formatu, izdvaja značajke koje opisuju stil igre te pomoću algoritma K-means grupira igrače prema sličnosti njihovih stilova.

Na temelju dobivenih klastera sustav preporučuje šahovska otvaranja koja su bila uspješna kod igrača sličnog stila igre. Aplikacija je implementirana u Pythonu, a za korisničko sučelje koristi se Streamlit.

## Funkcionalnosti

- Parsiranje šahovskih partija iz PGN datoteka.
- Izdvajanje značajki koje opisuju stil igre igrača.
- Normalizacija značajki prije grupiranja.
- Grupiranje igrača pomoću algoritma K-means.
- Analiza i evaluacija dobivenih klastera.
- Preporuka šahovskih otvaranja na temelju stila igre.
- Rangiranje otvaranja prema uspješnosti i broju odigranih partija.
- Vizualizacija rezultata analize.
- Korisničko sučelje izrađeno pomoću biblioteke Streamlit.

## Korištene tehnologije

- Python 3.12.1
- python-chess
- NumPy
- pandas
- Matplotlib
- scikit-learn
- Streamlit
- Jupyter Notebook
- pickle

## Struktura projekta

Projekt je podijeljen u module koji pokrivaju glavne faze sustava:

| Modul | Opis |
|---|---|
| `parser` | Parsiranje šahovskih partija iz PGN datoteka. |
| `features` | Izdvajanje značajki koje opisuju stil igre igrača. |
| `clustering` | Normalizacija značajki i grupiranje igrača. |
| `recommender` | Generiranje preporuka šahovskih otvaranja. |
| `evaluation` | Evaluacija grupiranja i sustava preporuke. |
| `app.py` | Pokretanje Streamlit aplikacije. |

## Metodologija

### 1. Priprema podataka

Ulazni podaci sastoje se od šahovskih partija zapisanih u PGN formatu. Pomoću biblioteke `python-chess` partije se parsiraju, a potezi se analiziraju radi prikupljanja informacija o načinu igre pojedinih igrača.

### 2. Izdvajanje značajki

Za svakog igrača izdvajaju se značajke koje opisuju njegov stil igre:

- Pritisak u središtu ploče.
- Broj žrtvovanih figura i vrijednost žrtava.
- Broj izmjena figura.
- Rana uzimanja figura.
- Razvijanje figura.
- Ponavljanje poteza.
- Izvođenje rokade i vrijeme njezina izvođenja.
- Napadi i šahovi.
- Udio poteza pješacima.

Izdvojene značajke agregiraju se na razini igrača i normaliziraju kako bi bile prikladne za postupak grupiranja.

### 3. Grupiranje igrača

Za grupiranje igrača koristi se algoritam K-means. Na temelju sličnosti izdvojenih značajki igrači se raspoređuju u tri klastera (`k = 3`).

Dobiveni klasteri interpretiraju se kao sljedeći stilovi igre:

- **Agresivni stil** – igrači koji češće stvaraju napade i biraju taktički zahtjevnije pozicije.
- **Eksperimentalni stil** – igrači koji se povezuju s nekonvencionalnim ili rjeđe korištenim pristupima.
- **Pozicijski stil** – igrači koji češće preferiraju pozicijske planove i postupno poboljšavanje položaja.

Ovi nazivi predstavljaju interpretaciju dobivenih klastera na temelju analiziranih značajki.

### 4. Generiranje preporuka

Sustav analizira uspješnost šahovskih otvaranja unutar klastera kojem igrač pripada. Otvaranja se rangiraju prema broju pobjeda i ukupnom broju odigranih partija, uz primjenu zaglađivanja radi smanjenja utjecaja otvaranja s malim brojem odigranih partija.

Na temelju dobivenog poretka korisniku se prikazuje popis preporučenih otvaranja. Za novog igrača sustav može odrediti klaster na temelju njegova vektora značajki i zatim generirati preporuke iz odgovarajućeg klastera.

## Instalacija i pokretanje

### Preduvjeti

Za pokretanje projekta potrebno je imati instaliran Python 3.12 ili kompatibilnu verziju te Git.

### 1. Kloniranje repozitorija

```bash
git clone https://github.com/IvanDundovic/chess-opening-recommender.git
cd chess-opening-recommender
```
### 2. Stvaranje virtualnog okruženja

Na sustavu Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Na sustavima Linux i macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalacija potrebnih biblioteka

```bash
pip install python-chess numpy pandas matplotlib scikit-learn streamlit jupyter
```

Biblioteka `pickle` dio je standardne Pythonove biblioteke i ne zahtijeva zasebnu instalaciju.

### 4. Pokretanje aplikacije

```bash
streamlit run app.py
```

Nakon pokretanja Streamlit će ispisati lokalnu adresu na kojoj se može otvoriti korisničko sučelje.

### 5. Pokretanje Jupyter Notebooka

```bash
jupyter notebook
```

## Ulazni podaci i modeli

Za rad sustava potrebne su PGN datoteke koje sadrže šahovske partije. Putanje do ulaznih datoteka potrebno je uskladiti s konfiguracijom projekta.

Ako se istrenirani model i parametri normalizacije spremaju pomoću biblioteke `pickle`, odgovarajuće datoteke moraju biti dostupne na lokacijama koje aplikacija očekuje.

## Evaluacija

Evaluacija obuhvaća analizu kvalitete grupiranja igrača i ponašanja sustava preporuke.

- **Silhouette score** – procjenjuje koliko su uzorci slični vlastitom klasteru u odnosu na ostale klastere.
- **Davies–Bouldin indeks** – procjenjuje odnos raspršenosti unutar klastera i njihove međusobne odvojenosti.

## Ograničenja

- Kvaliteta rezultata ovisi o količini i kvaliteti dostupnih PGN podataka.
- Klasteri predstavljaju pojednostavljenu podjelu stilova igre.
- Uspješnost otvaranja ovisi o razini igrača, protivniku i drugim okolnostima partije.
- Preporuke na temelju povijesnih rezultata ne jamče uspjeh u budućim partijama.

## Moguća buduća poboljšanja

- Proširenje skupa podataka dodatnim šahovskim partijama.
- Uvođenje dodatnih značajki za opis stila igre.
- Usporedba K-means algoritma s drugim metodama grupiranja.
- Proširenje evaluacije sustava preporuke.
- Poboljšanje korisničkog sučelja.

## Autor

Ime i prezime: Ivan Dundović

Projekt je izrađen u sklopu završnog rada.
