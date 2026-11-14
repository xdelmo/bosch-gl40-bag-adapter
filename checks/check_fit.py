from config import *
from generate_adapter import create_trial_plate


def test_plate_thickness():
    bb = create_trial_plate().bounding_box()
    assert abs(bb.min.Z) < 1e-3 and abs(bb.max.Z - PLATE_T) < 1e-3


def test_plate_outline():
    bb = create_trial_plate().bounding_box()
    assert abs(bb.size.X - max(PLATE_W_TOP, PLATE_W_BOTTOM)) < 0.05
    assert abs(bb.size.Y - (PLATE_H + TAB_H)) < 0.05
    # Foro all'origine: bordo inferiore a -HOLE_Y_FROM_BOTTOM, sagoma simmetrica in X
    assert abs(bb.min.Y + HOLE_Y_FROM_BOTTOM) < 0.05
    assert abs(bb.min.X + bb.max.X) < 0.05
    # La piastra può stringersi verso il basso: larghezza misurata 0.5 mm sopra il bordo inferiore
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
    # Al piano del letto (Z=0.05) il contorno è rientrato di EDGE_CHAMFER.
    # Si usa y=64 vicino al bordo superiore dove il lato destro è a bb.max.X.
    p = create_trial_plate()
    x_edge = p.bounding_box().max.X
    y = 64.0
    assert not p.is_inside((x_edge - EDGE_CHAMFER / 2, y, 0.05))
    assert p.is_inside((x_edge - EDGE_CHAMFER / 2, y, PLATE_T / 2))


def test_top_width():
    # Larghezza 0.5 mm sotto il bordo superiore (fuori dalla U):
    # verifica che il punto (±(PLATE_W_TOP/2 - 0.3), 64.5, PLATE_T/2) sia dentro e (±(PLATE_W_TOP/2 + 0.3), 64.5, ...) fuori.
    p = create_trial_plate()
    y = 64.5
    assert p.is_inside((PLATE_W_TOP / 2 - 0.3, y, PLATE_T / 2))
    assert p.is_inside((-(PLATE_W_TOP / 2 - 0.3), y, PLATE_T / 2))
    assert not p.is_inside((PLATE_W_TOP / 2 + 0.3, y, PLATE_T / 2))
    assert not p.is_inside((-(PLATE_W_TOP / 2 + 0.3), y, PLATE_T / 2))


def test_u_slot():
    p = create_trial_plate()
    # (0, 65 - U_DEPTH + 0.3, PLATE_T/2) fuori; (0, 65 - U_DEPTH - 0.5, PLATE_T/2) dentro
    assert not p.is_inside((0, 65 - U_DEPTH + 0.3, PLATE_T / 2))
    assert p.is_inside((0, 65 - U_DEPTH - 0.5, PLATE_T / 2))
    # Larghezza: a y=60 la U (cerchio r=U_W/2 centrato a y=65.5) è larga 2*sqrt(22.5²-5.5²) ≈ 43.6
    assert not p.is_inside((21.5, 60, PLATE_T / 2))
    assert p.is_inside((22.2, 60, PLATE_T / 2))


def test_tabs():
    p = create_trial_plate()
    # (±36.5, 65 + TAB_H/2, PLATE_T/2) dentro; (±(30.5 - 0.3), 65 + 0.5, ...) e (0, 66, ...) fuori
    assert p.is_inside((36.5, 65 + TAB_H / 2, PLATE_T / 2))
    assert p.is_inside((-36.5, 65 + TAB_H / 2, PLATE_T / 2))
    assert not p.is_inside((30.5 - 0.3, 65 + 0.5, PLATE_T / 2))
    assert not p.is_inside((-(30.5 - 0.3), 65 + 0.5, PLATE_T / 2))
    assert not p.is_inside((0, 66, PLATE_T / 2))
    # Bordo esterno a 42.5 e fianco a 45°: a y=67.5 il fianco esterno è a x=40.0
    assert not p.is_inside((42.8, 65.5, PLATE_T / 2))
    assert p.is_inside((39.7, 67.5, PLATE_T / 2))
    assert not p.is_inside((40.3, 67.5, PLATE_T / 2))
