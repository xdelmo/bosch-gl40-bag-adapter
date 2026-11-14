# src/config.py
# Quote dimensionali misurate (mm) e costanti geometriche per l'adattatore Bosch GL-40.
# Origine: centro del foro di aspirazione (X=0, Y=0), Z=0 faccia anteriore a contatto con il piatto di stampa.
# +Z verso l'interno vano / sacchetto; +Y verso la scanalatura a U e le alette superiori.

# Piastra (misure rilevate dal cartoncino originale)
PLATE_W_TOP = 98.0         # Larghezza bordo superiore (senza alette)
PLATE_W_BOTTOM = 90.0      # Larghezza bordo inferiore (lati inclinati simmetrici)
PLATE_H = 105.0            # Altezza totale piastra (senza alette)
PLATE_T = 1.5              # Spessore nominale piastra

# Scanalatura superiore a U
U_W = 45.0                 # Larghezza massima scanalatura
U_DEPTH = 22.0             # Profondità rientro dal bordo superiore

# Alette superiori di guida / aggancio
TAB_W = 12.0               # Larghezza base aletta
TAB_H = 3.0                # Altezza aletta oltre il bordo superiore
TAB_X_INSET = 6.5          # Distanza tra spigolo superiore piastra e inizio aletta

# Foro aspirazione
HOLE_D = 50.0              # Diametro foro passante
HOLE_X_FROM_LEFT = 47.0    # Distanza centro foro dal bordo sinistro a metà altezza (foro centrato)
HOLE_Y_FROM_BOTTOM = 40.0  # Quota centro foro dal bordo inferiore

# Tolleranze e parametri di stampa FDM
FIT_CLEARANCE = 0.4
EDGE_CHAMFER = min(0.5, PLATE_T * 0.25)  # 0.375 mm - smusso anti zampa d'elefante sul piatto

# NOTA: Le misure del vano (DEPTH_FREE, INLET_*, KEEPOUTS, MEMBRANE_*) mancano ancora: non aggiungerle.
