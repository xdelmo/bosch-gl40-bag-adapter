# Adattatore buste GL-40 — Piano di implementazione

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** piastra in PETG con la sagoma del cartoncino del sacchetto Bosch GL-40, con manicotto e ghiera a quarto di giro che fissano una busta di carta kraft universale.

**Architecture:** progetto CAD parametrico come `../magsafe-cardholder`: tutte le misure in `src/config.py`, geometria build123d in `src/generate_adapter.py` (una funzione per pezzo), controlli geometrici pytest in `checks/check_fit.py`, `build.sh` che genera STEP/STL e il 3MF Bambu Studio per A1 mini + patch dei parametri di stampa.

**Tech Stack:** Python 3.12, build123d ≥ 0.11, pytest, Bambu Studio CLI (`/Applications/BambuStudio.app`), skill `earthtojake/text-to-cad`.

**Spec:** `docs/superpowers/specs/2026-11-14-bosch-gl40-bag-adapter-design.md`

## Global Constraints

- Materiale PETG; stampante Bambu Lab A1 mini, ugello 0.4, piatto 180×180 mm.
- Spessore piastra = spessore del cartoncino misurato (`PLATE_T`), nessuna correzione a priori.
- Gioco accoppiamenti 0.4 mm (`FIT_CLEARANCE`).
- Smusso sul bordo della faccia a contatto col piatto: `EDGE_CHAMFER = min(0.5, PLATE_T * 0.25)`, così su un cartoncino sottile resta abbastanza bordo verticale nelle guide. Nel 3MF va disattivata l'Elephant Foot Compensation dello slicer (`elefant_foot_compensation "0"`), per non correggere due volte.
- Niente supporti: ogni sbalzo (cielo delle scanalature, denti della ghiera) ha uno smusso a 45°.
- Raccordo alla radice del manicotto ≥ 2.5 mm (`SLEEVE_ROOT_FILLET`).
- Cancello profondità: `DEPTH_FREE < 20` mm → stop, si ripensa con l'utente.
- Niente valori segnaposto in `config.py`: il CAD parte solo con misure reali.
- Sistema di riferimento: origine al centro del foro; Z=0 faccia anteriore (lato motore, sul piatto di stampa), +Z verso la busta; +Y verso la scanalatura a U. Schizzi solo su piani assoluti (`Plane.XY.offset(z)`), mai su `faces().sort_by(...)` (lezione del portacarte).
- `AGENTS.md` è symlink a `CLAUDE.md`; `CLAUDE.md` < 24 KB. Skill in `.agents/skills/<nome>` con symlink relativo `.claude/skills/<nome> -> ../../.agents/skills/<nome>`.
- File di prova solo in `tmp/` (ignorato da git), mai alla radice.
- I docs toccati da un task si aggiornano nello stesso commit.

## Review Focus

1. **Piastra troppo stretta nelle guide** (piede d'elefante, PETG che si allarga): l'utente si aspetta che scorra come il cartoncino. → `test_edge_chamfer_at_bed` (Task 3).
2. **Ingombro posteriore con la carta raccolta**: busta piegata a pieghe aggiunge spessore; manicotto + ghiera + carta devono restare sotto `DEPTH_FREE`. → `test_back_height_fits_compartment` con `PAPER_STACK` (Task 4).
3. **Ghiera che si apre da sola** col peso della busta piena / vibrazioni: deve restare chiusa finché non la giri a mano. → `test_ring_detent_blocks_unlock` (Task 4).
4. **Faccia anteriore non piana** se il bocchettone si appoggia: qualunque rilievo davanti rompe la tenuta. → `test_front_face_flat` (Task 3).
5. **Ingombro nelle zone di clip e linguetta di sicurezza**: nervature o manicotto lì impediscono la chiusura del coperchio. → `test_keepouts_clear` (Task 3 per la piastra, esteso in Task 4).
6. **Carta tra baionetta e ghiera**: se i denti della baionetta passano sopra la carta raccolta, la strappano e si intasano. La baionetta sta fuori dal diametro di serraggio (sul bordo esterno della flangia, oltre l'espanso) e la carta tocca solo il manicotto liscio e la faccia di pressione. → `test_bayonet_outside_clamp_zone` (Task 4).

---

### Task 1: Struttura del progetto, ambiente e skill

**Files:**
- Create: `CLAUDE.md`, `AGENTS.md` (symlink), `README.md`, `.gitignore`, `requirements.txt`, `docs/hardware_context.md`
- Create: `.agents/skills/{cad,cad-viewer,bambu-labs,dfam-check,step-parts}/`, `.claude/skills/*` (symlink), `skills-lock.json`

**Interfaces:**
- Produces: `.venv/bin/python` con `build123d` e `pytest`; comandi documentati in `CLAUDE.md`.

- [ ] **Step 1: `.gitignore`**: `__pycache__/`, `.venv/`, `output/`, `tmp/`, `.DS_Store`, `*.stl`, `*.step`, `*.3mf`.
- [ ] **Step 2: ambiente**: `python3.12 -m venv .venv && .venv/bin/pip install "build123d>=0.11" pytest`; `requirements.txt` con le due righe.
  Verifica: `.venv/bin/python -c "import build123d, pytest"` → nessun errore.
- [ ] **Step 3: skill**: dalla radice del progetto `npx -y skills add earthtojake/text-to-cad --skill cad --skill cad-viewer --skill bambu-labs --skill dfam-check --skill step-parts -y` (stessa sorgente e stesso `skills-lock.json` del portacarte; se la CLI non mette i file in `.agents/skills/`, spostarli lì). Poi per ognuna `ln -s ../../.agents/skills/<nome> .claude/skills/<nome>`.
  Verifica: `for s in cad cad-viewer bambu-labs dfam-check step-parts; do test -f .claude/skills/$s/SKILL.md || echo MISSING $s; done` → nessun output.
- [ ] **Step 4: `CLAUDE.md`** sul modello di `../magsafe-cardholder/CLAUDE.md` + le sue regole `AGENTS.md` (pipeline, tolleranze, sistema di riferimento, `./build.sh` dopo ogni modifica, `checks/check_fit.py`), adattate a questo pezzo; `ln -s CLAUDE.md AGENTS.md`.
  Verifica: `test -L AGENTS.md && wc -c CLAUDE.md` → < 24000.
- [ ] **Step 5: `docs/hardware_context.md`**: vincoli fisici dalla spec (GL-40, supporto 00495701 con clip e linguetta di sicurezza, A1 mini, PETG, buste kraft). `README.md` breve: cosa è, `./build.sh`, misure.
- [ ] **Step 6: Commit** `chore: struttura progetto, venv e skill 3D`.

### Task 2: Scheda misure e raccolta (CANCELLO UTENTE)

**Files:**
- Create: `docs/measurements.md`, `assets/images/riferimento-misure.svg`

**Interfaces:**
- Produces: tabella lettera → costante `config.py` → valore misurato; usata da Task 3 e 4.

- [ ] **Step 1: disegno di riferimento** `assets/images/riferimento-misure.svg`: contorno del cartoncino (da `assets/images/cartoncino-originale.jpg`) con quote a lettere.
- [ ] **Step 2: `docs/measurements.md`** con una riga per misura e colonna valore vuota:

| Lettera | Cosa | Costante |
|---|---|---|
| A1 / A2 / A3 | larghezza piastra in alto e in basso, lato inclinato | `PLATE_W_TOP`, `PLATE_W_BOTTOM`, `SIDE_TAPER` |
| B | altezza piastra (senza alette) | `PLATE_H` |
| C | spessore cartoncino | `PLATE_T` |
| D | larghezza scanalatura a U | `U_W` |
| E | profondità U dal bordo superiore | `U_DEPTH` |
| F | larghezza aletta / G altezza aletta sopra il bordo | `TAB_W`, `TAB_H` |
| H | distanza bordo esterno → aletta | `TAB_X_INSET` |
| I, J | tacca laterale: assente sull'originale (confermato dall'utente), nessuna costante | — |
| K | diametro foro nel cartoncino | `HOLE_D` |
| L, M | centro foro: da bordo sinistro, da bordo inferiore | `HOLE_X_FROM_LEFT`, `HOLE_Y_FROM_BOTTOM` |
| N | diametro esterno bocchettone | `INLET_D` |
| O | il bocchettone entra nel foro? (sì/no) e di quanto | `INLET_ENTERS`, `INLET_DEPTH` |
| P | profondità libera dietro la piastra nel vano | `DEPTH_FREE` |
| Q | zone di clip e linguetta di sicurezza (rettangoli x/y dal centro foro) | `KEEPOUTS` |
| R | rilievi/bordi sul cartoncino (note) | — |
| S | la linguetta di sicurezza va solo lasciata libera, o la piastra deve premerla per sbloccare il coperchio? Se va premuta: punto e corsa | `INTERLOCK_PUSH` (zona in `KEEPOUTS` oppure battuta) |
| T, U | membrana originale: diametro esterno, spessore; è integra e riusabile? | `MEMBRANE_OD`, `MEMBRANE_T` |
| V | spessore della carta della busta piegata a 4 strati (come si raccoglie sul manicotto) | `PAPER_STACK` |
| W | spessore dell'espanso adesivo acquistato (2-5 mm) | `FOAM_T` |

  Più le istruzioni pratiche (misurare 3 volte, annotare la media; P con la piastra originale inserita e il calibro in profondità).
- [ ] **Step 3: Commit** `docs: scheda misure`.
- [ ] **Step 4: STOP — l'utente compila `docs/measurements.md`** e compra l'espanso adesivo prima del CAD (serve `FOAM_T`). Se `DEPTH_FREE < 20`: fermarsi e riprendere il design con l'utente. Se `O` = sì, nella spec si definisce la profondità del foro prima del Task 3. Se `S` dice che la linguetta va premuta, nella spec si aggiunge la battuta prima del Task 3.

### Task 3: Piastra e stampa di prova (CANCELLO UTENTE)

**Files:**
- Create: `src/config.py`, `src/generate_adapter.py`, `checks/check_fit.py`, `build.sh`, `src/patch_3mf.py`

**Interfaces:**
- Consumes: valori di `docs/measurements.md`.
- Produces: `create_plate() -> Part` (piastra con nervature e sede della guarnizione, senza manicotto), `create_trial_plate() -> Part` (contorno + foro + sede, spessore `PLATE_T`, senza nervature), `create_depth_gauge() -> Part` (cilindro cavo sottile, diametro previsto della ghiera, alto `DEPTH_FREE - DEPTH_MARGIN`, da stampare insieme alla piastra di prova per controllare la chiusura del coperchio), costanti `config.py`: quelle di Task 2 + `FIT_CLEARANCE=0.4`, `EDGE_CHAMFER`, `RIB_H`, `RIB_W`, `RIB_COUNT`, `SEAL_SEAT_D`, `SEAL_SEAT_DEPTH`.
  Sede guarnizione: recesso sulla faccia anteriore attorno al foro, `SEAL_SEAT_D = MEMBRANE_OD + FIT_CLEARANCE`, `SEAL_SEAT_DEPTH = MEMBRANE_T * 0.8` (la membrana sporge un poco e fa tenuta); se la membrana non è riusabile, stesse quote per l'O-ring o l'espanso scelto. Il resto della faccia anteriore resta piano.
  `build.sh [trial|full]`: `trial` esporta `output/trial_plate.stl`, `output/depth_gauge.stl` e `output/trial_plate.3mf`.

- [ ] **Step 1: test che falliscono** in `checks/check_fit.py`:

```python
from config import *
from generate_adapter import create_plate, create_trial_plate

def test_plate_thickness():
    bb = create_trial_plate().bounding_box()
    assert abs(bb.min.Z) < 1e-3 and abs(bb.max.Z - PLATE_T) < 1e-3

def test_plate_outline():
    bb = create_trial_plate().bounding_box()
    assert abs(bb.size.X - max(PLATE_W_TOP, PLATE_W_BOTTOM)) < 0.05
    assert abs(bb.size.Y - (PLATE_H + TAB_H)) < 0.05
    # la piastra può stringersi verso il basso: larghezza misurata 0.5 mm sopra il bordo inferiore
    y = bb.min.Y + 0.5
    xs = [bb.min.X + i * 0.1 for i in range(int(bb.size.X / 0.1) + 1)]
    p = create_trial_plate()
    inside = [x for x in xs if p.is_inside((x, y, PLATE_T / 2))]
    assert abs((max(inside) - min(inside)) - PLATE_W_BOTTOM) < 0.3

def test_hole_through_and_sized():
    p = create_trial_plate()
    r = HOLE_D / 2
    assert not p.is_inside((0, 0, PLATE_T / 2))
    assert not p.is_inside((r - 0.1, 0, PLATE_T / 2))
    assert p.is_inside((r + 0.3, 0, PLATE_T / 2))

def test_edge_chamfer_at_bed():
    # al piano del letto il contorno è rientrato di EDGE_CHAMFER
    p = create_trial_plate(); x_edge = p.bounding_box().max.X
    assert not p.is_inside((x_edge - EDGE_CHAMFER / 2, 0, 0.05))
    assert p.is_inside((x_edge - EDGE_CHAMFER / 2, 0, PLATE_T / 2))

def test_front_face_flat():
    p = create_plate()
    assert abs(p.bounding_box().min.Z) < 1e-3  # niente sotto Z=0
    r_out = SEAL_SEAT_D / 2 + 2
    assert p.is_inside((r_out, 0, 0.05)) and p.is_inside((-r_out, 0, 0.05))

def test_seal_seat():
    p = create_trial_plate(); r = (HOLE_D / 2 + SEAL_SEAT_D / 2) / 2
    assert not p.is_inside((r, 0, SEAL_SEAT_DEPTH / 2))
    assert p.is_inside((r, 0, SEAL_SEAT_DEPTH + 0.1))

def keepout_volume(part):
    # volume dei keepout come prismi a tutta altezza posteriore
    boxes = [Box(x1 - x0, y1 - y0, DEPTH_FREE, align=Align.MIN).moved(Location((x0, y0, PLATE_T)))
             for (x0, y0, x1, y1) in KEEPOUTS]
    return sum((part & b).volume for b in boxes)

def test_keepouts_clear():
    assert keepout_volume(create_plate()) < 1e-3

def test_ribs_present():
    assert create_plate().volume > create_trial_plate().volume
```

Run (dalla radice): `.venv/bin/python -m pytest checks/check_fit.py -v` con `pythonpath = src` in `pytest.ini`. Atteso: FAIL (import).
- [ ] **Step 2: `src/config.py`** con le misure reali e le costanti sopra; `KEEPOUTS` come lista di tuple `(x0, y0, x1, y1)` nel sistema del centro foro.
- [ ] **Step 3: `create_trial_plate()` e `create_plate()`** in `src/generate_adapter.py`: contorno (rettangolo + alette con tacche − U − foro) estruso `PLATE_T` da `Plane.XY`, smusso `EDGE_CHAMFER` solo sugli spigoli a Z=0. `create_plate()` aggiunge `RIB_COUNT` nervature radiali sul retro (Z da `PLATE_T` a `PLATE_T + RIB_H`) tagliate fuori da `KEEPOUTS` e dalle guide laterali.
- [ ] **Step 4:** pytest → PASS.
- [ ] **Step 5: `src/patch_3mf.py`**: copia di `../magsafe-cardholder/src/patch_3mf.py` con overrides strutturali al posto di quelli per la trasparenza: `wall_loops "4"`, `sparse_infill_density "40%"`, `sparse_infill_pattern "gyroid"`, `layer_height "0.16"`, `enable_support "0"`, `elefant_foot_compensation "0"`, `filament_type ["PETG"]` (in `filament_specific` le chiavi filamento come nel gemello). Shell top/bottom e temperature restano quelle del profilo Generic PETG.
- [ ] **Step 6: `build.sh`**: come il gemello (stessi profili A1 mini 0.4 / 0.16 Optimal / Generic PETG, niente `--arrange`); modalità `trial` e `full`; `set -e`; esegue pytest prima dell'export.
  Verifica: `./build.sh trial` → crea `output/trial_plate.3mf`, aprirlo con la skill `cad-viewer` per un controllo a vista.
- [ ] **Step 7: Commit** `feat: piastra e stampa di prova`.
- [ ] **Step 8: STOP — l'utente stampa `output/trial_plate.3mf`** e prova: scorre nelle guide, la clip aggancia le tacche, il bocchettone tiene sulla sede, il coperchio si chiude; poi con il calibro di profondità appoggiato dietro il foro il coperchio deve chiudersi ancora. Correzioni solo in `config.py` (es. `PLATE_T`, posizione tacche), rebuild, ripetere finché l'utente conferma. Annotare in `docs/hardware_context.md` le correzioni e il perché.

### Task 4: Manicotto, flangia e ghiera a quarto di giro

**Files:**
- Modify: `src/config.py`, `src/generate_adapter.py`, `checks/check_fit.py`, `build.sh`

**Interfaces:**
- Consumes: `create_plate()` (Task 3).
- Produces: `create_plate_with_sleeve() -> Part`, `create_ring() -> Part`, `ring_pose(ring: Part, angle_deg: float, z: float) -> Part` (ruota attorno a Z e trasla), costanti `SLEEVE_ID`, `SLEEVE_WALL`, `SLEEVE_H`, `FLANGE_OD`, `FLANGE_T`, `FOAM_T`, `PAPER_STACK`, `CLAMP_GAP`, `LUG_COUNT`, `LUG_W`, `LUG_RAMP_DEG`, `LOCK_ANGLE=90`, `DETENT_H`, `RING_H`, `SLEEVE_ROOT_FILLET=2.5`, `DEPTH_MARGIN=2.0`.
  `SLEEVE_ID >= HOLE_D`. `SLEEVE_ID` = il massimo che `KEEPOUTS`, piastra e `DEPTH_FREE` consentono (scelta spec). `CLAMP_GAP = FOAM_T * 0.5 + PAPER_STACK` (espanso compresso del 50%).

- [ ] **Step 1: test che falliscono**:

```python
def test_sleeve_not_restrictive():
    assert SLEEVE_ID >= HOLE_D

def test_back_height_fits_compartment():
    top = ring_pose(create_ring(), LOCK_ANGLE, z_locked()).bounding_box().max.Z
    assert top + PAPER_STACK + DEPTH_MARGIN <= PLATE_T + DEPTH_FREE

def test_ring_inserts_at_zero():
    base = create_plate_with_sleeve()
    for z in z_insert_path():   # dalla cima del manicotto alla posizione di battuta
        assert (base & ring_pose(create_ring(), 0, z)).volume < 1e-3

def test_ring_locked_no_interference_and_clamps():
    base, r = create_plate_with_sleeve(), ring_pose(create_ring(), LOCK_ANGLE, z_locked())
    assert (base & r).volume < 1e-3
    assert abs(clamp_gap_at_lock() - CLAMP_GAP) < 0.1

def test_ring_detent_blocks_unlock():
    # il fermo si scavalca solo comprimendo l'espanso: il dente deve salire più del gioco libero
    assert FIT_CLEARANCE < DETENT_H <= FOAM_T * 0.5

def test_bayonet_outside_clamp_zone():
    # la carta sta tra SLEEVE_OD e il bordo dell'espanso: i denti della ghiera restano oltre
    assert ring_lug_inner_r() >= FLANGE_OD / 2 + FIT_CLEARANCE

def test_keepouts_clear_with_sleeve():
    assert keepout_volume(create_plate_with_sleeve()) < 1e-3
    assert keepout_volume(ring_pose(create_ring(), LOCK_ANGLE, z_locked())) < 1e-3

def test_parts_fit_bed():
    for p in (create_plate_with_sleeve(), create_ring()):
        bb = p.bounding_box(); assert max(bb.size.X, bb.size.Y) <= 175 or (bb.size.X**2 + bb.size.Y**2) ** 0.5 <= 250
```

  `z_locked()`, `z_insert_path()` (5-10 quote, non di più: i booleani sono lenti), `clamp_gap_at_lock()`, `ring_lug_inner_r()` sono helper in `generate_adapter.py` derivati dalle costanti (non numeri nei test).
  Run: pytest → FAIL.
- [ ] **Step 2: geometria**: manicotto cilindrico liscio coassiale (Z da `PLATE_T`), flangia di battuta alla base (`FLANGE_OD`, `FLANGE_T`) per l'espanso, raccordo `SLEEVE_ROOT_FILLET` alla radice. Sul bordo esterno della flangia, oltre l'espanso, un collare con `LUG_COUNT` scanalature a L (tratto assiale + tratto a rampa `LUG_RAMP_DEG` per `LOCK_ANGLE`) e dente di fermo `DETENT_H` a fine corsa. Ghiera a tazza: faccia anulare piana che preme la carta contro l'espanso, gonna esterna con `LUG_COUNT` denti interni che entrano nel collare, esterno zigrinato per la presa. Così la carta tocca solo il manicotto e la faccia di pressione. Gioco `FIT_CLEARANCE` su tutte le superfici di scorrimento. Stampabile senza supporti: ghiera stampata con faccia di pressione sul piatto, rampe ≤ 45° di sbalzo.
- [ ] **Step 3:** pytest → PASS.
- [ ] **Step 4: `build.sh full`** esporta `plate.step/stl`, `ring.step/stl` e i `*_offset.stl` affiancati con 5 mm di distanza → `output/bag_adapter_petg.3mf`. Controllo stampabilità con la skill `dfam-check` sugli STEP; vista con `cad-viewer`.
- [ ] **Step 5: docs**: `README.md` (pezzi, montaggio busta, espanso adesivo da comprare: spessore `FOAM_T`, larghezza ≥ `(FLANGE_OD - SLEEVE_ID)/2`), `docs/hardware_context.md`, `CLAUDE.md` se cambiano comandi.
- [ ] **Step 6: Commit** `feat: manicotto e ghiera a quarto di giro`.

### Task 5: Stampa completa e prova reale (CANCELLO UTENTE)

- [ ] **Step 1:** l'utente stampa `output/bag_adapter_petg.3mf`, incolla l'espanso sulla flangia, monta una busta kraft (bocca raccolta a pieghe sul manicotto, ghiera a 1/4 di giro).
- [ ] **Step 2: prova**: inserimento nel supporto, chiusura coperchio, 1 minuto di aspirazione su farina o polvere fine, controllo a occhio di polvere nel vano fuori dalla busta; tirare la busta piena per verificare che non si sfili né che la ghiera si sblocchi.
- [ ] **Step 3:** correzioni in `config.py` → rebuild → pytest; lezioni pratiche (tolleranze reali, comportamento della carta) in `docs/hardware_context.md`. Commit `fix: correzioni dopo prova reale`.
