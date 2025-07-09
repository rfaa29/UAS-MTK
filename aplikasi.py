import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

st.set_page_config(page_title="Optimasi Produksi", layout="centered")

st.title("📈 Optimasi Produksi (Linear Programming)")

st.markdown("""
Sebuah pabrik memproduksi dua produk:
- Produk A (`x`) = Kipas Angin
- Produk B (`y`) = Blender

Tujuan: **Memaksimalkan total keuntungan** dengan batasan waktu dari dua mesin.
""")

# Input
st.subheader("📥 Input Parameter")

col1, col2 = st.columns(2)
with col1:
    profit_A = st.number_input("Keuntungan per unit Produk A (x)", min_value=0.0, value=40.0)
    waktu_mesin1 = st.number_input("Batas waktu Mesin 1 (misal: x + y ≤ ...)", min_value=0.0, value=15.0)
with col2:
    profit_B = st.number_input("Keuntungan per unit Produk B (y)", min_value=0.0, value=30.0)
    waktu_mesin2 = st.number_input("Batas waktu Mesin 2 (misal: 2x + y ≤ ...)", min_value=0.0, value=20.0)

# Cek input
if profit_A > 0 and profit_B > 0 and waktu_mesin1 > 0 and waktu_mesin2 > 0:
    # Model LP
    c = [-profit_A, -profit_B]
    A = [[1, 1], [2, 1]]
    b = [waktu_mesin1, waktu_mesin2]

    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    # Visualisasi
    st.subheader("📊 Visualisasi Area Feasible dan Solusi Optimal")

    x_vals = np.linspace(0, max(waktu_mesin1, waktu_mesin2) + 5, 400)
    y1 = waktu_mesin1 - x_vals           # x + y ≤ waktu_mesin1
    y2 = waktu_mesin2 - 2 * x_vals       # 2x + y ≤ waktu_mesin2

    fig, ax = plt.subplots()
    ax.plot(x_vals, y1, label=f"x + y ≤ {waktu_mesin1}", color='blue')
    ax.plot(x_vals, y2, label=f"2x + y ≤ {waktu_mesin2}", color='green')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

    # Area feasible
    y_feasible = np.minimum(y1, y2)
    y_feasible = np.maximum(y_feasible, 0)
    ax.fill_between(x_vals, 0, y_feasible, where=(y_feasible >= 0), color='lightgrey', alpha=0.5, label='Feasible Region')

    # Solusi optimal
    if res.success:
        x_opt, y_opt = res.x
        ax.plot(x_opt, y_opt, 'ro', label='Solusi Optimal')
        ax.annotate(f"({x_opt:.2f}, {y_opt:.2f})", (x_opt, y_opt), textcoords="offset points", xytext=(10,10))

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Produk A (x)")
    ax.set_ylabel("Produk B (y)")
    ax.set_title("Feasible Region dan Solusi Optimal")
    ax.legend()
    st.pyplot(fig)

    # Hasil Optimasi
    if res.success:
        st.subheader("✅ Hasil Optimasi")
        st.success(f"""
        Kombinasi Produk Optimal:
        - Produk A (x): **{x_opt:.2f} unit**
        - Produk B (y): **{y_opt:.2f} unit**

        Total Keuntungan Maksimum: **Rp {-res.fun:,.2f} juta**
        """)
    else:
        st.error("Optimisasi gagal. Solver tidak menemukan solusi yang memenuhi.")
else:
    st.warning("⚠️ Harap masukkan semua nilai input dengan benar (lebih dari nol).")
