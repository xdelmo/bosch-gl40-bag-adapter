# Adattatore Buste Universali per Bosch GL-40

Adattatore parametrico stampato in 3D in PETG che sostituisce il cartoncino di supporto del sacchetto originale per aspirapolvere **Bosch GL-40** (Hair Animal), permettendo di utilizzare sacchetti di carta kraft universali senza cartoncino.

Il sistema è composto da:
1. **Piastra principale con manicotto**: replica il profilo del cartoncino originale con la scanalatura a U e le alette per scorrere nelle guide del supporto Bosch (00495701). Sul retro include un manicotto con flangia di battuta.
2. **Ghiera di serraggio a baionetta**: anello rimovibile con chiusura a quarto di giro che preme frontalmente la bocca della busta contro l'espanso adesivo della flangia, garantendo tenuta ermetica senza lacerare la carta.

## Pipeline & Comandi

Il progetto utilizza `build123d` per la generazione CAD parametrica e Bambu Studio per lo slicing:

```bash
# Generazione stampa di prova (default, solo profilo sottile piastra per verifica guide/clip nel vano)
./build.sh trial
# oppure semplicemente:
./build.sh

# Esecuzione controlli geometrici e tolleranze FDM
.venv/bin/python -m pytest checks/check_fit.py

# Generazione CAD isolata (STEP e STL in output/ senza slicer)
.venv/bin/python src/generate_adapter.py

# Esecuzione pipeline completa (disponibile dopo il rilevamento delle quote vano)
./build.sh full
```

## Misure & Parametri

Tutte le dimensioni e i vincoli geometrici derivano dalle misure effettuate con calibro sul pezzo fisico e sul vano aspirapolvere:
- Le quote e la tabella di rilevamento sono documentate in `docs/measurements.md` (con disegno in `assets/images/riferimento-misure.svg`).
- I parametri costruttivi effettivi sono definiti in `src/config.py`.
- I vincoli fisici e di sistema sono dettagliati in `docs/hardware_context.md`.

## Requisiti

- Python 3.12 con virtual environment in `.venv/` (`build123d>=0.11`, `pytest`)
- Bambu Studio in `/Applications/BambuStudio.app` (macOS)
- Stampante 3D Bambu Lab A1 mini con ugello 0.4 mm e filamento PETG
