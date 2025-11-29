import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from systems import SYSTEMS

st.set_page_config(page_title="Dynamical System Attractor Demo", layout="wide")

st.title("Dynamical System Attractor Demo")

# Sidebar for controls
st.sidebar.header("Configuration")

# System Selector
system_name = st.sidebar.selectbox("Select System", list(SYSTEMS.keys()))
system = SYSTEMS[system_name]

st.sidebar.subheader("Equations")
st.sidebar.latex(system.latex_equations)

st.sidebar.subheader("Parameters")
params = {}
for param_name, default_val in system.default_params.items():
    min_val, max_val = system.param_ranges[param_name]
    # Use slider for float parameters
    params[param_name] = st.sidebar.slider(
        f"{param_name}",
        min_value=float(min_val),
        max_value=float(max_val),
        value=float(default_val),
        step=0.01
    )

st.sidebar.subheader("Simulation Settings")
t_max = st.sidebar.number_input("Max Time", value=system.t_max, min_value=10.0, max_value=2000.0)
dt = st.sidebar.number_input("Time Step", value=system.dt, min_value=0.001, max_value=0.1, format="%.3f")

# Update system settings if changed
system.t_max = t_max
system.dt = dt

# Initial State
st.sidebar.subheader("Initial State")
init_state = []
labels = ['x', 'y', 'z']
for i, label in enumerate(labels):
    val = st.sidebar.number_input(f"Initial {label}", value=system.initial_state[i])
    init_state.append(val)
system.initial_state = init_state

# Solve System
t, states = system.solve(params)
df = pd.DataFrame(states, columns=['x', 'y', 'z'])
df['t'] = t

# Visualization
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Phase Space Trajectory")
    
    view_mode = st.radio("View Mode", ["3D", "2D (XY)", "2D (XZ)", "2D (YZ)"], horizontal=True)
    
    if view_mode == "3D":
        fig = go.Figure(data=[go.Scatter3d(
            x=df['x'], y=df['y'], z=df['z'],
            mode='lines',
            line=dict(color=t, colorscale='Viridis', width=2),
            opacity=0.8
        )])
        fig.update_layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            ),
            margin=dict(l=0, r=0, b=0, t=0),
            height=600
        )
    else:
        if view_mode == "2D (XY)":
            x_col, y_col = 'x', 'y'
        elif view_mode == "2D (XZ)":
            x_col, y_col = 'x', 'z'
        else: # YZ
            x_col, y_col = 'y', 'z'
            
        fig = go.Figure(data=[go.Scatter(
            x=df[x_col], y=df[y_col],
            mode='lines',
            line=dict(color='teal', width=1.5)
        )])
        fig.update_layout(
            xaxis_title=x_col.upper(),
            yaxis_title=y_col.upper(),
            height=600,
            margin=dict(l=0, r=0, b=0, t=0)
        )
        
    st.plotly_chart(fig, width="stretch")

from plotly.subplots import make_subplots

# ... (existing imports)

# ... (inside the column layout)

with col2:
    st.subheader("Time Series")
    
    # Plot x, y, z over time in separate subplots
    fig_ts = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                           subplot_titles=("x(t)", "y(t)", "z(t)"))
    
    fig_ts.add_trace(go.Scatter(x=t, y=df['x'], name='x', line=dict(width=1)), row=1, col=1)
    fig_ts.add_trace(go.Scatter(x=t, y=df['y'], name='y', line=dict(width=1)), row=2, col=1)
    fig_ts.add_trace(go.Scatter(x=t, y=df['z'], name='z', line=dict(width=1)), row=3, col=1)
    
    fig_ts.update_layout(
        height=600,
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False
    )
    fig_ts.update_xaxes(title_text="Time", row=3, col=1)
    
    st.plotly_chart(fig_ts, width="stretch")
    
    st.write("### Statistics")
    st.write(df.describe())
