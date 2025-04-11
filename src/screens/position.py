import uuid
import streamlit as st
from services.database import AnalyseDatabase
from models.job import Job

class Position:

    def __init__(self):
        self.jobname = []
        self.activies = []
        self.requisities = []
        self.differentials = []

        self.database = AnalyseDatabase()

    def informations(self):
        
        st.title("Criar Vaga")
        st.text("Preencha as informações nos campos a baixo para criar uma nova vaga para fazer comparações")

        job_name = st.text_input("Nome da vaga")
        activies = st.text_area("Atividades")
        prerequisities = st.text_area("Pré Requisitos")
        differentials = st.text_area("Diferencial")
        
        return job_name, activies, prerequisities, differentials

    def create_job_in_database(self, job_name, activies, prerequisities, differentials):

        button = st.button('Criar vaga')

        if button:
            self.jobname.append(job_name)
            self.activies.append(activies)
            self.differentials.append(differentials)
            self.requisities.append(prerequisities)
        
            job = Job(
                id=str(uuid.uuid4()),
                name=job_name,
                main_activies=activies,
                prerequisities=prerequisities,
                diferentials=differentials
            )

            self.database.jobs.insert(job.model_dump())

            self.popup()

    @st.dialog("Vaga Criada")
    def popup(self):
        st.write("Parabéns a vaga foi criada com sucesso, agora você já pode usa-lá para analises")

    def run(self):
        
        job_name, activies, prerequisities, differentials = self.informations()
        self.create_job_in_database(job_name, activies, prerequisities, differentials)