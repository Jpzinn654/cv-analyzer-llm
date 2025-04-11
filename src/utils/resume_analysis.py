import sys, os, uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.helper import extract_data_analysis, get_pdf_paths, read_pdf
from src.services.database import AnalyseDatabase
from src.llm.ai import GroqClient
from src.models.resum import Resum
from src.models.file import File

class ResumeAnalysis:

    def __init__(self, job_name):
        
        self.database = AnalyseDatabase()
        self.ai = GroqClient()
        self.job = self.database.get_job_by_name({job_name})

    def generate_analysis_from_resumes(self, path, resum, opinion, score):

        resum_schema = Resum(
            id=str(uuid.uuid4()),
            job_id=self.job.get('id'),
            content=resum,
            file=str(path),
            opinion=opinion,
        )

        file_schema = File(
            id=str(uuid.uuid4()),
            job_id=self.job.get('id'),
        )

        analisys_schema = extract_data_analysis(
            resum, resum_schema.job_id, resum_schema.id, score
        )

        self.database.resums.insert(resum_schema.model_dump())
        self.database.analysis.insert(analisys_schema.model_dump())
        self.database.files.insert(file_schema.model_dump())

    def run(self):

        cv_paths = get_pdf_paths(dir=r'utils\curriculos')

        for path in cv_paths:
            content = read_pdf(path)
            resum = self.ai.resum_cv(content)
            opinion = self.ai.generate_opnion(content, self.job)
            score = self.ai.generate_score(content, self.job)
            self.generate_analysis_from_resumes(path, resum, opinion, score)
