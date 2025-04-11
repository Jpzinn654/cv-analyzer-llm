import sys, os, uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from helper import extract_data_analysis, get_pdf_paths, read_pdf
from src.services.database import AnalyseDatabase
from src.llm.ai import GroqClient
from src.models.resum import Resum
from src.models.file import File

database = AnalyseDatabase()
ai = GroqClient()
job = database.get_job_by_name('Vaga Jovem Aprendiz Desenvolvedor')
print(type(job))  # Verificar o tipo
print(job)

cv_paths = get_pdf_paths(dir=r'utils\curriculos')

for path in cv_paths:
    content = read_pdf(path)
    resum = ai.resum_cv(content)
    opinion = ai.generate_opnion(content, job)
    score = ai.generate_score(content, job)

    resum_schema = Resum(
        id=str(uuid.uuid4()),
        job_id=job.get('id'),
        content=resum,
        file=str(path),
        opinion=opinion,
    )

    file_schema = File(
        id=str(uuid.uuid4()),
        job_id=job.get('id'),
    )

    analisys_schema = extract_data_analysis(
        resum, resum_schema.job_id, resum_schema.id, score
    )
    print(analisys_schema.model_dump())
    print(resum_schema.model_dump())
    print(file_schema.model_dump())

    database.resums.insert(resum_schema.model_dump())
    database.analysis.insert(analisys_schema.model_dump())
    database.files.insert(file_schema.model_dump())