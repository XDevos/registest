# Module description

There are three modules: independent but combinable.
1. Deform
2. Register
3. Compare

## 1. Deform

Features:
- Linear
    - Axis X,Y,Z
    - Rotation
    - Zoom
- No linear

## 2. Register

Feature:
- Find shift values with a registration method
- Apply shift

Methods:
- Cross-correlation
- X-corr by blocks (pyhim global)
- SimpleITK

## 3. Compare

Feature:
- Compute similarity (SSIM, MSE)
- Create similarity file (CSV) group by same ref img ?
- Plot similarity results
- Overlay ref and target img in 3D
    - Save in HTML (plotly)
    - TIFF for napari visualization
    - PNG with a Z projection
- PDF report with PNG and graphs
