---
type: hardware_context
project: Bosch GL-40 Bag Adapter
target_device: Aspirapolvere Bosch GL-40 (Hair Animal)
printer: Bambu Lab A1 mini
material: PETG
---

# Contesto Hardware: Adattatore Buste Universali per Bosch GL-40

## 1. Dispositivo di Destinazione & Vano Sacchetto (Bosch GL-40)
- **Scopo**: Sostituire il cartoncino a perdere del sacchetto originale (danneggiato/strappato) con una piastra permanente stampata in 3D in PETG, su cui montare e cambiare rapidamente sacchetti di carta kraft universali.
- **Supporto sacchetto**: Alloggiamento in plastica originale Bosch (codice ricambio 00495701) presente nel vano dell'aspirapolvere.
  - Guide di scorrimento laterali in cui la piastra deve infilarsi dall'alto verso il basso con gioco calibrato.
  - Clip di ritegno superiore per trattenere la piastra in sede durante l'aspirazione e le vibrazioni.
  - Linguetta di sicurezza/interblocco meccanico che impedisce la chiusura del coperchio se il sacchetto non è inserito correttamente.
- **Tenuta sul bocchettone**:
  - Il foro della piastra è coassiale al bocchettone di aspirazione.
  - La tenuta ermetica è garantita da una guarnizione/membrana (recupero della membrana originale del cartoncino o O-ring/gomma espansa adesiva) alloggiata in un'apposita gola/sede.
  - La faccia anteriore della piastra (lato motore/piatto) deve rimanere perfettamente complanare se il bocchettone vi va in battuta frontale.
- **Vincolo di profondità nel vano**:
  - Manicotto posteriore, ghiera di bloccaggio e sacchetto di carta raccolto devono rientrare nella profondità libera del vano (`DEPTH_FREE >= 20 mm`).
  - Se la profondità libera misurata è inferiore a 20 mm, manicotto e ghiera non possono coesistere e il design va ridiscusso con l'utente.
- **Keep-out zones**:
  - Manicotto, ghiera e nervature di rinforzo sul retro della piastra non devono interferire con la clip del supporto né con la linguetta di sicurezza del supporto 00495701.

## 2. Sacchetti di Carta Kraft Universali
- **Tipologia**: Buste aperte in cima con soffietto laterale, prive di cartoncino proprio.
- **Fissaggio**: La bocca della busta viene infilata sul manicotto posteriore, raccolta a pieghe e serrata assialmente tra la battuta con guarnizione in espanso adesivo (2-5 mm) della flangia e la ghiera a baionetta (quarto di giro).
- **Protezione della carta**: I denti della baionetta operano all'esterno del diametro di serraggio per non pizzicare o strappare la carta durante la rotazione di bloccaggio.

## 3. Ambiente di Produzione (Bambu Lab A1 mini)
- **Volume di Stampa**: 180 × 180 × 180 mm.
- **Ugello**: 0.4 mm.
- **Materiale**: PETG (scelto per rigidità strutturale, resistenza termica alle temperature di esercizio del motore in depressione ed elasticità degli innesti). No PLA (flessibile e soggetto a creep/deformazione termica).
- **Tolleranze FDM e parametri geometrici**:
  - Gioco generale accoppiamenti (`FIT_CLEARANCE`): +0.4 mm.
  - Spessore piastra (`PLATE_T`): identico al nominale misurato sul cartoncino originale per non forzare le guide.
  - Smusso anti piede d'elefante sul bordo a contatto col piatto: `EDGE_CHAMFER = min(0.5, PLATE_T * 0.25)` con Elephant Foot Compensation disattivata (`elefant_foot_compensation "0"`) nello slicer per preservare la verticalità delle guide.
  - Raccordo alla radice del manicotto: `SLEEVE_ROOT_FILLET >= 2.5 mm` contro lo sforzo di taglio e trazione dei layer causato dal peso del sacchetto pieno.
  - Stampa senza supporti: sbalzi e rampe a 45°.

## 4. Pipeline & Output
- **Pipeline**: Modellazione parametrica in Python con `build123d` → export STEP e STL in `output/` → generazione progetto 3MF tramite CLI di Bambu Studio (`/Applications/BambuStudio.app`) → patch dei profili di processo e filamento PETG via script dedicato.
- **Output**:
  - `output/adapter_plate.step` / `.stl`
  - `output/clamp_ring.step` / `.stl`
  - `output/bosch_gl40_adapter.3mf` (completo) e versione `trial` per test di scorrimento guide.
