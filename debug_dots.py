
import cv2
import numpy as np
from core.vision import MugguVision

def debug_dots(image_path):
    print(f"Debugging {image_path}...")
    vision = MugguVision(image_path)
    
    v_channel = vision.hsv[:, :, 2]
    print(f"Max V: {np.max(v_channel)}")
    print(f"Mean V: {np.mean(v_channel)}")
    
    # Test current logic
    _, mask = cv2.threshold(v_channel, 200, 255, cv2.THRESH_BINARY)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(mask_open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Contours found: {len(contours)}")
    
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if i < 10: # Print first 10
            print(f"Cnt {i} Area: {area}")
            
    # Check if adaptive thresholding helps
    print("\nTesting Adaptive Thresholding for Dots:")
    gray = vision.gray
    # Inverted because we want bright dots (which become 'foreground' in adaptive if we treat them right)
    # Actually adaptive thresholding usually finds dark edges or creates local binary. 
    # For bright dots on dark bg:
    binary_adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, -5) 
    # -5 C constant helps pick out bright glowing spots? Or just standard threshold.
    
    # Or just a lower global threshold?
    _, mask_low = cv2.threshold(v_channel, 150, 255, cv2.THRESH_BINARY)
    print(f"Contours at Threshold=150: {len(cv2.findContours(mask_low, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0])}")


if __name__ == "__main__":
    debug_dots("assets/kolam4.jpg")
