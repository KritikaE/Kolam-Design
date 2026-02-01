import numpy as np
from scipy.interpolate import CubicSpline
import random

class CurveGenerator:
    @staticmethod
    def smooth_path(path, points_per_segment=20):
        path = np.array(path)
        if len(path) < 3: return path
        t = np.linspace(0, 1, len(path))
        t_new = np.linspace(0, 1, len(path) * points_per_segment)
        cs_x = CubicSpline(t, path[:, 0], bc_type='clamped')
        cs_y = CubicSpline(t, path[:, 1], bc_type='clamped')
        return np.vstack((cs_x(t_new), cs_y(t_new))).T

import random

class HeritageGenerator:
    def __init__(self, size):
        self.size = size
        self.center = size // 2

    def get_varied_petal_layers(self):
        """Generates random layers that are strictly anchored to the dot grid."""
        layers = []
        # We'll generate 2 to 4 layers
        num_layers = random.randint(2, 4)
        
        for i in range(num_layers):
            # DESIGN PRINCIPLE: 
            # Step must be 1.0 to align with square grid or 0.5 for staggered.
            # We pick a random length (how many dots out) and width (how many dots wide).
            
            # Inner layers stay small, outer layers go further
            min_dist = i + 1
            max_dist = self.center
            
            length = random.randint(min_dist, max_dist)
            width = random.uniform(0.5, length * 0.5) 
            
            # Higher index layers get more petals for the 'blooming' effect
            petal_counts = [4, 8, 12, 16]
            
            layers.append({
                'path': self._make_petal(self.center, self.center, length, width),
                'petals': petal_counts[i] if i < len(petal_counts) else 16,
                'fill': random.choice([True, False])
            })
            
        return layers

    def _make_petal(self, x, y, length, width):
        # Anchor points: (Center) -> (Curve Out) -> (Tip on Dot) -> (Curve In) -> (Center)
        return [
            (x, y), 
            (x + width, y + length/2), 
            (x, y + length), 
            (x - width, y + length/2), 
            (x, y)
        ]