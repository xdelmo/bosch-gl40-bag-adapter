# CLAUDE.md — Linee guida del progetto

Questo file contiene il contesto e le regole per Claude e gli agenti di sviluppo (AGY) che lavorano su questo repository.

## 1. Contesto del Progetto
Progetto CAD parametrico basato su Python (`build123d`) che genera un adattatore permanente in PETG per sostituire il cartoncino rotto del sacchetto dell'aspirapolvere **Bosch GL-40** (Hair Animal). L'adattatore consente di montare e sostituire sacchetti in carta kraft universali (senza cartoncino proprio) serrati frontalmente contro una guarnizione tramite un manicotto solidale alla piastra e una ghiera di bloccaggio a baionetta (quarto di giro).

## 2. Comandi Principali
Tutti i comandi vanno eseguiti dalla radice del repository:

```bash
# Esecuzione pipeline completa (CAD -> STEP/STL -> 3MF Bambu Studio -> Patch PETG)
./build.sh full

# Generazione stampa di prova (solo profilo sottile piastra per verifica guide/clip nel vano)
./build.sh trial

# Esecuzione controlli geometrici e tolleranze FDM
.venv/bin/python -m pytest checks/check_fit.py

# Generazione CAD isolata (STEP e STL in output/)
.venv/bin/python src/generate_adapter.py
```

## 3. Architettura & Pipeline
- `src/config.py`: tutte le quote dimensionali misurate e le costanti geometriche. Nessun valore derivato o segnaposto non verificato: il CAD parte solo con misure reali.
- `src/generate_adapter.py`: modellazione procedurale con `build123d` (`BuildPart`). Funzioni separate per piastra (`create_plate()`) e ghiera (`create_ring()`). Esporta STEP e STL in `output/`.
- `checks/check_fit.py`: suite di test `pytest` che verifica interferenze, giochi FDM, quote d'ingombro massimo rispetto a `DEPTH_FREE` e zone di rispetto (keep-out).
- `build.sh`: script di build che invoca la CLI di Bambu Studio (`/Applications/BambuStudio.app/Contents/MacOS/BambuStudio`) per importare la geometria e lancia `src/patch_3mf.py` per applicare i parametri di stampa ottimali in PETG.
- `src/patch_3mf.py`: modifica diretta del file 3MF zippato (`Metadata/project_settings.config`), aggiornando coerentemente la chiave `different_settings_to_system` per evitare reset da parte dell'interfaccia di Bambu Studio.

## 4. Sistema di Riferimento & Vincoli Globali (CRITICO)
- **Sistema di coordinate**:
  - Origine (X=0, Y=0): centro del foro del bocchettone di aspirazione.
  - Piano Z=0: faccia anteriore della piastra (lato motore/vano, superficie a contatto con il piatto di stampa).
  - Asse +Z: orientato verso il retro della piastra (verso il sacchetto e l'interno del vano).
  - Asse +Y: orientato verso l'alto (verso la scanalatura a U e le alette superiori).
- **Regola di sketch**: Schizzi solo su piani assoluti (es. `Plane.XY.offset(z)`, `Plane.YZ.offset(x)`), MAI su `faces().sort_by(...)` poiché i piani delle facce invertono o traslano gli assi locali in modo imprevedibile.
- **Materiale e Stampa**: PETG su Bambu Lab A1 mini (piatto 180×180×180 mm, ugello 0.4 mm). Non usare PLA (cede al calore e sotto depressione continua).
- **Tolleranze e accoppiamenti**:
  - Gioco generale accoppiamenti: `FIT_CLEARANCE = 0.4 mm`.
  - Spessore piastra: identico al nominale misurato del cartoncino (`PLATE_T`), nessuna correzione a priori.
  - Smusso anti piede d'elefante sul piatto: `EDGE_CHAMFER = min(0.5, PLATE_T * 0.25)` sulla faccia a contatto col piatto per consentire lo scorrimento nelle guide senza allargamenti. Nel 3MF disattivare la compensazione dello slicer (`elefant_foot_compensation "0"`).
  - Assenza di supporti: ogni sbalzo o sottosquadro (scanalature, rampe dei denti baionetta) deve prevedere smussi a 45°.
  - Raccordo radice manicotto: `SLEEVE_ROOT_FILLET >= 2.5 mm` per sopportare il peso del sacchetto pieno senza delaminazione tra i layer.
  - Cancello profondità vano: se `DEPTH_FREE < 20 mm`, stop immediato prima del CAD per ridiscutere l'attacco con l'utente.
  - Baionetta esterna: i denti della ghiera e della baionetta devono trovarsi all'esterno della zona di serraggio carta per non strappare la busta durante la rotazione.

## 5. Regole di Sviluppo & Workflow
- **Pipeline obbligatoria**: dopo qualsiasi modifica geometrica o di configurazione, eseguire `./build.sh` e verificare che `.venv/bin/python -m pytest checks/check_fit.py` sia completamente verde.
- **File temporanei**: file di prova, scratch script o esportazioni provvisorie vanno posizionati esclusivamente in `tmp/` (già ignorato da git), MAI nella radice del progetto né in cartelle tracciate.
- **Documentazione sincronizzata**: i file di documentazione in `docs/` (`hardware_context.md`, `measurements.md`, `README.md`) e questo `CLAUDE.md` devono essere aggiornati nello stesso commit in cui il codice o i requisiti cambiano.
- **Virtual Environment**: utilizzare sempre il Python del venv `.venv/bin/python`.
