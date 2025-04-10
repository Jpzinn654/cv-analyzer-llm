from helper import extract_data_analysis, get_pdf_paths, read_pdf
from tools.database import AnalyseDatabase
from llm.ai import GroqClient

database = AnalyseDatabase()
ai = GroqClient()
job = database.get_job_by_name('Vaga Desenvolvedor Senior')

cv_paths = get_pdf_paths(dir='curriculos')

print(cv_paths)