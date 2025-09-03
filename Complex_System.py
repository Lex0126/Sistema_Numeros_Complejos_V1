"""
Sistema para generar números complejos en forma binómica y trigonométrica,
con funciones de verificación.

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import math
import random

@dataclass
class Complejo:
    a: float  # parte real
    b: float  # parte imaginaria

    @property
    def binomica(self) -> Tuple[float, float]:
        """Retorna (a, b)."""
        return (self.a, self.b)

    @property
    def modulo(self) -> float:
        """r = |z| = sqrt(a^2 + b^2)"""
        return math.hypot(self.a, self.b)

    @property
    def argumento(self) -> float:
        """θ = atan2(b, a), normalizado a [0, 2π)."""
        theta = math.atan2(self.b, self.a)
        if theta < 0:
            theta += 2 * math.pi
        return theta

    @property
    def trigonometrica(self) -> Tuple[float, float]:
        """Retorna (r, θ) con r ≥ 0 y θ en [0, 2π)."""
        return (self.modulo, self.argumento)

    @staticmethod
    def desde_trigonometrica(r: float, theta: float) -> "Complejo":
        """Construye un complejo desde (r, θ). θ puede ser cualquier real; se normaliza."""
        # Normalizamos θ a [0, 2π) solo para consistencia (no es estrictamente necesario)
        tau = 2 * math.pi
        theta_norm = theta % tau
        a = r * math.cos(theta_norm)
        b = r * math.sin(theta_norm)
        return Complejo(a, b)

    def casi_igual(self, otro: "Complejo", tol: float = 1e-9) -> bool:
        """Compara dos complejos con tolerancia absoluta."""
        return math.isclose(self.a, otro.a, rel_tol=0.0, abs_tol=tol) and \
               math.isclose(self.b, otro.b, rel_tol=0.0, abs_tol=tol)


def generar_complejos_aleatorios(n: int,
                                 rango_a: Tuple[int, int] = (-10, 10),
                                 rango_b: Tuple[int, int] = (-10, 10),
                                 semilla: Optional[int] = None) -> List[Complejo]:
    """
    Genera 'n' números complejos con partes enteras.
    """
    if semilla is not None:
        random.seed(semilla)
    a_min, a_max = rango_a
    b_min, b_max = rango_b
    datos = []
    for _ in range(n):
        a = random.randint(a_min, a_max)
        b = random.randint(b_min, b_max)
        datos.append(Complejo(a, b))
    return datos



def verificar_conversion(z: Complejo, tol: float = 1e-9) -> Tuple[bool, Complejo, Tuple[float, float]]:
    """
    Verifica que convertir z=(a,b) a trigonométrica y de vuelta a binómica
    recupera el mismo número (dentro de una tolerancia).
    Retorna (ok, z_reconstruido, (r, θ)).
    """
    r, theta = z.trigonometrica
    z2 = Complejo.desde_trigonometrica(r, theta)
    ok = z.casi_igual(z2, tol=tol)
    return ok, z2, (r, theta)


def a_grados(theta_rad: float) -> float:
    """Convierte radianes a grados en [0, 360)."""
    deg = math.degrees(theta_rad) % 360.0
    if deg < 0:
        deg += 360.0
    return deg


# Ejemplo rápido si se ejecuta este archivo directamente
if __name__ == "__main__":
    muestras = generar_complejos_aleatorios(5, semilla=42)
    for z in muestras:
        ok, z2, (r, th) = verificar_conversion(z)
        print(f"a+bi=({z.a:.6f}, {z.b:.6f}) | r∠θ=({r:.6f}, {th:.6f} rad ≈ {a_grados(th):.3f}°) | "
              f"reconstruido=({z2.a:.6f}, {z2.b:.6f}) | ok={ok}")