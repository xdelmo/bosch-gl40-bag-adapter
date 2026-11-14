# Adattatore buste universali per Bosch GL-40 — Design

Data: 2026-11-14 · Stato: approvato dall'utente (2026-11-14)

## Intento

Il sacchetto originale del Bosch GL-40 Hair Animal ha un cartoncino rigido (piastra) che scorre nel supporto di plastica del vano sacchetto. Il cartoncino dell'ultimo sacchetto è strappato. L'utente vuole usare **buste universali**: serve una piastra stampata, permanente, con la stessa sagoma del cartoncino GL-40, su cui si monta e si cambia la busta universale.

Successo = la piastra entra nel supporto come il cartoncino originale, il coperchio del vano si chiude, l'aspirazione non perde aria attorno al bocchettone, e cambiare busta richiede meno di un minuto senza attrezzi.

## Obiettivi
- Piastra stampata in 3D che replica la sagoma del cartoncino originale (misurato con il calibro sul pezzo rotto).
- Manicotto sul retro + ghiera di bloccaggio che stringe la bocca della busta universale.
- Tenuta sul bocchettone dell'aspirapolvere.
- Nuovo progetto in `~/development/hobbies/bosch-gl40-bag-adapter/` con la stessa pipeline del portacarte MagSafe (build123d → STEP/STL → 3MF Bambu Studio A1 mini) e le skill 3D.

## Non-obiettivi
- Aletta di chiusura automatica del sacchetto (quella dell'originale): fuori. Eventuale tappino a scatto per chiudere il manicotto quando si toglie la busta piena: solo se resta tempo, separato.
- Ricambio del supporto di plastica del vano (codice 00495701): non è rotto.
- Compatibilità con altri modelli Bosch/Siemens.

## Anti-obiettivi (fallisce anche se "funziona")
- La piastra impedisce la chiusura del coperchio o forza la linguetta di sicurezza del supporto.
- Aria e polvere che passano attorno al bocchettone o dalla bocca della busta, finendo nel motore.
- La busta si sfila quando è piena e pesante.

## Vincoli
- **Stampante**: Bambu Lab A1 mini, 180×180×180 mm, ugello 0.4.
- **Materiale**: PETG (no PLA: si deforma col calore e col carico).
- **Spessore piastra** = spessore del cartoncino originale (misurato), perché deve scorrere nelle guide del supporto e lasciare lavorare clip e linguetta di sicurezza.
- **Ingombro dietro la piastra**: manicotto + anello + busta devono stare nel vano senza toccare la clip del supporto né la linguetta di interblocco. Profondità disponibile da misurare nel vano.
- **Tolleranze FDM**: gioco generale 0.4 mm per gli accoppiamenti (come nel portacarte); spessore della piastra al nominale misurato, con eventuale correzione dopo la prima stampa di prova.
- Misure tutte dal pezzo fisico: nessun disegno ufficiale disponibile.

## Approcci considerati
- **A. Piastra + manicotto + anello di bloccaggio** — *scelto dall'utente* (proposto a scatto; poi passato a ghiera a quarto di giro, vedi Pezzi). Riutilizzabile, cambio busta veloce, va bene con buste con o senza cartoncino proprio. Due pezzi; il manicotto aumenta l'ingombro sul retro.
- **B. Doppia piastra a sandwich** che pizzica la busta tagliata: semplice ma tenuta peggiore sui bordi e cambio più lento.
- **C. Solo piastra, busta incollata/nastrata**: stampa rapidissima ma colla o nastro a ogni cambio.

## Design deciso

### Pezzi
1. **Piastra** — contorno del cartoncino GL-40: scanalatura a U in alto, due alette superiori con le tacche, foro del bocchettone. Spessore = cartoncino. Stampata piatta sul piatto, faccia anteriore (lato motore) in basso.
2. **Manicotto** — tubo corto solidale alla piastra sul retro, coassiale al foro, con una flangia di battuta alla base su cui è incollata una guarnizione in espanso adesivo. Raccordo ≥ 2.5 mm alla radice (il peso della busta piena tira tra i layer). Diametro: il massimo che lo spazio misurato nel vano consente (*mia scelta*).
3. **Ghiera di bloccaggio a quarto di giro** — pezzo separato, attacco a baionetta sul manicotto (2-3 denti, rampa che stringe in 1/4 di giro, piccolo fermo a fine corsa). Preme la bocca della busta **frontalmente** contro l'espanso della flangia: è la pressione assiale sull'espanso a chiudere le pieghe della carta (*mia scelta, su obiezione di agy*: uno scatto radiale lascia passare polvere dalle pieghe e strappa la carta).

### Buste
Sacchetti di carta kraft universali, aperti in cima, con soffietto, senza cartoncino ([foto prodotto](https://m.media-amazon.com/images/S/aplus-media-library-service-media/63c0395e-9237-44b2-b641-d10099010bf9.__CR0,0,1959,803_PT0_SX1464_V1___.png)). L'utente: "non importa la grandezza" — la busta si adatta al pezzo (raccolta a pieghe attorno al manicotto, piegata o tagliata se serve), non il contrario. Nessun dimensionamento sulla busta.

### Tenuta sul bocchettone
*Mia proposta, da confermare dopo le misure:* foro della piastra con una sede (gola) per una guarnizione — prima scelta riusare la membrana di gomma del cartoncino rotto se è integra, altrimenti O-ring o striscia di gomma/espanso adesivo. Scelta definitiva dopo aver misurato il bocchettone.

### Misure da prendere col calibro (prima del CAD)
Raccolte in `docs/measurements.md` con un disegno di riferimento:
- contorno piastra: larghezza, altezza, larghezza e profondità della U, raggio della U, posizione e forma delle alette e delle tacche;
- spessore del cartoncino;
- diametro e posizione (dal bordo) del foro e della membrana;
- diametro esterno del bocchettone dell'aspirapolvere;
- profondità libera dietro la piastra nel vano (fino al fondo/parete del vano o al primo ostacolo);
- posizione della clip e della linguetta di sicurezza del supporto rispetto alla piastra;
- se il bocchettone **entra** nel foro (attraverso la membrana) o si **appoggia** alla faccia anteriore: se entra, conta la profondità del foro; se si appoggia, la faccia anteriore deve restare piana e diventa la superficie di tenuta;
- se il cartoncino è davvero piatto o ha rilievi/bordi più spessi (si replicano solo quelli funzionali);
- tacche delle alette: trattate come **funzionali** (agganci della clip), misurate con precisione.

**Cancello**: se la profondità libera dietro la piastra è < 20 mm, manicotto + ghiera non ci stanno: ci si ferma e si ripensa l'attacco con l'utente prima del CAD.

### Struttura del progetto
Come `magsafe-cardholder`, con le correzioni:
- `CLAUDE.md` con le regole, `AGENTS.md` symlink a `CLAUDE.md`.
- `src/config.py` (tutte le misure) e `src/generate_adapter.py` (build123d, una funzione per pezzo, export STEP/STL in `output/`).
- `checks/check_fit.py`: asserzioni su interferenza anello/manicotto, ingombro posteriore entro la profondità misurata, spessore della piastra, foro coassiale.
- `build.sh`: CAD → Bambu Studio CLI (A1 mini 0.4, Generic PETG) → patch 3MF; patch e profili ripresi dal portacarte.
- `docs/hardware_context.md` (vincoli fisici), `docs/measurements.md`, `docs/superpowers/` (specifiche e piani).
- `.venv` con build123d; `.gitignore` per `output/`, `.venv/`, `tmp/`.
- `git init`. File di prova solo in `tmp/` (ignorato), mai alla radice.
- Skill 3D da `earthtojake/text-to-cad` in `.agents/skills/` con symlink relativi in `.claude/skills/`, solo quelle utili qui: `cad`, `cad-viewer`, `bambu-labs`, `dfam-check`, `step-parts`.

### Stampabilità e rigidità (*mie scelte*)
- Smusso 0.5 mm sul bordo della faccia a contatto col piatto (piede d'elefante), altrimenti la piastra non scorre nelle guide.
- Nervature radiali sul retro della piastra, fuori dalle zone delle guide e della clip, contro la flessione in depressione (il PETG a 2-3 mm flette più del cartoncino pressato).
- Perimetri pieni attorno al foro e alla radice del manicotto.
- Se un lato della piastra supera ~170 mm: stampa in diagonale sul piatto.

### Verifica
1. `./build.sh` senza errori e `checks/check_fit.py` verde.
2. **Stampa di prova (cancello)**: prima solo un ritaglio sottile della piastra (contorno + foro, senza manicotto) per provare scorrimento nelle guide, aggancio della clip e chiusura del coperchio. Ci si ferma finché l'utente non conferma; eventuali correzioni vanno in `config.py`.
3. Poi stampa completa: montaggio busta, chiusura coperchio, aspirazione di prova e controllo a occhio di perdite.
4. CAD solo con misure reali: niente `config.py` con valori segnaposto.

## Lasciato al builder
- Profilo esatto della baionetta (numero denti, rampa, gioco, fermo), purché regga una busta piena e si apra a mano anche impolverata.
- Spessore dell'espanso adesivo da prevedere nella flangia (da scegliere tra quelli in commercio, 2-5 mm).
- Altezza del manicotto entro la profondità libera misurata.
- Raccordi e smussi per stampabilità senza supporti.
- Override di stampa nel 3MF (perimetri, riempimento), partendo da quelli del portacarte.
