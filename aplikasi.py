import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="Kalkulator Turunan & Integral",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom styling
st.markdown("""
<style>
body {background-color: #f5f5f5;}
.stApp {font-family: 'Segoe UI', sans-serif;}
h1 {text-align: center; color: #2c3e50;}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🧮 Kalkulator Turunan & Integral")

# Columns: results (left), inputs (right)
col_results, col_input = st.columns([2, 3])

with col_input:
    st.subheader("Masukkan Fungsi & Pilih Operasi")
    expr_input = st.text_area("Fungsi f(x):", "x**3 + 2*x**2 - 5*x + 1", height=150)
    var = st.text_input("Variabel (misal: x):", "x")
    operation = st.selectbox("Operasi:", ["Turunan", "Integral Tak Tentu", "Integral Tentu"])

    if operation == "Integral Tentu":
        a = st.text_input("Batas Bawah:", "0")
        b = st.text_input("Batas Atas:", "1")

    # Domain untuk plotting
    min_x = st.number_input("Domain Plot: Batas Bawah", value=-10.0)
    max_x = st.number_input("Domain Plot: Batas Atas", value=10.0)

    if st.button("Hitung dan Plot"):  
        try:
            x = sp.Symbol(var)
            f = sp.sympify(expr_input)
            steps = []
            # Compute
            if operation == "Turunan":
                terms = f.as_ordered_terms()
                for term in terms:
                    d = sp.diff(term, x)
                    steps.append(f"d/d{var}({sp.latex(term)}) = {sp.latex(d)}")
                result_expr = sp.diff(f, x)
            elif operation == "Integral Tak Tentu":
                terms = f.as_ordered_terms()
                for term in terms:
                    integ = sp.integrate(term, x)
                    steps.append(f"∫({sp.latex(term)})d{var} = {sp.latex(integ)} + C")
                result_expr = sp.integrate(f, x)
            else:
                low = sp.sympify(a)
                high = sp.sympify(b)
                F = sp.integrate(f, x)
                steps.append(f"F(x) = {sp.latex(F)} + C")
                Fb = F.subs(x, high);
                Fa = F.subs(x, low)
                steps.append(f"F({sp.latex(high)}) - F({sp.latex(low)}) = {sp.latex(Fb)} - {sp.latex(Fa)} = {sp.latex(Fb - Fa)}")
                result_expr = Fb - Fa

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
