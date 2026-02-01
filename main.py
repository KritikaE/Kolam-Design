import matplotlib.pyplot as plt
import cv2
import numpy as np
import random
import tkinter as tk
from tkinter import messagebox, filedialog
from core.grid import KolamEngine
from core.symmetry import MugguSymmetry
from core.generator import CurveGenerator, HeritageGenerator
from core.vision import MugguVision

# --- THEME DEFINITION ---
THEME = {
    "bg": "#FFF8E1",          # Cream / Rice Flour (Soft Background)
    "fg": "#4E342E",          # Deep Earth Brown (Primary Text)
    "accent_1": "#66BB6A",    # Muted Sage (Green - Generate/Success)
    "accent_2": "#42A5F5",    # Soft Indigo (Blue - Analyze/Action)
    "accent_3": "#EF5350",    # Terracotta (Red - Exit/Alert)
    "text_light": "#8D6E63",  # Light Brown (Secondary Text)
    "font_title": ("Georgia", 16, "bold"),
    "font_body": ("Segoe UI", 10),
    "font_btn": ("Segoe UI", 11, "bold")
}

from matplotlib.widgets import Button

# --- MODULE 1: YOUR DESIGN GENERATOR ---
def run_generator():
    SIZE = 11 
    CENTER = SIZE // 2 
    engine = KolamEngine(size=SIZE)
    
    heritage = HeritageGenerator(size=SIZE)
    smoother = CurveGenerator()
    sym = MugguSymmetry(center_point=(CENTER, CENTER))
    
    palettes = [
        ['#D32F2F', '#FFC107', '#1976D2'], 
        ['#8E24AA', '#00ACC1', "#7094E9"], 
        ["#388E3C", "#8BC34A", "#CDDC39"], # Greenery
        ["#F57C00", "#FFB74D", "#FF9800"], # Sunset
    ]

    # Create figure only once
    fig, ax = plt.subplots(figsize=(8,8), facecolor=THEME["bg"]) 
    plt.subplots_adjust(bottom=0.2) # Make space for button

    def generate(event=None):
        ax.clear()
        ax.set_facecolor(THEME["bg"])
        
        # 1. Background Grid
        dots_x, dots_y = engine._generate_square_grid() 
        ax.scatter(dots_x, dots_y, c=THEME["text_light"], s=20, zorder=1, alpha=0.4)
        
        # 2. Design
        current_colors = random.choice(palettes)
        design = heritage.get_varied_petal_layers()
        
        for i, layer in enumerate(design):
            curvy = smoother.smooth_path(layer['path'])
            rotations = sym.apply_radial_symmetry(curvy, num_petals=layer['petals'])
            color = current_colors[i % len(current_colors)]
            for part in rotations:
                if layer['fill']:
                    ax.fill(part[:, 0], part[:, 1], color=color, alpha=0.2, zorder=i+2)
                ax.plot(part[:, 0], part[:, 1], color=color, lw=2.5, zorder=i+3)

        ax.axis('off')
        ax.set_aspect('equal')
        ax.set_title(" Loop & Bloom Generator ", color=THEME["fg"], 
                  fontsize=18, fontname="Georgia", pad=10)
        plt.draw()

    # Initial Run
    generate()

    # Add Regenerate Button
    ax_btn = plt.axes([0.35, 0.05, 0.3, 0.075]) # [left, bottom, width, height]
    btn = Button(ax_btn, 'Generate New ↻', color=THEME["accent_1"], hovercolor=THEME["accent_2"])

    # Styling button label
    btn.label.set_fontsize(12)
    btn.label.set_fontname("Segoe UI")
    btn.label.set_color("white")
    
    btn.on_clicked(generate)
    plt.show()

# --- MODULE 2: THE CV ANALYZER ---

# --------------------------------------------------
# MAIN ANALYZER
# --------------------------------------------------
def run_analyzer(image_path):
    try:
        vision = MugguVision(image_path)

        # 1. Principles check now runs identify_chukkalu and get_skeleton internally
        principles = vision.analyze_principles()
        
        # 2. We still want these for the visual subplots
        dots = vision.identify_chukkalu() 
        edges = vision.get_edges()

        # --- Visualization ---
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7.5), facecolor=THEME["bg"])
        
        # Adjust layout to give ample space at the bottom for text
        plt.subplots_adjust(bottom=0.35, wspace=0.1, left=0.05, right=0.95) 

        ax1.imshow(cv2.cvtColor(vision.image, cv2.COLOR_BGR2RGB))
        ax1.set_title("1. Feature Extraction", color=THEME["fg"], fontsize=12, fontweight="bold", fontname="Georgia")
        ax1.axis("off")

        # Display the edges/skeleton on the right
        ax2.imshow(edges, cmap="gray")
        ax2.set_title("2. Structural Skeleton & Dots", color=THEME["fg"], fontsize=12, fontweight="bold", fontname="Georgia")
        ax2.axis("off")
        
        # HIGHLIGHT DETECTED DOTS
        if dots:
            dots_np = np.array(dots)
            # Scatter plot on top of skeleton (ax2)
            # x is col (0), y is row (1)
            ax2.scatter(dots_np[:, 0], dots_np[:, 1], c=THEME["accent_3"], s=40, marker='o', label='Dots')
            # Also on original image for reference? (optional, user asked strictly 'highlighted in skeletal image')

        # --- Rule Output Text ---
        # Construct a cleaner, multi-line string
        info_text = "✿ ANALYSIS RESULTS ✿\n\n"
        
        # 1. Principles
        info_text += "[ Principles Check ]\n"
        for key, value in principles.items():
            if isinstance(value, bool):
                mark = "✓" if value else "✗"
                info_text += f"  {mark} {key}\n"
                
        # 2. Details
        info_text += f"\n[ Details ]\n  • Detected Dots: {len(dots)}\n"
        
        if "Design Style" in principles:
             info_text += f"  • Style: {principles['Design Style']}\n"
             
        if "Detected Palette" in principles:
             palette_str = ", ".join(principles["Detected Palette"])
             info_text += f"  • Palette: {palette_str}\n"

        # Styled Text Box
        props = dict(boxstyle='round,pad=1', facecolor='white', alpha=0.8, edgecolor=THEME["text_light"])
        fig.text(0.5, 0.03, info_text, ha="center", va="bottom", fontsize=10, 
                 color=THEME["fg"], linespacing=1.6, fontweight="normal", family="sans-serif",
                 bbox=props)

        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
# --------------------------------------------------
# FILE PICKER
# --------------------------------------------------
def select_and_analyze():
    file_path = filedialog.askopenfilename(
        title="Select Muggu / Kolam Image",
        filetypes=(
            ("Image files", "*.jpg *.png *.jpeg"),
            ("All files", "*.*")
        )
    )
    if file_path:
        run_analyzer(file_path)

        
# --- GUI DASHBOARD ---
def start_dashboard():
    root = tk.Tk()
    root.title("Loop & Bloom Dashboard")
    root.geometry("450x350")
    root.configure(bg=THEME["bg"])

    # Header
    label = tk.Label(root, text="✿❁❀ Loop & Bloom ❀❁✿", 
                     font=THEME["font_title"], bg=THEME["bg"], fg=THEME["fg"])
    label.pack(pady=30)

    # Styling helper
    def create_btn(text, cmd, color):
        return tk.Button(root, text=text, command=cmd, width=28, 
                         bg=color, fg="white", 
                         font=THEME["font_btn"], 
                         relief="flat", pady=8, cursor="hand2")

    # Option 1: Generate
    btn_gen = create_btn("1. Generate Rangoli", run_generator, THEME["accent_1"])
    btn_gen.pack(pady=10)

    # Option 2: Analyze
    btn_ana = create_btn("2. Analyze Muggu", select_and_analyze, THEME["accent_2"])
    btn_ana.pack(pady=10)

    # Option 3: Exit
    btn_exit = create_btn("3. Exit", root.destroy, THEME["accent_3"])
    btn_exit.pack(pady=10)
    
    # Footer
    footer = tk.Label(root, text="A fusion of Math, Art & Tradition", 
                      font=("Segoe UI", 9, "italic"), bg=THEME["bg"], fg=THEME["text_light"])
    footer.pack(side="bottom", pady=20)

    root.mainloop()

if __name__ == "__main__":
    start_dashboard()