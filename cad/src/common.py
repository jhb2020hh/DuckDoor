"""Gemeinsame Schnittstelle für das CAD-Modell DuckDoor (CadQuery).

Koordinatensystem (identisch mit TZ-01/TZ-02):
  x = 0  Mitte Lichtöffnung (quer zur Durchgangsrichtung)
  y = 0  Mittelebene Schieber; +y = Entenseite (Gehege), -y = Raubtierseite
  z = 0  Oberkante Fundament (OKF); Gelände = -20
Einheiten: mm. Dargestellter Zustand: ZU_VERRIEGELT (Bolzen z = +594).

Jedes Teilmodul (parts_*.py) stellt bereit:
    def build() -> list[Part]
Die Geometrie wird direkt in GLOBALEN Koordinaten erzeugt (keine Mates nötig).
"""
from dataclasses import dataclass, field
import cadquery as cq


@dataclass
class Part:
    name: str               # eindeutiger Bauteilname, z. B. "P07_Pfosten_links"
    pos: str                # Positionsnummer lt. drawings/TZ_Positionsliste.csv bzw. BMK
    shape: cq.Workplane     # Geometrie in globalen Koordinaten
    material: str
    group: str              # Unterbaugruppe: GRUENDUNG, GESTELL, FUEHRUNG, SCHIEBER, ANTRIEB, KASTEN, ELEKTRO, KAUFTEIL
    color: tuple = (0.7, 0.7, 0.7)   # RGB 0..1
    kaufteil: bool = False
    note: str = ""


# Farben (Darstellung)
C_BETON = (0.65, 0.65, 0.62)
C_STAHL_VZ = (0.55, 0.58, 0.60)
C_ALU = (0.80, 0.82, 0.85)
C_EDELSTAHL = (0.70, 0.72, 0.74)
C_KUNSTSTOFF_W = (0.95, 0.95, 0.92)
C_KUNSTSTOFF_S = (0.15, 0.15, 0.15)
C_GUMMI = (0.10, 0.10, 0.10)
C_KAUFTEIL = (0.20, 0.35, 0.60)
C_WARN = (0.95, 0.80, 0.10)


def box(x0, x1, y0, y1, z0, z1) -> cq.Workplane:
    """Quader aus Min/Max-Koordinaten (global)."""
    return (cq.Workplane("XY")
            .box(x1 - x0, y1 - y0, z1 - z0, centered=False)
            .translate((min(x0, x1), min(y0, y1), min(z0, z1))))


def cyl_z(x, y, z0, z1, d) -> cq.Workplane:
    """Zylinder entlang z."""
    return cq.Workplane("XY").circle(d / 2).extrude(z1 - z0).translate((x, y, z0))


def cyl_y(x, z, y0, y1, d) -> cq.Workplane:
    """Zylinder entlang y."""
    return (cq.Workplane("XZ").circle(d / 2).extrude(-(y1 - y0))
            .translate((x, y0, z)))
