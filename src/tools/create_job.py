import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database import AnalyseDatabase
import uuid
from src.models.job import Job

database = AnalyseDatabase()

name = 'Vaga Desenvolvedor Senior'
activies = 'Ser desenvolvedor senior, ter mais de 5 anos de experiencias com python'
prerequisities = 'Experiencia comprovado como gestor/senior'
diferentials = 'Saber AWS'

job = Job(
    id=str(uuid.uuid4()),
    name=name,
    main_activies=activies,
    prerequisities=prerequisities,
    diferentials=diferentials
)

database.jobs.insert(job.model_dump()) # Inseri um dicionário