# Adattatore Buste Universali per Bosch GL-40

Adattatore parametrico stampato in 3D in PETG che sostituisce il cartoncino di supporto del sacchetto originale per aspirapolvere **Bosch GL-40** (Hair Animal), permettendo di utilizzare sacchetti di carta kraft universali senza cartoncino.

Il sistema è composto da:
1. **Piastra principale con manicotto**: replica il profilo del cartoncino originale con la scanalatura a U e le alette per scorrere nelle guide del supporto Bosch (00495701). Sul retro include un manicotto con flangia di battuta.
2. **Ghiera di serraggio a baionetta**: anello rimovibile con chiusura a quarto di giro che preme frontalmente la bocca della busta contro l'espanso adesivo della flangia, garantendo tenuta ermetica senza lacerare la carta.

## Pipeline & Comandi

Il progetto utilizza `build123d` per la generazione CAD parametrica e Bambu Studio per lo slicing:

```bash
# Esecuzione pipeline completa (CAD -> STEP/STL -> 3MF Bambu Studio -> Patch PETG)
./build.sh full

# Generazione stampa di prova (solo profilo sottile per verificare guide, clip e chiusura vano)
./build.sh trial

# Esecuzione controlli geometrici e tolleranze FDM
.venv/bin/python -m pytest checks/check_fit.py
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
