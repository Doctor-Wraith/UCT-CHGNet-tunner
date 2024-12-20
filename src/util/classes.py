from dataclasses import dataclass
from typing import Optional


class Vector2D:
    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)

    def __dict__(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
        }


class Vector3D:

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value: float):
        self._z = float(value)

    def __dict__(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }


class Position(Vector3D):

    @property
    def position_type(self) -> str:
        return self._position_type

    @position_type.setter
    def position_type(self, value: str):
        self._position_type = value

    def __str__(self) -> str:
        return f"Position:\n\tx: {self.x}\n\ty: {self.y}\n\tz: {self.z}"


class Force(Vector3D):
    def __str__(self) -> str:
        return f"Forces:\n\tx: {self.x}\n\ty: {self.y}\n\tz: {self.z}"


@dataclass
class Atom:
    name: str
    count: int
    surface: bool
    locations: Optional[list[Position]]
    forces: Optional[list[Force]]
