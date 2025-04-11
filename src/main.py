import streamlit as st
from screens.position import Position
from screens.analysis import JobAnalysisApp

st.set_page_config(layout="wide", page_title="Recrutador", page_icon=":brain:")

def page_1():
    st.title("Página 1")
    st.write("Bem-vindo à Página 1!")

# Função de Navegação
def main():
    # Criação do menu lateral (drawer)
    menu = st.sidebar.selectbox("Escolha uma página", ("Criar Vaga", "Análise de currículos"))

    # Redireciona para a página selecionada
    if menu == "Criar Vaga":
        Position().run()
    elif menu == "Análise de currículos":
        JobAnalysisApp().run()

# Execução do App
if __name__ == "__main__":
    main()