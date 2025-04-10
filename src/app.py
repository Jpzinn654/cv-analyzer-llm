import os
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from tools.database import AnalyseDatabase

database = AnalyseDatabase()

st.set_page_config(layout='wide', page_title='Analizador IA')

options = st.selectbox(
    'Escolha sua vaga:',
    [job.get('name') for job in database.jobs.all()],
    index=None
)

data = None


if options:
    job = database.get_job_by_name(options)
    data = database.get_analisis_by_job_id(job.get('id'))

    df = pd.DataFrame(
        data if data else {},
        columns=[
            'name',
            'education',
            'skills',
            'language',
            'score',
            'resum_id',
            'id',
        ]
    )

    df.rename(
        columns={
            'name': 'Nome',
            'education': 'educação',
            'skills': 'Habilidades',
            'language': 'Linguagens',
            'score': 'Pontos',
            'resum_id': 'Resumo_id',
            'id': 'ID',
        },
        inplace=True
    )

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)

    if data:
        gb.configure_column('score', header_name='score', sorted='desc') # Scores 
        gb.configure_selection(selection_mode='mutiple', use_checkbox=True) # Seleção para escolher candidatos

    grid_options = gb.build() # Construindo tabela com as config acima

    st.subheader('Classificação dos candidatos')
    st.bar_chart(data=df, x='Nome', y='Pontos', color='Nome', horizontal=True) # Rankeando os

    response = AgGrid(
        df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.COLUMN_CHANGED,
        theme='streamlit'
    ) 

    selected_responde = response.get('selected_response', [])
    candidates_df = pd.DataFrame(selected_responde) # Selecionando em tabela os candidatos

    resums = database.get_resums_by_job_id(job.get('id'))

    if st.button("Limpar Análise"):
        database.delete_all_resums_by_job_id(job.get('id'))
        database.delete_all_analisys_by_job_id(job.get('id'))
        database.delete_all_files_by_job_id(job.get('id'))

    def delete_files_resums(resums):
        for resum in resums:
            path = resum.get('file')
            if os.path.exists(path):
                os.remove(path)

    # Renderização colunas separadas
    if not candidates_df.empty:
        cols = st.columns(len(candidates_df))
        for i, row in enumerate(candidates_df.iterrows()):
            with st.container():
                if resum_data := database.get_result_by_id(row[1]['Resum id']):
                    st.markdown(resum_data.get('content'))
                    st.markdown(resum_data.get('opinion'))
                    with open(resum_data.get('file'), 'rb') as file:
                        pdf_data = file.read()
                        st.download_button(label=f"Download curriculo {row[1]['Nome']}",
                                            data=pdf_data,
                                            file_name=f"{row[1]['Nome']}.pdf",
                                            mime='application/pdf')
