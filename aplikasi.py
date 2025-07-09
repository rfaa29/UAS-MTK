# Streamlit App: Optimasi Produksi (Linear Programming)
# Dibuat menggunakan Streamlit dan PuLP

import streamlit as st
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, value

st.set_page_config(page_title="Optimasi Produksi", layout="centered")
st.title("Optimasi Produksi dengan Linear Programming")

# Input jumlah produk dan jumlah kendala
jumlah_produk = st.number_input("Masukkan jumlah produk:", min_value=1, value=2)
jumlah_kendala = st.number_input("Masukkan jumlah kendala:", min_value=1, value=2)

# Input koefisien keuntungan tiap produk
default_profit = ",".join(["0"] * jumlah_produk)
input_profit = st.text_input(
    "Masukkan koefisien keuntungan per produk (pisahkan dengan koma):",
    value=default_profit
)

def parse_input(s, n):
    try:
        items = [float(x.strip()) for x in s.split(",") if x.strip()]
        return items + [0.0] * (n - len(items))
    except:
        return [0.0] * n

profit_vector = parse_input(input_profit, jumlah_produk)

# Input kendala
st.subheader("Masukkan Koefisien Kendala dan RHS")
kendala_list = []
for i in range(jumlah_kendala):
    default_k = ",".join(["0"] * jumlah_produk)
    coeff_str = st.text_input(
        f"Koefisien kendala {i+1} (pisahkan dengan koma):",
        value=default_k,
        key=f"kendala_{i}"
    )
    rhs = st.number_input(f"Batas kendala (RHS) {i+1}:", value=0.0, key=f"rhs_{i}")
    kendala_list.append({
        "koef": parse_input(coeff_str, jumlah_produk),
        "rhs": rhs
    })

# Tombol solve
if st.button("Hitung Solusi Optimal"):
    # Inisialisasi model
    model = LpProblem("Optimasi_Produksi", LpMaximize)
    
    # Variabel keputusan
    x = [LpVariable(f"x{i+1}", lowBound=0) for i in range(jumlah_produk)]

    # Fungsi tujuan
    model += lpSum([profit_vector[i] * x[i] for i in range(jumlah_produk)]), "Total_Keuntungan"

    # Tambah kendala
    for i, k in enumerate(kendala_list):
        model += lpSum([k["koef"][j] * x[j] for j in range(jumlah_produk)]) <= k["rhs"], f"Kendala_{i+1}"

    # Solve
    model.solve()

    # Output
    st.subheader("Hasil Optimasi")
    st.write("Status:", LpStatus[model.status])

    hasil = {f"x{i+1}": value(var) for i, var in enumerate(x)}
    df = pd.DataFrame(hasil.items(), columns=["Variabel", "Nilai Optimal"])
    st.dataframe(df)
    st.success(f"Total keuntungan maksimum: {value(model.objective)}")

st.markdown("---")
st.markdown("Aplikasi ini menyelesaikan persoalan Linear Programming dengan metode Simpleks dari pustaka PuLP.")
            st.session_state['steps'] = steps
            st.session_state['result_expr'] = result_expr
            st.session_state['plot_expr'] = result_expr if isinstance(result_expr, sp.Expr) else sp.diff(f, x) if operation=="Integral Tentu" else result_expr
            st.session_state['domain'] = (min_x, max_x)

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

with col_results:
    st.subheader("Langkah Perhitungan")
    if 'steps' in st.session_state:
        for s in st.session_state['steps']:
            st.latex(s)
        st.markdown("---")
        st.subheader("Hasil Akhir")
        st.latex(sp.latex(st.session_state['result_expr']))

        # Plot
        expr_plot = st.session_state['plot_expr']
        dom = st.session_state['domain']
        # Lambdify for numeric plot
        func = sp.lambdify(x, expr_plot, 'numpy')
        xs = np.linspace(dom[0], dom[1], 400)
        ys = func(xs)
        fig, ax = plt.subplots()
        ax.plot(xs, ys)
        ax.set_title(f"Plot dari {'derivative' if operation=='Turunan' else 'integral'}")
        ax.set_xlabel(var)
        ax.set_ylabel('y')
        st.pyplot(fig)
    else:
        st.write("Klik tombol 'Hitung dan Plot' di samping untuk melihat langkah dan grafik...")

# Footer
st.markdown("---")
st.caption("© 2025 Kalkulator Matematika Streamlit")
