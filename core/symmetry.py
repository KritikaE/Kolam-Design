import numpy as np

class MugguSymmetry:
    def __init__(self, center_point=(0, 0)):
        self.center = np.array(center_point)

    def apply_radial_symmetry(self, path, num_petals):
        """
        Rotates a path evenly based on the number of petals requested.
        Design Principle: Radial Symmetry (360/n)
        """
        path = np.array(path)
        full_pattern = []
        
        # Calculate the angle for each petal
        angles = np.linspace(0, 360, num_petals, endpoint=False)
        
        for angle in angles:
            theta = np.radians(angle)
            c, s = np.cos(theta), np.sin(theta)
            R = np.array(((c, -s), (s, c)))
            
            # Rotate around center
            rotated_path = (path - self.center) @ R.T + self.center
            full_pattern.append(rotated_path)
            
        return full_pattern