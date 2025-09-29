import streamlit as st
import pandas as pd
from io import BytesIO

# Dicionário de categorias e percentuais
CATEGORIAS = {
    "Moradia": 0.25,
    "Alimentação": 0.12,
    "Transporte": 0.08,
    "Saúde": 0.08,
    "Educação": 0.06,
    "Despesas Pessoais": 0.06,
    "Lazer e Entretenimento": 0.06,
    "Pets": 0.03,
    "Impostos e Taxas": 0.03,
    "Reserva / Valor Extra": 0.17
}

def calcular_gastos(total_renda):
    """Calcula os valores por categoria com base na renda total."""
    dados = {
        "Categoria": [],
        "Percentual": [],
        "Valor Estimado (R$)": []
    }
    for categoria, percentual in CATEGORIAS.items():
        dados["Categoria"].append(categoria)
        dados["Percentual"].append(f"{percentual * 100}%")
        dados["Valor Estimado (R$)"].append(round(total_renda * percentual, 2))
    return pd.DataFrame(dados)

def gerar_excel(df):
    """Gera um arquivo Excel em memória."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Planejamento Financeiro', index=False)
    output.seek(0)
    return output

def main():
    st.set_page_config(page_title="Organizador Financeiro", layout="centered")
    st.title("💰 Planejador Financeiro Pessoal/Familiar")

    st.markdown("""
    Este sistema calcula a distribuição ideal de seus gastos mensais com base na sua **renda**.
    """)
    
    # Entrada principal
    renda_base = st.number_input("Informe sua Renda Mensal (R$):", min_value=0.0, step=100.0, format="%.2f")

    # Entradas adicionais
    st.markdown("### 💼 Entradas adicionais (opcional)")
    renda_extra = st.number_input("Renda Extra / Freelance (R$):", min_value=0.0, step=50.0, format="%.2f")
    decimo_terceiro = st.number_input("13º Salário (R$):", min_value=0.0, step=50.0, format="%.2f")
    outros_valores = st.number_input("Outros valores recebidos (R$):", min_value=0.0, step=50.0, format="%.2f")

    if st.button("Calcular Planejamento"):
        total_renda = renda_base + renda_extra + decimo_terceiro + outros_valores
        if total_renda <= 0:
            st.warning("Insira pelo menos a renda mensal ou outro valor adicional.")
            return

        st.success(f"Renda Total Considerada: R$ {total_renda:.2f}")

        df = calcular_gastos(total_renda)
        st.dataframe(df, use_container_width=True)

        # Download do Excel
        excel_file = gerar_excel(df)
        st.download_button(
            label="📥 Baixar Planilha Excel",
            data=excel_file,
            file_name="planejamento_financeiro.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()
