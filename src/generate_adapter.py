import os
from build123d import *
from config import *


def create_trial_plate() -> Part:
    """Crea la piastra di prova sottile (spessore PLATE_T) con solo profilo esterno, alette, scanalatura a U e foro."""
    y_bottom = -HOLE_Y_FROM_BOTTOM
    y_top = PLATE_H - HOLE_Y_FROM_BOTTOM

    with BuildPart() as bp:
        with BuildSketch(Plane.XY):
            # Contorno trapezoidale isoscele centrato in X
            Polygon([
                (-PLATE_W_BOTTOM / 2, y_bottom),
                (PLATE_W_BOTTOM / 2, y_bottom),
                (PLATE_W_TOP / 2, y_top),
                (-PLATE_W_TOP / 2, y_top),
            ])
            # Alette sul bordo superiore: trapezi con fianchi a 45°, base da x_in a x_out (30.5..42.5)
            x_out = PLATE_W_TOP / 2 - TAB_X_INSET
            x_in = x_out - TAB_W
            for sx in (1, -1):
                Polygon([
                    (sx * x_in, y_top),
                    (sx * x_out, y_top),
                    (sx * (x_out - TAB_H), y_top + TAB_H),
                    (sx * (x_in + TAB_H), y_top + TAB_H),
                ])
            # Scanalatura a U: cerchio di raggio U_W/2 centrato in x=0, y=65-U_DEPTH+U_W/2
            u_y_center = y_top - U_DEPTH + U_W / 2
            with Locations((0, u_y_center)):
                Circle(radius=U_W / 2, mode=Mode.SUBTRACT)

            # Foro passante Ø HOLE_D centrato in (0,0)
            Circle(radius=HOLE_D / 2, mode=Mode.SUBTRACT)

        # Estrusione Z 0 -> PLATE_T da Plane.XY
        extrude(amount=PLATE_T)

        # Smusso anti piede d'elefante SOLO sugli spigoli a Z=0 (faccia sul piatto)
        bed_edges = bp.edges().filter_by(
            lambda e: abs(e.bounding_box().min.Z) < 1e-5 and abs(e.bounding_box().max.Z) < 1e-5
        )
        chamfer(bed_edges, length=EDGE_CHAMFER)

    return bp.part


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    trial_plate = create_trial_plate()
    export_step(trial_plate, "output/trial_plate.step")
    export_stl(trial_plate, "output/trial_plate.stl")
    print("Esportati con successo output/trial_plate.step e output/trial_plate.stl")
