import sys, os, re, uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import fitz
from src.models.analysis import Analysis

def read_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            # Esse operadorador sempre vai acrentar caso tiver mais de um pag ao final
            text += page.get_text()

    return text

def extract_data_analysis(resum_cv, job_id, resum_id, score) -> Analysis:
    secoes_dict = {
        "id": str(uuid.uuid4()),
        "job_id": job_id,
        "resum_id": resum_id,
        "name": "",
        "skills": [],
        "education": [],
        "language": [],
        "score": score
    }

    patterns = {
        "name": r"(?:## Nome Completo\s*|Nome Completo\s*\|\s*Valor\s*\|\s*\S*\s*\|\s*)(.*)",
        "skills": r"## Habilidades\s*([\s\S]*?)(?=##|$)",
        "education": r"## Educação\s*([\s\S]*?)(?=##|$)",
        "languages": r"## Idiomas\s*([\s\S]*?)(?=##|$)",
    }

    def clean_string(string: str) -> str:
        return re.sub(r"[\*\-]+", "", string).strip()

    # aplicando o padrão das regex dentro das nossas seções devolvendo meu dicionario da maneira correta
    for secao, pattern in patterns.items():
        match = re.search(pattern, resum_cv)
        if match:
            if secao == "name":
                secoes_dict[secao] = clean_string(match.group(1))
            else:
                secoes_dict[secao] = [clean_string(item) for item in match.group(1).split('\n') if item.strip()]

    # Validação para garantir que nenhuma seção obrigatória esteja vazia
    for key in ["name", "education", "skills"]:
        if not secoes_dict[key] or (isinstance(secoes_dict[key], list) and not any(secoes_dict[key])):
            raise ValueError(f"A seção '{key}' não pode ser vazia ou uma string vazia.")

    return Analysis(**secoes_dict)

def get_pdf_paths(dir):
    pdf_paths = []

    for filename in os.listdir(dir): # Sempre irá listar os curriculos dentro do diretorio
        if filename.endswith('.pdf'):
            file_path = os.path.join(dir, filename) 
            pdf_paths.append(file_path)

    return pdf_paths
