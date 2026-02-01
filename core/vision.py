import cv2
import numpy as np

class MugguVision:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Could not open image at {image_path}")
        # Convert to HSV for better color/brightness separation
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def identify_chukkalu(self):
        """
        Feature Extraction: Using HSV Color Segmentation and High-Intensity Thresholding 
        to isolate 'Chukkalu' (dots).
        """
        # 1. Use V (Value) channel from HSV for intensity
        v_channel = self.hsv[:, :, 2]
        
        # 2. High-Intensity Thresholding
        # Dots are usually the brightest part of the image
        _, mask = cv2.threshold(v_channel, 200, 255, cv2.THRESH_BINARY)
        
        # 3. Morphological cleanup to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # 4. Contour detection
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        dots = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # Filter by area to distinguish dots from lines or noise
            # Increased max area to 2000 to catch dots in larger/closer images (e.g. kolam4)
            if 5 < area < 2000:  
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    dots.append((cx, cy))
        return dots

    def get_skeleton(self):
        """
        Structural Skeletonization: Converting hand-drawn or digital lines into a 
        1-pixel-wide mathematical 'skeleton'.
        """
        # 1. Adaptive Thresholding for robust line detection
        binary = cv2.adaptiveThreshold(self.gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # 2. Morphological Closing to bridge gaps
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # 3. Skeletonization
        try:
            # Check for ximgproc (opencv-contrib-python)
            skeleton = cv2.ximgproc.thinning(closed, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
        except AttributeError:
            # Fallback for standard OpenCV
            skeleton = self._skeletonize_morphological(closed)
            
        return skeleton

    def _skeletonize_morphological(self, img):
        """Standard morphological skeletonization fallback."""
        size = np.size(img)
        skel = np.zeros(img.shape, np.uint8)
        
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        done = False
        
        while not done:
            eroded = cv2.erode(img, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img = eroded.copy()
            
            zeros = size - cv2.countNonZero(img)
            if zeros == size:
                done = True
        return skel

    def verify_sikku_topology(self, skeleton):
        """
        Rule-Based Verification: Applying Topological Neighbor Counting to verify 
        if a design follows the Sikku principle (single continuous closed loop).
        """
        skel_bool = (skeleton > 0).astype(np.uint8)
        
        # Neighbor counting kernel
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)
        
        # Count neighbors for each pixel
        neighbor_count = cv2.filter2D(skel_bool, -1, kernel)
        neighbor_count = neighbor_count * skel_bool
        
        # Endpoints have exactly 1 neighbor
        endpoints = np.sum(neighbor_count == 1)
        
        # Sikku Principle: A closed loop must have ZERO endpoints.
        is_closed_loop = (endpoints == 0)
        has_content = np.sum(skel_bool) > 0
        
        return {
            "is_closed_loop": is_closed_loop,
            "endpoints_count": endpoints,
            "has_content": has_content
        }

    def classify_style(self, dots, skeleton):
        """
        Style Classifier: Distinguishes between Puli, Sikku, and Padi styles.
        """
        if not dots:
            return "Unknown (No Dots)"
        
        # 1. Distance Transform from Skeleton
        skel_inv = cv2.bitwise_not(skeleton)
        dist_transform = cv2.distanceTransform(skel_inv, cv2.DIST_L2, 5)
        
        dot_distances = []
        for dot in dots:
            d = dist_transform[dot[1], dot[0]]
            dot_distances.append(d)
            
        avg_dist = np.mean(dot_distances) if dot_distances else 0
        
        style = "Unknown"
        
        # Heuristic: If avg distance is very small (< 10 pixels), likely Puli.
        if avg_dist < 12:
            style = "Puli Kolam (Dot-to-Dot)"
        else:
            style = "Sikku Kolam (Curved)"
            
        return style

    def extract_color_palette(self, k=2):
        """
        Color Palette 'Mood' Extraction: K-Means Clustering on original colors.
        Ignores background color to find dominant *design* colors.
        Returns Top 2 colors.
        """
        # Resize for speed
        img_small = cv2.resize(self.image, (150, 150))
        img_rgb = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
        
        # Detect background color (median of 4 corners)
        h, w, _ = img_rgb.shape
        corners = [
            img_rgb[0, 0], img_rgb[0, w-1], 
            img_rgb[h-1, 0], img_rgb[h-1, w-1]
        ]
        bg_color = np.median(corners, axis=0) # [R, G, B]
        
        pixels = img_rgb.reshape(-1, 3).astype(np.float32)
        
        # Filter out background pixels
        # Calculate distance of each pixel to detected background
        dist_to_bg = np.linalg.norm(pixels - bg_color, axis=1)
        
        # Threshold: exclude pixels very close to background (e.g., < 30 euclidean dist)
        # Also exclude very dark pixels if BG is dark (Charcoal Black issue)
        # But 'bg_color' logic covers generic background.
        
        non_bg_mask = dist_to_bg > 30 
        content_pixels = pixels[non_bg_mask]
        
        # If image is solid color or mask removed everything, fallback to original
        if len(content_pixels) < 100:
            content_pixels = pixels

        # K-Means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        
        # Handle case where we have fewer pixels than k centers
        actual_k = min(k, len(content_pixels))
        
        if actual_k > 0:
            _, labels, centers = cv2.kmeans(content_pixels, actual_k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            dominant_colors = centers.astype(int)
        else:
            dominant_colors = []
        
        palette = []
        for color in dominant_colors:
            name = self._get_cultural_color_name(color)
            palette.append(name)
            
        return palette

    def _get_cultural_color_name(self, rgb):
        """Maps RGB to nearest Indian cultural color name."""
        r, g, b = rgb
        
        # Simple Euclidean distance mapping to a predefined cultural palette
        cultural_colors = {
            "Kumkum Red": (180, 20, 20),
            "Turmeric Yellow": (255, 200, 0),
            "Rice Flour White": (240, 240, 240),
            "Charcoal Black": (30, 30, 30),
            "Leaf Green": (34, 139, 34),
            "Sky Blue": (135, 206, 235),
            "Magenta": (255, 0, 255),
            "Saffron": (255, 153, 51),
            "Mud Brown": (101, 67, 33),
            "Deep Blue": (0, 50, 150)
        }
        
        min_dist = float('inf')
        closest_name = "Unknown"
        
        for name, ref_rgb in cultural_colors.items():
            dist = np.sqrt((r - ref_rgb[0])**2 + (g - ref_rgb[1])**2 + (b - ref_rgb[2])**2)
            if dist < min_dist:
                min_dist = dist
                closest_name = name
                
        return closest_name

    def analyze_principles(self):
        dots = self.identify_chukkalu()
        skel = self.get_skeleton()
        topology = self.verify_sikku_topology(skel)
        
        style_label = self.classify_style(dots, skel)
        palette = self.extract_color_palette()
        
        return {
            "Anchor Dot Grid (Chukkalu)": len(dots) >= 1,
            "Single Continuous Line (Sikku)": topology["is_closed_loop"] and topology["has_content"],
            "Zero Endpoints Checks": topology["endpoints_count"] == 0,
            "Design Style": style_label,
            "Detected Palette": palette
        }

    def get_edges(self):
        return self.get_skeleton()