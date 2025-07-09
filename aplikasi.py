import streamlit as st
import pulp
import pandas as pd

st.set_page_config(page_title="Aplikasi Optimasi Produksi", layout="centered")
st.title("Aplikasi Optimasi Produksi (Linear Programming)")

# Input jumlah produk dan kendala
n = st.number_input("Jumlah Produk", min_value=1, step=1, value=2)
m = st.number_input("Jumlah Kendala", min_value=1, step=1, value=2)

# Input koefisien fungsi tujuan
def parse_list(input_str, length):
    try:
        vals = [float(x.strip()) for x in input_str.split(",") if x.strip()]
        if len(vals) < length:
            vals += [0.0] * (length - len(vals))
        return vals[:length]
    except:
        return [0.0] * length

profit_input = st.text_input(
    "Masukkan koefisien profit per produk (pisahkan dengan koma)",
    value=",").join(["0"] * n)
);
profits = parse_list(profit_input, int(n))

# Input kendala
constraints = []
for i in range(int(m)):
    coeff_str = st.text_input(
        f"Koefisien kendala {i+1} (pisahkan dengan koma)",
        value=",").join(["0"] * n)
    rhs = st.number_input(f"Batas RHS kendala {i+1}", value=0.0, key=f"rhs_{i}")
    constraints.append({"coeff": parse_list(coeff_str, int(n)), "rhs": float(rhs)})

# Tombol solve
if st.button("Solve"):
    # Definisi model
    prob = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)
    # Variabel keputusan
    x = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(int(n))]
    # Fungsi tujuan
    prob += pulp.lpSum([profits[i] * x[i] for i in range(int(n))]), "Total_Profit"
    # Tambah kendala
    for idx, con in enumerate(constraints):
        prob += pulp.lpSum([con["coeff"][j] * x[j] for j in range(int(n))]) <= con["rhs"], f"Constraint_{idx+1}"
    # Solve
    prob.solve()

    # Hasil
    status = pulp.LpStatus[prob.status]
    sol = {f"x{i+1}": float(pulp.value(var)) for i, var in enumerate(x)}
    total_profit = float(pulp.value(prob.objective))

    st.subheader("Hasil Optimasi")
    st.write("Status Solving:", status)
    df_sol = pd.DataFrame.from_dict(sol, orient="index", columns=["Nilai Optimal"])  
    st.dataframe(df_sol)
    st.write(f"**Total Profit Optimal:** {total_profit}")

# Info tambahan
st.markdown("---")
st.markdown("Aplikasi ini menggunakan library **PuLP** untuk menyelesaikan masalah Linear Programming.")
st.markdown("Masukkan parameter sesuai kebutuhan, lalu klik tombol **Solve** untuk mendapatkan solusi optimal.")
