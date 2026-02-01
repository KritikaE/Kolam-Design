import numpy as np

class KolamEngine:
    def __init__(self, size=5, spacing=1):
        self.size = size
        self.spacing = spacing
        # Default square grid
        self.dots = self._generate_square_grid()

    def _generate_square_grid(self):
        x = np.linspace(0, (self.size - 1) * self.spacing, self.size)
        y = np.linspace(0, (self.size - 1) * self.spacing, self.size)
        xv, yv = np.meshgrid(x, y)
        return xv, yv

    def generate_staggered_grid(self):
        """
        Implements the 'Idai Pulli' (Triangular/Hexagonal) grid.
        This places dots in the gaps of the previous row.
        """
        x_coords = []
        y_coords = []
        for r in range(self.size):
            # Every other row is shifted by half the spacing
            offset = (self.spacing / 2) if r % 2 != 0 else 0
            for c in range(self.size):
                x_coords.append(c * self.spacing + offset)
                y_coords.append(r * self.spacing)
        return np.array(x_coords), np.array(y_coords)