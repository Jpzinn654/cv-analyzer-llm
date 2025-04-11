import os, time
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from services.database import AnalyseDatabase
from utils.resume_analysis import ResumeAnalysis

class JobAnalysisApp:

    def __init__(self):
        # Inicializa a base de dados
        self.database = AnalyseDatabase()
        self.job = None
        self.df = None
        self.data = None

    def load_job_data(self, job_name):
        """Carrega dados de uma vaga selecionada."""
        self.job = self.database.get_job_by_name(job_name)
        self.data = self.database.get_analisis_by_job_id(self.job.get('id'))

        # Cria um DataFrame do Pandas para armazenar os dados das análises
        self.df = pd.DataFrame(
            self.data if self.data else {},
            columns=[
                'name',
                'education',
                'skills',
                'languages',
                'score',
                'resum_id',
                'id'
            ]
        )

        # Renomeia as colunas para melhorar a legibilidade
        self.df.rename(
            columns={
                'name': 'Nome',
                'education': 'Educação',
                'skills': 'Habilidades',
                'languages': 'Idiomas',
                'score': 'Score',
                'resum_id': 'Resum ID',
                'id': 'ID'
            },
            inplace=True
        )

    def display_job_selector(self):
        """Exibe a seleção da vaga para o usuário."""
        select = st.selectbox(
            "Escolha sua vaga:",
            [job.get('name') for job in self.database.jobs.all()],
            index=None
        )
        btn = st.button('Gerar Análise')

        if btn:
            with st.spinner("Carregando os currículos", show_time=True):
                ResumeAnalysis(job_name=select).run()
                time.sleep(100)
        return select

    def display_candidate_chart(self):
        """Exibe o gráfico de barras com as pontuações dos candidatos."""
        st.subheader('Classificação dos Candidatos')
        st.bar_chart(self.df, x="Nome", y="Score", color="Nome", horizontal=True)

    def display_candidate_table(self):
        """Exibe a tabela interativa com os candidatos."""
        gb = GridOptionsBuilder.from_dataframe(self.df)
        gb.configure_pagination(paginationAutoPageSize=True)

        # Ordena pela coluna 'Score'
        gb.configure_column("Score", header_name="Score", sort="desc")
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)  # Adiciona seleção com checkboxes

        grid_options = gb.build()

        response = AgGrid(
            self.df,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme='streamlit',
        )

        return response.get('selected_rows', [])

    def delete_files_resum(self, resums):
        """Deleta os arquivos dos currículos."""
        for resum in resums:
            path = resum.get('file')
            if os.path.isfile(path):
                os.remove(path)

    def clear_analysis(self):
        """Limpa a análise e deleta os arquivos relacionados aos currículos."""
        resums = self.database.get_resums_by_job_id(self.job.get('id'))
        self.database.delete_all_resums_by_job_id(self.job.get('id'))
        self.database.delete_all_analysis_by_job_id(self.job.get('id'))
        self.database.delete_all_files_by_job_id(self.job.get('id'))
        self.delete_files_resum(resums)
        st.rerun()  # Recarrega a página

    def display_resumes(self, candidates_df):
        """Exibe os currículos dos candidatos selecionados."""
        if not candidates_df.empty:
            cols = st.columns(len(candidates_df))  # Cria colunas para exibir os currículos
            for idx, row in enumerate(candidates_df.iterrows()):
                with cols[idx]:  # Exibe cada currículo em uma coluna
                    with st.container():
                        if resum_data := self.database.get_resum_by_id(row[1]['Resum ID']):
                            st.markdown(resum_data.get('content'))  # Exibe o resumo do currículo
                            st.markdown(resum_data.get('opinion'))  # Exibe a opinião da IA sobre o currículo

                            # Exibe um botão para download do currículo em PDF
                            with open(resum_data.get('file'), "rb") as pdf_file:
                                pdf_data = pdf_file.read()
                                st.download_button(
                                    label=f"Download Currículo {row[1]['Nome']}",
                                    data=pdf_data,
                                    file_name=f"{row[1]['Nome']}.pdf",
                                    mime="application/pdf"
                                )

    def run(self):
        """Método principal para rodar o aplicativo."""
        option = self.display_job_selector()

        if option:
            self.load_job_data(option)
            self.display_candidate_chart()

            selected_candidates = self.display_candidate_table()
            candidates_df = pd.DataFrame(selected_candidates)

            # Botão para limpar as análises e deletar os currículos
            if st.button('Limpar Análise'):
                self.clear_analysis()

            self.display_resumes(candidates_df)


# Executa a função principal quando o script é chamado diretamente
if __name__ == "__main__":
    app = JobAnalysisApp()
    app.run()