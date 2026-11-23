import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

st.set_page_config(page_title="Beam Experiment Visualizer", page_icon="⚖️", layout="wide")

st.title("Beam Experiment – Live Diagram")
st.write(
    "Change the load, its position, beam dimensions, or experimental reaction. "
    "The beam sketch, force arrows, reaction values, and % error update immediately. "
    "This version uses diagrams only — no graphs."
)

mode = st.radio("Choose experiment", ["Simple Beam", "Compound Beam"], horizontal=True)


def draw_arrow(ax, x, y_start, y_end, label, color, label_dx=0.0, label_dy=0.0, fontsize=11):
    ax.annotate(
        "",
        xy=(x, y_end),
        xytext=(x, y_start),
        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=color, mutation_scale=16),
    )
    ax.text(
        x + label_dx,
        (y_start + y_end) / 2 + label_dy,
        label,
        color=color,
        fontsize=fontsize,
        weight="bold",
        ha="center",
        va="center",
    )


def draw_support(ax, x, y, kind="pin", label=None):
    if kind == "roller":
        tri = Polygon(
            [[x - 0.045, y - 0.13], [x + 0.045, y - 0.13], [x, y - 0.02]],
            closed=True,
            fill=False,
            edgecolor="black",
            linewidth=1.6,
        )
        ax.add_patch(tri)
        ax.add_patch(Circle((x, y - 0.16), 0.018, fill=False, edgecolor="black", linewidth=1.2))
        ax.plot([x - 0.075, x + 0.075], [y - 0.19, y - 0.19], color="black", lw=1.4)
    else:
        tri = Polygon(
            [[x - 0.055, y - 0.14], [x + 0.055, y - 0.14], [x, y - 0.015]],
            closed=True,
            fill=False,
            edgecolor="black",
            linewidth=1.6,
        )
        ax.add_patch(tri)
        ax.plot([x - 0.08, x + 0.08], [y - 0.15, y - 0.15], color="black", lw=1.4)

    if label:
        ax.text(x, y - 0.25, label, ha="center", va="top", fontsize=10, weight="bold")


def beam_line(ax, x0, x1, y, label_left, label_right):
    ax.plot([x0, x1], [y, y], color="#333333", lw=9, solid_capstyle="butt", zorder=2)
    ax.plot([x0, x1], [y + 0.035, y + 0.035], color="#888888", lw=1, zorder=3)
    ax.text(x0 - 0.03, y + 0.11, label_left, ha="center", fontsize=11, weight="bold")
    ax.text(x1 + 0.03, y + 0.11, label_right, ha="center", fontsize=11, weight="bold")


def setup_ax(ax, ylim=(-0.95, 1.55)):
    ax.set_xlim(-0.14, 1.14)
    ax.set_ylim(*ylim)
    ax.axis("off")


def simple_diagram(L, W, x):
    fig, ax = plt.subplots(figsize=(10, 3.6))
    setup_ax(ax, ylim=(-0.90, 1.45))

    y = 0.62
    xp = x / L

    beam_line(ax, 0.0, 1.0, y, "A", "B")
    draw_support(ax, 0.0, y - 0.02, "pin", "Pin")
    draw_support(ax, 1.0, y - 0.02, "roller", "Roller")

    arrow_len = 0.22 + 0.22 * min(W / 15.0, 1.0)
    draw_arrow(ax, xp, y + 0.56, y + 0.56 - arrow_len, f"W = {W:.2f} N", "#d62728", label_dx=0.085)
    draw_arrow(ax, 1.0, y - 0.52, y - 0.05, "Rᴮ", "#1f77b4", label_dx=0.065)

    # Dimension x from A
    ax.annotate("", xy=(xp, 1.25), xytext=(0.0, 1.25),
                arrowprops=dict(arrowstyle="<->", lw=1.3, color="black"))
    ax.plot([0.0, 0.0], [y + 0.06, 1.28], color="#999999", lw=0.8, ls=":")
    ax.plot([xp, xp], [y + 0.06, 1.28], color="#999999", lw=0.8, ls=":")
    ax.text(xp / 2 if xp > 0.08 else 0.07, 1.28, f"x = {x:.2f} m",
            ha="center", va="bottom", fontsize=10)

    # Span L
    ax.text(0.5, -0.72, f"Beam span L = {L:.2f} m", ha="center", fontsize=10, weight="bold")
    ax.set_title("SIMPLE BEAM – point load and support reaction", fontsize=12, weight="bold")
    fig.tight_layout()
    return fig


def compound_diagram(L1, L2, a, W, x):
    """
    Compound Beam geometry:
    - Upper beam AB (span L1): Pin support at A (left), resting on lower beam CD at right end B.
    - Lower beam CD (span L2): Pin support at C (left) with reaction R_C, roller support at D (right).
    - Contact/transfer point is at distance 'a' from D (so distance L2 - a from C).
    - Force transferred from upper to lower beam is F_B = W * x / L1.
    - Reaction at C is R_C = F_B * (L2 - a) / L2 = W * x * (L2 - a) / (L1 * L2).
    """
    fig, ax = plt.subplots(figsize=(10, 4.8))
    setup_ax(ax, ylim=(-1.05, 1.75))

    # Upper beam AB spans x_top in [0.05, 0.75] (visual length 0.70 representing L1)
    x_a, x_b = 0.05, 0.75
    y_top = 1.08
    xp_top = x_a + (x / L1) * (x_b - x_a)

    beam_line(ax, x_a, x_b, y_top, "A", "B")
    draw_support(ax, x_a, y_top - 0.02, "pin", "A (Pin)")

    # Applied load W on upper beam AB
    arrow_len = 0.20 + 0.20 * min(W / 15.0, 1.0)
    draw_arrow(
        ax, xp_top, y_top + 0.50, y_top + 0.50 - arrow_len,
        f"W = {W:.2f} N", "#d62728", label_dx=0.085, fontsize=10
    )

    # Lower beam CD spans x_low in [0.20, 0.95] (visual length 0.75 representing L2)
    x_c, x_d = 0.20, 0.95
    y_low = 0.22
    # Contact point on lower beam CD is at distance 'a' from D (right end)
    x_contact = x_d - (a / L2) * (x_d - x_c)

    beam_line(ax, x_c, x_d, y_low, "C", "D")
    draw_support(ax, x_c, y_low - 0.02, "pin", "C (Pin)")
    draw_support(ax, x_d, y_low - 0.02, "roller", "D (Roller)")

    # Transferred load F_B from upper beam B to lower beam at contact point
    FB = W * x / L1
    ax.plot([x_b, x_contact], [y_top - 0.04, y_low + 0.16], color="#555555", lw=1.2, ls="--")
    draw_arrow(
        ax, x_contact, y_low + 0.44, y_low + 0.06,
        f"F_B = {FB:.2f} N", "#e67e22", label_dx=0.10, fontsize=9.5
    )

    # Reaction arrow R_C at C
    draw_arrow(ax, x_c, y_low - 0.52, y_low - 0.05, "Rᶜ", "#1f77b4", label_dx=-0.06, fontsize=11)

    # Dimension x from A on upper beam
    ax.annotate("", xy=(xp_top, 1.48), xytext=(x_a, 1.48),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color="black"))
    ax.text((x_a + xp_top) / 2, 1.51, f"x = {x:.2f} m", ha="center", va="bottom", fontsize=9.5)

    # Dimension L1 on upper beam
    ax.annotate("", xy=(x_b, 1.66), xytext=(x_a, 1.66),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color="black"))
    ax.text((x_a + x_b) / 2, 1.69, f"L₁ = {L1:.2f} m", ha="center", va="bottom", fontsize=10)

    # Dimension 'a' from D to contact point on lower beam
    ax.annotate("", xy=(x_d, -0.58), xytext=(x_contact, -0.58),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color="#444444"))
    ax.text((x_contact + x_d) / 2, -0.61, f"a = {a:.2f} m", ha="center", va="top", fontsize=9.5)

    # Summary dimensions footer
    ax.text(
        0.5, -0.92,
        f"Upper beam span L₁ = {L1:.2f} m   |   Lower beam span L₂ = {L2:.2f} m   |   Distance a (from D) = {a:.2f} m",
        ha="center", fontsize=10, weight="bold"
    )
    ax.set_title("COMPOUND BEAM – upper beam AB transferring load to lower beam CD", fontsize=12, weight="bold")
    fig.tight_layout()
    return fig


def render_comparison(analytical_val: float, experimental_val: float, label: str):
    st.divider()
    st.subheader("Analytical vs. Experimental Comparison")
    m1, m2, m3 = st.columns(3)
    m1.metric(f"Analytical {label}", f"{analytical_val:.3f} N")
    m2.metric(f"Experimental {label}", f"{experimental_val:.3f} N")

    if analytical_val == 0.0:
        m3.metric("% Error (w.r.t. Analytical)", "Undefined (R_analytical = 0)")
        st.warning("Analytical reaction is 0.000 N (e.g., when x = 0), so % error w.r.t. analytical cannot be calculated.")
    else:
        pct_error = ((experimental_val - analytical_val) / analytical_val) * 100.0
        m3.metric("% Error (w.r.t. Analytical)", f"{pct_error:+.2f}%")
        st.latex(
            r"\%\text{ Error} = \frac{R_{\text{experimental}} - R_{\text{analytical}}}{R_{\text{analytical}}} \times 100"
        )


if mode == "Simple Beam":
    st.subheader("Simple Beam – change the values")
    c1, c2, c3, c4 = st.columns(4)
    L = c1.number_input("Span L (m)", min_value=0.10, value=1.00, step=0.10)
    W = c2.number_input("External load W (N)", min_value=0.01, value=5.88, step=0.10)
    x = c3.number_input("Load distance x from A (m)", min_value=0.00, value=0.20, step=0.05)
    R_exp = c4.number_input("Experimental reaction Rᴮ,exp (N)", min_value=0.00, value=1.18, step=0.01, format="%.3f")

    if x > L:
        st.error("The load position x cannot be greater than the beam span L.")
    else:
        RB_analytical = W * x / L
        st.pyplot(simple_diagram(L, W, x), use_container_width=True)
        st.latex(r"R_B = \frac{Wx}{L}")
        st.caption("The red arrow marks the applied load W. The blue arrow marks reaction Rᴮ.")
        render_comparison(RB_analytical, R_exp, "Reaction Rᴮ")

else:
    st.subheader("Compound Beam – change the values")
    c1, c2, c3 = st.columns(3)
    L1 = c1.number_input("Upper beam span L₁ (m)", min_value=0.10, value=1.00, step=0.10)
    L2 = c2.number_input("Lower beam span L₂ (m)", min_value=0.10, value=1.00, step=0.10)
    a = c3.number_input("Distance a from D (m)", min_value=0.00, value=0.20, step=0.05)

    c4, c5, c6 = st.columns(3)
    W = c4.number_input("External load W (N)", min_value=0.01, value=7.84, step=0.10)
    x = c5.number_input("Load distance x from A (m)", min_value=0.00, value=0.20, step=0.05)
    R_exp = c6.number_input("Experimental reaction Rᶜ,exp (N)", min_value=0.00, value=0.31, step=0.01, format="%.3f")

    if x > L1:
        st.error("The load position x cannot be greater than L₁.")
    elif a >= L2:
        st.error("Distance a must be smaller than L₂.")
    else:
        RC_analytical = W * x * (L2 - a) / (L1 * L2)
        st.pyplot(compound_diagram(L1, L2, a, W, x), use_container_width=True)
        st.latex(r"R_C = \frac{Wx(L_2-a)}{L_1L_2}")
        st.caption("Red: applied load W | Orange: transferred load F_B onto lower beam | Blue: reaction Rᶜ.")
        render_comparison(RC_analytical, R_exp, "Reaction Rᶜ")
