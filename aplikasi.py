import streamlit as st
import sympy as sp

# Page configuration
st.set_page_config(
    page_title="Kalkulator Turunan & Integral",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
}
.stApp {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1 {
    text-align: center;
    color: #2c3e50;
}
.sidebar .sidebar-content {
    background-color: #ecf0f1;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🧮 Kalkulator Turunan & Integral")

# Sidebar inputs
with st.sidebar:
    st.header("Input Parameter")
    expr_input = st.text_area(
        "Masukkan fungsi f(x):",
        "x**3 + 2*x**2 - 5*x + 1",
        height=100
    )
    var = st.text_input("Variabel (misal: x):", "x")
    operation = st.selectbox("Operasi:", ["Turunan", "Integral Tak Tentu", "Integral Tentu"])

    # Jika integral tentu, tampilkan input batas
    if operation == "Integral Tentu":
        col1, col2 = st.columns(2)
        with col1:
            a = st.text_input("Batas Bawah:", "0")
        with col2:
            b = st.text_input("Batas Atas:", "1")
    
    st.markdown("---")
    # Contoh fungsi
    st.markdown("**Contoh:** x**2, sin(x), exp(x), log(x)")
    if st.button("Hitung"):
        try:
            x = sp.Symbol(var)
            f = sp.sympify(expr_input)

            if operation == "Turunan":
                result = sp.diff(f, x)
                st.subheader("Hasil Turunan")
                st.latex(r"\frac{d}{d%s} %s = %s" % (var, sp.latex(f), sp.latex(result)))

            elif operation == "Integral Tak Tentu":
                result = sp.integrate(f, x)
                st.subheader("Hasil Integral Tak Tentu")
                st.latex(r"\int %s \, d%s = %s + C" % (sp.latex(f), var, sp.latex(result)))

            else:  # Integral Tentu
                low = sp.sympify(a)
                high = sp.sympify(b)
                indef = sp.integrate(f, (x, low, high))
                st.subheader("Hasil Integral Tentu")
                st.latex(r"\int_{%s}^{%s} %s \, d%s = %s" % (
                    sp.latex(low), sp.latex(high), sp.latex(f), var, sp.latex(indef)
                ))
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# Main area with description
st.markdown(
    """
    **Panduan:**
    - Gunakan ekspresi Python untuk fungsi, misalnya `x**2`, `sin(x)`, `exp(x)`, `log(x)`.
    - Untuk integral tentu, masukkan batas bawah dan atas.
    - Hasil ditampilkan dalam format LaTeX yang mudah dibaca.
    """
)

# Footer
st.markdown("---")
st.caption("© 2025 by Kalkulator Matematika Streamlit")
