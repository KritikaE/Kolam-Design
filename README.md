# Loop & Bloom

Experimental Generative Design & Computer Vision Project exploring **Kolams (Muggu)** — traditional Indian threshold art. This project combines procedural generation with computer vision analysis to explore the mathematical and artistic properties of Kolams.

## 🌟 Features

### 1. Generative Art (Loop & Bloom Generator)
- **Procedural Design**: Generates unique loop-based Kolam designs based on mathematical curves and symmetry.
- **Customizable**: Uses randomized parameters for layers, petal counts, and sizes to create varied patterns.
- **Style Themes**: Features curated color palettes and a "Regenerate" button to explore different aesthetics.
- **Smooth Curves**: Implements spline interpolation for fluid, organic-looking lines.

### 2. Heritage Analyzer (Computer Vision)
- **Image Analysis**: Analyzes uploaded images of drawn Kolams/Muggus.
- **Feature Extraction**: Detects "Chukkalu" (dots) and the structural skeleton of the design.
- **Rule Verification**: Checks against traditional rules like "Sikku" (single continuous closed loop) and endpoint counts.
- **Style Classification**: Attempts to classify the design into styles like "Puli Kolam" or "Sikku Kolam".
- **Color Extraction**: Identifies dominant cultural colors (e.g., Kumkum Red, Turmeric Yellow) from the image.

## 🛠️ Installation

Ensure you have Python installed. Clone the repository and install the dependencies:

```bash
pip install matplotlib opencv-python numpy scipy
```

*Note: `tkinter` is required for the GUI, which is usually included with standard Python installations.*

## 🚀 Usage

Run the main application to launch the dashboard:

```bash
python main.py
```

### Dashboard Options:
1.  **Generate Rangoli**: Opens the generator window. Click "Generate New ↻" to create fresh patterns.
2.  **Analyze Muggu**: A file picker opens. Select an image (`.jpg`, `.png`) of a Kolam to analyze its structure and properties.
3.  **Exit**: Closes the application.

## 📂 Project Structure

- **`main.py`**: Entry point for the application. Handles the GUI dashboard and integrates modules.
- **`core/`**:
    - **`generator.py`**: Logic for procedural curve generation (`CurveGenerator`, `HeritageGenerator`).
    - **`vision.py`**: Computer vision algorithms for image analysis (`MugguVision`).
    - **`grid.py`**: (Internal) Grid system logic.
    - **`symmetry.py`**: (Internal) Symmetry operations.
- **`assets/`**: Contains resource files.

## 🎓 Credits

**Developed by Kritika E.**
*A fusion of Math, Art & Tradition.*