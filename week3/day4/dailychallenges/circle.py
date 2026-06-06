# ============================================================
#  Circle Class — OOP & Dunder Methods Assignment
# ============================================================
import math


class Circle:
    """A class representing a circle, defined by its radius."""

    # ── Constructor ──────────────────────────────────────────
    def __init__(self, radius):
        self.radius = radius

    # ── Class method (decorator) — alternative constructor ───
    @classmethod
    def from_diameter(cls, diameter):
        """Create a Circle from a diameter instead of a radius."""
        return cls(diameter / 2)

    # ── Property — compute diameter on the fly ───────────────
    @property
    def diameter(self):
        return self.radius * 2

    # ── Ability 1: Compute area ──────────────────────────────
    def area(self):
        return math.pi * self.radius ** 2

    # ── Ability 2: Human-readable string (__str__) ───────────
    def __str__(self):
        return (f"Circle(radius={self.radius}, "
                f"diameter={self.diameter}, "
                f"area={self.area():.2f})")

    # ── __repr__ (used in lists / debugging) ─────────────────
    def __repr__(self):
        return f"Circle(radius={self.radius})"

    # ── Ability 3: Add two circles → new circle (__add__) ────
    def __add__(self, other):
        return Circle(self.radius + other.radius)

    # ── Ability 4: Greater-than comparison (__gt__) ──────────
    def __gt__(self, other):
        return self.radius > other.radius

    # ── Ability 5: Equality comparison (__eq__) ──────────────
    def __eq__(self, other):
        return self.radius == other.radius

    # ── Ability 6: Less-than for sorting (__lt__) ────────────
    def __lt__(self, other):
        return self.radius < other.radius


# ── Test / demo ──────────────────────────────────────────────
if __name__ == "__main__":

    # Create circles
    c1 = Circle(5)
    c2 = Circle(3)
    c3 = Circle.from_diameter(16)   # radius = 8
    c4 = Circle(3)

    print("=== Circles ===")
    print(c1)
    print(c2)
    print(c3)

    print("\n=== Area ===")
    print(f"c1 area: {c1.area():.2f}")
    print(f"c3 area: {c3.area():.2f}")

    print("\n=== Addition ===")
    c5 = c1 + c2          # radius 5 + 3 = 8
    print(f"c1 + c2 = {c5}")

    print("\n=== Comparisons ===")
    print(f"c1 > c2  → {c1 > c2}")    # True
    print(f"c2 > c1  → {c2 > c1}")    # False
    print(f"c2 == c4 → {c2 == c4}")   # True  (both radius 3)
    print(f"c1 == c2 → {c1 == c2}")   # False

    print("\n=== Sorting ===")
    circles = [c1, c2, c3, c4]
    print("Before:", circles)
    circles_sorted = sorted(circles)
    print("After: ", circles_sorted)
