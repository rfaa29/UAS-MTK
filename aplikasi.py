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

Tujuan: **Memaksimalkan total keuntungan** dengan batasan waktu mesin dan jumlah produksi maksimal.
""")

# Input
st.subheader("📥 Input Parameter")

col1, col2 = st.columns(2)
with col1:
    profit_A = st.number_input("Keuntungan per unit Produk A (x)", min_value=0.0, value=80.0)
    waktu_mesin1 = st.number_input("Batas waktu Mesin 1 (misal: x + y ≤ ...)", min_value=0.0, value=330.0)
    jumlah_maks_A = st.number_input("Jumlah maksimum Produk A (x)", min_value=0.0, value=100.0)

with col2:
    profit_B = st.number_input("Keuntungan per unit Produk B (y)", min_value=0.0, value=50.0)
    waktu_mesin2 = st.number_input("Batas waktu Mesin 2 (misal: 2x + y ≤ ...)", min_value=0.0, value=440.0)
    jumlah_maks_B = st.number_input("Jumlah maksimum Produk B (y)", min_value=0.0, value=120.0)

# Cek validitas input
if all(v > 0 for v in [profit_A, profit_B, waktu_mesin1, waktu_mesin2, jumlah_maks_A, jumlah_maks_B]):
    # Fungsi tujuan
    c = [-profit_A, -profit_B]

    # Batasan
    A = [
        [1, 1],     # Mesin 1: x + y ≤ ...
        [2, 1],     # Mesin 2: 2x + y ≤ ...
        [1, 0],     # x ≤ jumlah_maks_A
        [0, 1]      # y ≤ jumlah_maks_B
    ]
    b = [waktu_mesin1, waktu_mesin2, jumlah_maks_A, jumlah_maks_B]

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None), method='highs')

    # Visualisasi
    st.subheader("📊 Visualisasi Area Feasible dan Solusi Optimal")

    x_vals = np.linspace(0, max(jumlah_maks_A, waktu_mesin1, waktu_mesin2), 400)
    y1 = waktu_mesin1 - x_vals
    y2 = waktu_mesin2 - 2 * x_vals
    y3 = np.full_like(x_vals, jumlah_maks_B)  # y ≤ jumlah_maks_B
    y4 = np.maximum(0, np.full_like(x_vals, 0))  # y ≥ 0

    fig, ax = plt.subplots()
    ax.plot(x_vals, y1, label=f"x + y ≤ {waktu_mesin1}", color='blue')
    ax.plot(x_vals, y2, label=f"2x + y ≤ {waktu_mesin2}", color='green')
    ax.axhline(jumlah_maks_B, color='purple', linestyle='--', label=f"y ≤ {jumlah_maks_B}")
    ax.axvline(jumlah_maks_A, color='orange', linestyle='--', label=f"x ≤ {jumlah_maks_A}")

    # Area feasible (approx.)
    y_feasible = np.minimum(np.minimum(y1, y2), jumlah_maks_B)
    y_feasible = np.maximum(y_feasible, 0)
    x_limit = x_vals[x_vals <= jumlah_maks_A]
    y_limit = y_feasible[:len(x_limit)]
    ax.fill_between(x_limit, 0, y_limit, where=(y_limit >= 0), color='lightgrey', alpha=0.5, label='Feasible Region')

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

    # Hasil akhir
    if res.success:
        st.subheader("✅ Hasil Optimasi")
        st.success(f"""
        
        st.subheader("📦 Jumlah Produksi Optimal (Bar Chart)")
        fig2, ax2 = plt.subplots()
        ax2.bar(["Produk A (Kipas Angin)", "Produk B (Blender)"], [x_opt, y_opt], color=["skyblue", "salmon"])
        ax2.set_ylabel("Unit")
        ax2.set_ylim(0, max(jumlah_maks_A, jumlah_maks_B) * 1.2)
        ax2.set_title("Produksi Optimal per Produk")
        st.pyplot(fig2)

        # Gantt-like chart pemanfaatan mesin
        st.subheader("⚙️ Pemanfaatan Mesin (Gantt-like Chart)")
        pemakaian_mesin1 = x_opt + y_opt
        pemakaian_mesin2 = 2 * x_opt + y_opt

        fig3, ax3 = plt.subplots()
        mesin_labels = ["Mesin 1", "Mesin 2"]
        durasi_pakai = [pemakaian_mesin1, pemakaian_mesin2]
        kapasitas = [waktu_mesin1, waktu_mesin2]

        ax3.barh(mesin_labels, kapasitas, color="lightgrey", label="Total Kapasitas")
        ax3.barh(mesin_labels, durasi_pakai, color="steelblue", label="Waktu Terpakai")
        ax3.set_xlabel("Jam")
        ax3.set_title("Utilisasi Mesin Produksi")
        ax3.legend()
        st.pyplot(fig3)

        Kombinasi Produk Optimal:
        - Produk A (x): **{x_opt:.2f} unit**
        - Produk B (y): **{y_opt:.2f} unit**

        Total Keuntungan Maksimum: **Rp {-res.fun:,.2f} juta**
        """)
    else:
        st.error("Optimisasi gagal. Solver tidak menemukan solusi yang memenuhi.")
else:
    st.warning("⚠️ Semua nilai input harus lebih dari 0.")
