import streamlit as st
import sympy as sp

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

# Create two main columns: results on left, inputs on right (wider)
col_results, col_input = st.columns([2, 3])

with col_input:
    st.subheader("Masukkan Fungsi & Pilih Operasi")
    expr_input = st.text_area(
        "Fungsi f(x):",
        "x**3 + 2*x**2 - 5*x + 1",
        height=150
    )
    var = st.text_input("Variabel (misal: x):", "x")
    operation = st.selectbox("Operasi:", ["Turunan", "Integral Tak Tentu", "Integral Tentu"])
    if operation == "Integral Tentu":
        a = st.text_input("Batas Bawah:", "0")
        b = st.text_input("Batas Atas:", "1")
    if st.button("Hitung"):
        try:
            x = sp.Symbol(var)
            f = sp.sympify(expr_input)
            step_outputs = []

            if operation == "Turunan":
                # Step-by-step: term by term
                terms = f.as_ordered_terms()
                for term in terms:
                    d = sp.diff(term, x)
                    step_outputs.append(f"d/d{var}({sp.latex(term)}) = {sp.latex(d)}")
                total = sp.diff(f, x)

            elif operation == "Integral Tak Tentu":
                terms = f.as_ordered_terms()
                for term in terms:
                    integ = sp.integrate(term, x)
                    step_outputs.append(f"∫({sp.latex(term)})d{var} = {sp.latex(integ)} + C")
                total = sp.integrate(f, x)

            else:  # Integral Tentu
                low = sp.sympify(a)
                high = sp.sympify(b)
                # Antiderivative
                F = sp.integrate(f, x)
                step_outputs.append(f"F(x) = {sp.latex(F)} + C")
                # Evaluate bounds
                Fb = F.subs(x, high)
                Fa = F.subs(x, low)
                step_outputs.append(f"F({sp.latex(high)}) - F({sp.latex(low)}) = {sp.latex(Fb)} - {sp.latex(Fa)} = {sp.latex(Fb - Fa)}")
                total = Fb - Fa

            # Store in session_state to render in results
            st.session_state['steps'] = step_outputs
            st.session_state['result'] = total

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

with col_results:
    st.subheader("Langkah Perhitungan")
    if 'steps' in st.session_state:
        for s in st.session_state['steps']:
            st.latex(s)
        st.markdown("---")
        st.subheader("Hasil Akhir")
        st.latex(sp.latex(st.session_state['result']))
    else:
        st.write("Klik tombol 'Hitung' di samping untuk menampilkan langkah...")

# Footer
st.markdown("---")
st.caption("© 2025 Kalkulator Matematika Streamlit")
