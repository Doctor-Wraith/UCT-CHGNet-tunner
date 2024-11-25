from dataclasses import dataclass
from typing import Literal


@dataclass
class Atom:
    atom_id: str
    atom_name: str


@dataclass
class Tunning:
    tunning_id: str
    surface: Atom
    adsorbate_1: Atom | None
    adsorbate_2: Atom | None
    adsorbate_3: Atom | None
    Energy: float
    outcar_path: str
    training: bool


@dataclass
class Position:
    position_id: str
    atom: Atom
    tunning: Tunning
    position_type: Literal["cartesian", "direct"]
    x: float
    y: float
    z: float


@dataclass
class Force:
    force_id: str
    atom: Atom
    tunning: Tunning
    x: float
    y: float
    z: float
