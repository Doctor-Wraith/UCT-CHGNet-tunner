class Vector:
    
    @property
    def x(self) -> float:
        return self._x
    
    @x.setter
    def x(self, value:float) -> None:
        self._x = value
    
    @property
    def y(self) -> float:
        return self._y
    
    @y.setter
    def y(self, value:float) -> None:
        self._y = value
    
    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, value:float):
        self._z = value

    def __dict__(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

class Position(Vector):
    def __str__(self) -> str:
        return f"Position:\n\tx: {self.x}\n\ty: {self.y}\n\tz: {self.z}"

class Force(Vector):
    def __str__(self) -> str:
        return f"Forces:\n\tx: {self.x}\n\ty: {self.y}\n\tz: {self.z}"