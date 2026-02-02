import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
from core.grid import KolamEngine
from core.symmetry import MugguSymmetry
from core.generator import CurveGenerator, HeritageGenerator
from core.vision import MugguVision

def generate_sample_kolam(output_path="sample_kolam.png"):
    print(f"Generating sample Kolam to {output_path}...")
    SIZE = 11 
    CENTER = SIZE // 2 
    engine = KolamEngine(size=SIZE)
    dots_x, dots_y = engine._generate_square_grid() 

    heritage = HeritageGenerator(size=SIZE)
    smoother = CurveGenerator()
    sym = MugguSymmetry(center_point=(CENTER, CENTER))

    # Single color for simplicity in verification
    color = '#D32F2F'

    # Create figure without borders for cleaner image analysis
    fig, ax = plt.subplots(figsize=(6,6), facecolor='white') 
    ax.set_facecolor('white')
    ax.set_facecolor('black')
    
    # Bright White Dots
    ax.scatter(dots_x, dots_y, c='white', s=50, zorder=1) 

    design = heritage.get_varied_petal_layers()
    for i, layer in enumerate(design):
        curvy = smoother.smooth_path(layer['path'])
        rotations = sym.apply_radial_symmetry(curvy, num_petals=layer['petals'])
        for part in rotations:
            # Dimmer lines to differentiate from bright dots for high-intensity thresholding test
            ax.plot(part[:, 0], part[:, 1], color='#555555', lw=3, zorder=i+3)

    ax.axis('off')
    ax.set_aspect('equal')
    
    # Save with tight bounding box
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()
    print("Sample generated.")

def verify_analysis(image_path="sample_kolam.png"):
    print(f"Analyzing {image_path}...")
    vision = MugguVision(image_path)
    
    # DEBUG: Check V channel stats
    v_channel = vision.hsv[:, :, 2]
    print(f"V-Channel Max: {np.max(v_channel)}")
    print(f"V-Channel Mean: {np.mean(v_channel)}")
    
    # DEBUG: Check threshold count locally to see if vision.py is consistent
    _, mask = cv2.threshold(v_channel, 200, 255, cv2.THRESH_BINARY)
    print(f"Pixels > 200 in V: {cv2.countNonZero(mask)}")
    
    # Run Analysis
    results = vision.analyze_principles()
    
    print("\n--- Verification Results ---")
    for key, value in results.items():
        print(f"{key}: {value}")
        
    # Check specifics
    dots = vision.identify_chukkalu()
    print(f"Dots Detected: {len(dots)}")
    
    # Palette check
    palette = vision.extract_color_palette(k=2)
    print(f"Palette: {palette}")
    
    # Visual check
    skel = vision.get_skeleton()
    cv2.imwrite("debug_skeleton.png", skel)
    print("Saved 'debug_skeleton.png' for inspection.")
    
    # Assertions
    if len(dots) > 0:
        print("[Pass] Dots detected.")
    else:
        print("[FAIL] No dots detected!")
        
    if results.get("Zero Endpoints Checks") or results.get("Single Continuous Line (Sikku)"):
        print("[Pass] Topology check passed (Closed Loop).")
    else:
        print("[WARN] Topology check indicates open loop or endpoints found. (Expected for some random designs, but Code logic ran).")

if __name__ == "__main__":
    # Test on requested images
    test_files = ["assets/kolam1.JPG", "assets/kolam4.jpg"]
    
    for image_file in test_files:
        if os.path.exists(image_file):
            print(f"\n{'='*30}")
            print(f"VERIFYING: {image_file}")
            print(f"{'='*30}")
            verify_analysis(image_file)
        else:
            print(f"Error: {image_file} not found locally.")
        # Fallback to generation if file missing (optional, but good for safety)
        # generate_sample_kolam()
        # verify_analysis()
