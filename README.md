# Dynamical System Attractor Demo

An interactive visualization of chaotic dynamical systems using Python and Streamlit. This application allows you to explore the Lorenz, Rössler, and Thomas attractors in 3D and 2D, with real-time parameter adjustment.

## Features

-   **Interactive Visualization**: Rotate and zoom 3D phase space trajectories.
-   **Multiple Systems**: Explore different chaotic attractors:
    -   **Lorenz Attractor**: The classic butterfly effect.
    -   **Rössler Attractor**: Simpler chaotic dynamics.
    -   **Thomas Cyclically Symmetric Attractor**: A beautiful 3D structure.
-   **Real-time Parameters**: Adjust system constants (e.g., $\sigma, \rho, \beta$) and see the impact immediately.
-   **Time Series Analysis**: View the time evolution of each variable ($x, y, z$) in separate plots.
-   **Mathematical Context**: View the differential equations for the selected system.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yasuhiroinoue/DynamicalSystemDemo.git
    cd DynamicalSystemDemo
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser (usually at `http://localhost:8501`).

## Dependencies

-   `streamlit`
-   `numpy`
-   `scipy`
-   `plotly`
-   `pandas`
