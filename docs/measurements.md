# Scheda Misure e Raccolta Quote — Adattatore Bosch GL-40

> **CANCELLO UTENTE (Task 2)**: Prima di procedere con la modellazione CAD (Task 3 e successivi), compilare la tabella sottostante inserendo le misure rilevate con il calibro sul cartoncino originale del sacchetto e nel vano dell'aspirapolvere Bosch GL-40 (Hair Animal).
> Fare riferimento allo schema grafico quotato in [`assets/images/riferimento-misure.svg`](../assets/images/riferimento-misure.svg).

---

## 1. Istruzioni Pratiche di Misurazione

1. **Ripetibilità delle misure (Media su 3 letture)**:
   - Misurare ogni quota **3 volte** con un calibro a corsoio (digitale o ventesimale).
   - Annotare nella tabella la **media aritmetica** delle 3 letture per annullare errori di lettura e compensare eventuali deformazioni o usura del cartoncino originale.
2. **Quota P (Profondità libera vano — Calibro di profondità)**:
   - Inserire la piastra di cartoncino originale nell'alloggiamento di supporto in plastica (codice ricambio Bosch 00495701) all'interno del vano dell'aspirapolvere, assicurandosi che sia completamente a fondo corsa nelle guide.
   - Utilizzare l'**astina di profondità del calibro** appoggiando il fusto del calibro sulla faccia posteriore del cartoncino e spingendo l'astina fino a toccare la parete posteriore o il primo ostacolo del vano.
   - Rilevare la quota `P` (`DEPTH_FREE`) in più punti attorno alla zona centrale per individuare il punto più restrittivo.
3. **Quota Q (Zone di rispetto / Keep-outs)**:
   - Individuare la posizione delle guide laterali, della clip di fermo superiore e della linguetta di sicurezza dell'alloggiamento 00495701.
   - Esprimere ogni zona di keep-out come un rettangolo definito da `[x0, y0, x1, y1]` in millimetri, riferito al **sistema di coordinate globale** con **origine (X=0, Y=0) posizionata al centro del foro di aspirazione**:
     - Asse **+X**: orientato verso destra.
     - Asse **+Y**: orientato verso l'alto (verso le alette e la scanalatura a U).
     - Asse **+Z**: orientato verso il retro (verso il sacchetto e l'interno del vano).
4. **Quota V (Spessore carta sacchetto arricciata)**:
   - Prendere una delle buste kraft universali acquistate (prive di cartoncino proprio).
   - Piegare la carta a **4 strati** per simulare le pieghe e l'arricciatura che la bocca della busta formerà attorno al manicotto cilindrico quando verrà serrata dalla ghiera.
   - Posizionare i 4 strati tra i becchi del calibro e chiuderli **delicatamente a contatto**, senza stringere né comprimere le fibre della carta, registrando lo spessore a riposo.
5. **Acquisto Guarnizione Adesiva (Quota W)**:
   - Acquistare una striscia o nastro di gomma/espanso adesivo a cellule chiuse (spessore nominale consigliato tra 2 e 5 mm) per la tenuta frontale della carta sul manicotto.
   - Misurare lo spessore a riposo senza comprimere l'adesivo e riportarlo in `W` (`FOAM_T`).

---

## 2. Cancelli Decisionali Obbligatori (Gating Checks)

Prima di passare alla fase CAD, verificare scrupolosamente i seguenti tre cancelli:

* 🛑 **CANCELLO P (`DEPTH_FREE >= 20 mm`)**:
  Se la profondità libera misurata `P` dietro la piastra è **inferiore a 20 mm**, **ARRESTO IMMEDIATO DEI LAVORI**.
  Con meno di 20 mm di spazio utile, il manicotto cilindrico, la flangia di battuta e la ghiera a baionetta non possono fisicamente coesistere con la chiusura del vano. In tal caso è necessario fermarsi e ridiscutere l'architettura del meccanismo di serraggio con l'utente.

* ⚠️ **CANCELLO O (`INLET_ENTERS`)**:
  Se il bocchettone maschio dell'aspirapolvere penetra all'interno del foro del cartoncino (`O = sì`), occorre indicare la quota esatta di penetrazione `INLET_DEPTH` in mm. In questo caso, prima del Task 3 andrà aggiornata la specifica per prevedere una svasatura/recesso interno nel manicotto ed evitare interferenze meccaniche. Se non penetra (`O = no`), il bocchettone va in battuta piana frontale contro la guarnizione a filo piastra.

* ⚠️ **CANCELLO S (`INTERLOCK_PUSH`)**:
  Verificare la funzione della linguetta di sicurezza del supporto 00495701:
  - Se serve solo non interferire con essa: va inserita nelle zone di rispetto `Q` (`KEEPOUTS`).
  - Se invece la piastra deve premerla fisicamente per disimpegnare l'interblocco e consentire la chiusura del coperchio: indicare le coordinate del punto di contatto e la corsa di spinta richiesta. Prima del Task 3 andrà aggiunta al modello una sporgenza/battuta di azionamento dedicata.

---

## 3. Tabella Raccolta Misure

> **Nota**: Compilare la colonna **Valore (mm)** con i dati misurati. Lasciare note chiarificatrici nell'ultima colonna in caso di asimmetrie o particolarità.

| Lettera | Cosa | Costante | Valore (mm) | Note |
|---|---|---|---|---|
| **A1** | Larghezza piastra in alto | `PLATE_W_TOP` | 98 | Subito sotto le alette, da spigolo a spigolo |
| **A2** | Larghezza piastra in basso | `PLATE_W_BOTTOM` | 90 | Lungo il bordo inferiore. A1 ≠ A2: la piastra si stringe verso il basso di 8 mm, come nella foto |
| **A3** | Quale lato è inclinato | `SIDE_TAPER` | entrambi (da confermare) | Dalla foto raddrizzata (era ruotata di ~1,5°) i lati sono simmetrici, ~4 mm per lato (~2,2°). Per confermare: `sinistro`, `destro` o `entrambi`: appoggia una squadra sul bordo inferiore e guarda quale lato se ne stacca |
| **B** | Altezza piastra (escluse alette) | `PLATE_H` | | Lungo il lato dritto, dal bordo inferiore al bordo superiore |
| **C** | Spessore nominale cartoncino | `PLATE_T` | 1.5 | Misurato su bordo non schiacciato (sarà lo spessore piastra) |
| **D** | Larghezza scanalatura a U | `U_W` | 45 | Larghezza dell'apertura a U sul bordo superiore |
| **E** | Profondità scanalatura a U | `U_DEPTH` | 22 | Distanza dal bordo superiore al punto più basso della U |
| **F** | Larghezza singola aletta | `TAB_W` | 12 | Larghezza dell'aletta superiore |
| **G** | Altezza aletta sopra il bordo | `TAB_H` | 3 | Sporgenza verticale dell'aletta oltre il bordo superiore |
| **H** | Distanza bordo esterno → aletta | `TAB_X_INSET` | 6.5 | Rientro dell'aletta rispetto allo spigolo laterale |
| **I** | Profondità tacca laterale | `NOTCH_D` | — (assente) | Il cartoncino originale non ha tacche laterali (confermato dall'utente) |
| **J** | Posizione tacca dal bordo sup. | `NOTCH_Z` | — (assente) | Il cartoncino originale non ha tacche laterali (confermato dall'utente) |
| **K** | Diametro foro aspirazione | `HOLE_D` | 50 | Diametro interno del foro nel cartoncino |
| **L** | Centro foro da bordo sinistro | `HOLE_X_FROM_LEFT` | | Distanza orizzontale bordo sinistro → asse foro, misurata all'altezza del foro (il lato può essere inclinato) |
| **M** | Centro foro da bordo inferiore | `HOLE_Y_FROM_BOTTOM` | 40 | Distanza verticale bordo inferiore → asse foro |
| **N** | Diametro esterno bocchettone | `INLET_D` | | Diametro esterno del tubo di aspirazione macchina |
| **O** | Bocchettone entra nel foro? | `INLET_ENTERS` / `INLET_DEPTH` | | `sì` (indicare mm penetrazione) oppure `no` (battuta piana) |
| **P** | Profondità libera dietro piastra | `DEPTH_FREE` | | **CANCELLO CRITICO**: se < 20 mm stop immediato |
| **Q** | Zone di rispetto clip e blocco | `KEEPOUTS` | | Rettangoli `[x0, y0, x1, y1]` dal centro foro (0,0) |
| **R** | Rilievi / bordi / pieghe | — | | Note su rilievi o guide sul cartoncino originale |
| **S** | Linguetta sicurezza: va premuta? | `INTERLOCK_PUSH` | | `libera` oppure `va premuta` (indicare punto e corsa) |
| **T** | Membrana originale: diametro est. | `MEMBRANE_OD` | | Diametro esterno della guarnizione in gomma originale |
| **U** | Membrana originale: spessore | `MEMBRANE_T` | | Spessore guarnizione e stato (integra e riusabile?) |
| **V** | Spessore carta busta (4 strati) | `PAPER_STACK` | | Misurata a contatto senza compressione |
| **W** | Spessore espanso adesivo | `FOAM_T` | | Spessore a riposo nastro adesivo acquistato (2-5 mm) |
