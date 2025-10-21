import streamlit as st
import groq
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Justus - Assistente Jurídico Sênior",
    page_icon="⚖️",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .justus-response {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .user-message {
        background-color: #e6f3ff;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class JustusAssistant:
    def __init__(self):
        self.client = groq.Groq(api_key=st.secrets["GROQ_API_KEY"])
    
    def consultar_ia(self, pergunta):
        try:
            response = self.client.chat.completions.create(
                model="llama2-70b-4096",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é o Justus, assistente jurídico sênior especializado em direito brasileiro. Forneça respostas precisas e fundamentadas. Sempre cite artigos de lei quando possível. ⚠️ AVISO: Esta resposta não substitui consulta com advogado."
                    },
                    {
                        "role": "user", 
                        "content": pergunta
                    }
                ],
                temperature=0.3,
                max_tokens=1024
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Erro: {str(e)}"

def main():
    st.markdown('<h1 class="main-header">⚖️ JUSTUS</h1>', unsafe_allow_html=True)
    st.markdown("### Seu Assistente Jurídico em IA")
    
    if 'justus' not in st.session_state:
        st.session_state.justus = JustusAssistant()
        st.session_state.historico = []
    
    with st.sidebar:
        st.title("Menu Justus")
        opcao = st.radio(
            "Selecione:",
            ["💬 Chat Jurídico", "📅 Calculadora de Prazos", "🔍 Pesquisar Jurisprudência"]
        )
        
        if st.button("🧹 Limpar Histórico"):
            st.session_state.historico = []
            st.success("Histórico limpo!")

    if opcao == "💬 Chat Jurídico":
        st.header("💬 Chat Jurídico")
        
        for msg in st.session_state.historico:
            if msg["tipo"] == "usuario":
                st.markdown(f'<div class="user-message"><strong>👤 Você:</strong> {msg["conteudo"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="justus-response"><strong>⚖️ Justus:</strong> {msg["conteudo"]}</div>', unsafe_allow_html=True)
        
        pergunta = st.text_input("Digite sua pergunta jurídica:")
        if st.button("🚀 Enviar") and pergunta:
            with st.spinner("Justus está pesquisando..."):
                st.session_state.historico.append({"tipo": "usuario", "conteudo": pergunta})
                resposta = st.session_state.justus.consultar_ia(pergunta)
                st.session_state.historico.append({"tipo": "justus", "conteudo": resposta})
            st.rerun()

    elif opcao == "📅 Calculadora de Prazos":
        st.header("📅 Calculadora de Prazos")
        
        col1, col2 = st.columns(2)
        with col1:
            tipo_prazo = st.selectbox("Tipo de prazo:", ["Contestação Trabalhista", "Apelação Cível", "Recurso Especial"])
            data_inicio = st.date_input("Data do evento:", datetime.now())
        
        with col2:
            if st.button("🔄 Calcular Prazo"):
                pergunta = f"Calcule o prazo para {tipo_prazo} a partir de {data_inicio}. Cite o artigo de lei."
                with st.spinner("Calculando..."):
                    resposta = st.session_state.justus.consultar_ia(pergunta)
                    st.markdown(f'<div class="justus-response">{resposta}</div>', unsafe_allow_html=True)

    elif opcao == "🔍 Pesquisar Jurisprudência":
        st.header("🔍 Pesquisa Jurídica")
        
        termos = st.text_input("Termos para pesquisa:")
        if st.button("🔎 Pesquisar") and termos:
            pergunta = f"Pesquise jurisprudência sobre: {termos}"
            with st.spinner("Pesquisando..."):
                resposta = st.session_state.justus.consultar_ia(pergunta)
                st.markdown(f'<div class="justus-response">{resposta}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
