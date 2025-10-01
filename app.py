import streamlit as st
import pandas as pd
from io import BytesIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
senha = os.environ.get("EMAIL_SENHA")


def enviar_email_feedback(comentario):
    remetente = "andreprogramador@gmail.com"
    destinatario = "andreprogramador@gmail.com"  # pode ser o mesmo ou outro
    senha = ""  # NÃO usar senha de login do Gmail

    assunto = "Novo feedback negativo recebido"
    corpo = f"Comentário recebido no app:\n\n{comentario if comentario else '[Sem comentário]'}"

    # Criação da mensagem
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.attach(MIMEText(corpo, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        return True
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False


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

    # ---------------------------
    # Seção de Feedback
    # ---------------------------
    st.markdown("---")
    st.subheader("📣 Envie seu feedback")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Gostei"):
            st.success("Obrigado pelo feedback positivo! 😊")

    with col2:
        if st.button("👎 Não gostei"):
            with st.form("form_feedback_negativo", clear_on_submit=True):
                comentario = st.text_area("Nos diga o que podemos melhorar (opcional):")
                enviado = st.form_submit_button("Enviar Feedback")
                if enviado:
                    sucesso = enviar_email_feedback(comentario)
                    if sucesso:
                        st.success("Obrigado pelo seu feedback! Ele foi enviado com sucesso. 📩")
                else:
                    st.error("Não foi possível enviar o feedback por e-mail. Tente novamente mais tarde.")

if __name__ == "__main__":
    main()


# Orientações:
# executar: python -m streamlit run app.py
