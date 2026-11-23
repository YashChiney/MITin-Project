import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

st.set_page_config(page_title="Beam Experiment Visualizer", page_icon="⚖️", layout="wide")

st.title("Beam Experiment – Live Diagram")
st.write(
    "Change the load, its position, or the beam dimensions. "
    "The beam sketch, load arrow, reaction arrow and labels update immediately. "
    "This version uses diagrams only — no graphs."
)

mode = st.radio("Choose experiment", ["Simple Beam", "Compound Beam"], horizontal=True)

def draw_arrow(ax, x, y_start, y_end, label, color, label_dx=0.0):
    ax.annotate(
        "", xy=(x, y_end), xytext=(x, y_start),
        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=color, mutation_scale=16)
    )
    ax.text(x + label_dx, (y_start + y_end) / 2, label,
            color=color, fontsize=11, weight="bold", ha="center", va="center")

def draw_support(ax, x, y, kind="pin", label=None):
    if kind == "roller":
        tri = Polygon([[x - 0.045, y - 0.13], [x + 0.045, y - 0.13], [x, y - 0.02]],
                      closed=True, fill=False, edgecolor="black", linewidth=1.6)
        ax.add_patch(tri)
        ax.add_patch(Circle((x, y - 0.16), 0.018, fill=False, edgecolor="black", linewidth=1.2))
        ax.plot([x - 0.075, x + 0.075], [y - 0.19, y - 0.19], color="black", lw=1.4)
    else:
        tri = Polygon([[x - 0.055, y - 0.14], [x + 0.055, y - 0.14], [x, y - 0.015]],
                      closed=True, fill=False, edgecolor="black", linewidth=1.6)
        ax.add_patch(tri)
        ax.plot([x - 0.08, x + 0.08], [y - 0.15, y - 0.15], color="black", lw=1.4)
    if label:
        ax.text(x, y - 0.29, label, ha="center", va="top", fontsize=10)

def beam_line(ax, x0, x1, y, label_left, label_right):
    ax.plot([x0, x1], [y, y], color="#333333", lw=9, solid_capstyle="butt", zorder=2)
    ax.plot([x0, x1], [y + 0.035, y + 0.035], color="#888888", lw=1, zorder=3)
    ax.text(x0, y + 0.13, label_left, ha="center", fontsize=11, weight="bold")
    ax.text(x1, y + 0.13, label_right, ha="center", fontsize=11, weight="bold")

def setup_ax(ax, ylim=(-0.85, 1.35)):
    ax.set_xlim(-0.13, 1.13)
    ax.set_ylim(*ylim)
    ax.axis("off")

def simple_diagram(L, W, x):
    fig, ax = plt.subplots(figsize=(10, 3.4))
    setup_ax(ax)
    y = 0.62
    xp = x / L

    beam_line(ax, 0, 1, y, "A", "B")
    draw_support(ax, 0, y - 0.02, "pin", "Pin support")
    draw_support(ax, 1, y - 0.02, "roller", "Roller support")

    # Load position and force arrow; arrow length responds to W.
    arrow_len = 0.22 + 0.22 * min(W / 15.0, 1.0)
    draw_arrow(ax, xp, y + 0.55, y + 0.55 - arrow_len, f"W = {W:.2f} N", "#d62728", 0.075)
    draw_arrow(ax, 1, y - 0.45, y - 0.05, "Rᴮ", "#1f77b4", 0.06)

    ax.annotate("", xy=(xp, 1.22), xytext=(0, 1.22),
                arrowprops=dict(arrowstyle="<->", lw=1.3, color="black"))
    ax.text(xp / 2 if xp > 0.08 else 0.07, 1.25, f"x = {x:.2f} m",
            ha="center", va="bottom", fontsize=10)
    ax.text(0.5, -0.67, f"Beam span L = {L:.2f} m", ha="center", fontsize=10)
    ax.set_title("SIMPLE BEAM – point load and support reaction", fontsize=12, weight="bold")
    fig.tight_layout()
    return fig

def compound_diagram(L1, L2, a, W, x):
    fig, ax = plt.subplots(figsize=(10, 4.4))
    setup_ax(ax, (-1.0, 1.65))

    # Upper beam AB: A at 0, B at 1; C is L1-a from A.
    y_top = 1.05
    c = (L1 - a) / L1
    xp = x / L1

    beam_line(ax, 0, 1, y_top, "A", "B")
    draw_support(ax, 0, y_top - 0.02, "pin", "A")
    # Contact point C between the two beams.
    ax.plot([c, c], [y_top - 0.02, 0.45], color="#555555", lw=1.3, ls="--")
    ax.text(c, y_top + 0.13, "C", ha="center", fontsize=11, weight="bold")

    arrow_len = 0.22 + 0.22 * min(W / 15.0, 1.0)
    draw_arrow(ax, xp, y_top + 0.58, y_top + 0.58 - arrow_len,
               f"W = {W:.2f} N", "#d62728", 0.075)

    # Lower beam CD. C and D are its ends, span L2.
    y_low = 0.28
    beam_line(ax, 0.12, 0.88, y_low, "C", "D")
    draw_support(ax, 0.12, y_low - 0.02, "pin", "Support")
    draw_support(ax, 0.88, y_low - 0.02, "roller", "Support")
    draw_arrow(ax, 0.12, y_low - 0.55, y_low - 0.08, "Rᶜ", "#1f77b4", -0.055)

    # Dimension guides.
    ax.annotate("", xy=(1, 1.48), xytext=(0, 1.48),
                arrowprops=dict(arrowstyle="<->", lw=1.2))
    ax.text(0.5, 1.51, f"L₁ = {L1:.2f} m", ha="center", va="bottom", fontsize=10)
    ax.annotate("", xy=(xp, 1.30), xytext=(0, 1.30),
                arrowprops=dict(arrowstyle="<->", lw=1.1))
    ax.text(max(xp / 2, 0.06), 1.32, f"x = {x:.2f} m", ha="center", va="bottom", fontsize=9)
    ax.text(0.5, -0.77, f"Lower beam span L₂ = {L2:.2f} m     a = {a:.2f} m",
            ha="center", fontsize=10)
    ax.set_title("COMPOUND BEAM – upper beam AB resting on lower beam CD",
                  fontsize=12, weight="bold")
    fig.tight_layout()
    return fig

if mode == "Simple Beam":
    st.subheader("Simple Beam – change the values")
    c1, c2, c3 = st.columns(3)
    L = c1.number_input("Span L (m)", min_value=0.10, value=1.00, step=0.10)
    W = c2.number_input("External load W (N)", min_value=0.01, value=5.88, step=0.10)
    x = c3.number_input("Load distance x from A (m)", min_value=0.00, value=0.20, step=0.05)
    if x > L:
        st.error("The load position x cannot be greater than the beam span L.")
    else:
        RB = W * x / L
        st.pyplot(simple_diagram(L, W, x), use_container_width=True)
        st.latex(r"R_B = \frac{Wx}{L}")
        st.metric("Analytical reaction at B", f"{RB:.3f} N")
        st.caption("The red arrow marks the applied load W. The blue arrow marks reaction Rᴮ.")

else:
    st.subheader("Compound Beam – change the values")
    c1, c2, c3 = st.columns(3)
    L1 = c1.number_input("Upper beam span L₁ (m)", min_value=0.10, value=1.00, step=0.10)
    L2 = c2.number_input("Lower beam span L₂ (m)", min_value=0.10, value=1.00, step=0.10)
    a = c3.number_input("Distance a (m)", min_value=0.00, value=0.20, step=0.05)
    c4, c5 = st.columns(2)
    W = c4.number_input("External load W (N)", min_value=0.01, value=7.84, step=0.10)
    x = c5.number_input("Load distance x from A (m)", min_value=0.00, value=0.20, step=0.05)

    if x > L1:
        st.error("The load position x cannot be greater than L₁.")
    elif a >= L2:
        st.error("Distance a must be smaller than L₂.")
    else:
        RC = W * x * (L2 - a) / (L1 * L2)
        st.pyplot(compound_diagram(L1, L2, a, W, x), use_container_width=True)
        st.latex(r"R_C = \frac{Wx(L_2-a)}{L_1L_2}")
        st.metric("Analytical reaction at C", f"{RC:.3f} N")
        st.caption("The red arrow marks the applied load W. The blue arrow marks reaction Rᶜ.")

st.divider()
