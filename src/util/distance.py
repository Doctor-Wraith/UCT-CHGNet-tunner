from .classes import Vector3D


def distance(v1:Vector3D, v2:Vector3D) -> float:
    x = (v1.x - v2.x)**2
    y = (v1.y - v2.y)**2
    z = (v1.z - v2.z)**2

    return (x+y+z)**(0.5)