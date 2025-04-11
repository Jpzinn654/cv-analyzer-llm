import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from database import AnalyseDatabase
import uuid
from src.models.job import Job

database = AnalyseDatabase()

name = 'Vaga Jovem Aprendiz Desenvolvedor'

activies = 'Como Jovem Aprendiz na area de Desenvolvimento na Unifisa, voce atuara no departamento de Tecnologia, prestando suporte as atividades de desenvolvimento e manutencao. Sua paixao por programacao, capacidade de aprendizado rapido e habilidades basicas em desenvolvimento serao fundamentais para contribuir com nossos projetos e solucoes tecnologicas.'

prerequisities = 'Idade: de 18 a 22 anos; Nunca ter atuado anteriormente como Jovem Aprendiz; Ensino Medio Completo / Superior Cursando em cursos correlatos a area de tecnologia, como, Analise e Desenvolvimento de Sistemas (ADS), Ciencias da Computacao ou equivalente; Disposicao para aprender e aplicar novos conhecimentos de forma autonoma; Capacidade de adaptar-se rapidamente a mudancas e trabalhar em um ambiente dinamico; Excelente comunicacao verbal e escrita, capacidade de trabalhar bem em equipe; Comprometimento com prazos e qualidade do trabalho, mantendo uma conduta profissional etica.'

differentials = 'Habilidade com ferramentas de versionamento, como Git, e uso de plataformas como GitHub; Conhecimento solido em logica de programacao e experiencia com Python e suas principais bibliotecas. Valorizamos os profissionais que tenham agilidade de raciocinio, controle emocional, diligencia, disciplina, empatia, organizacao, proatividade, bom relacionamento interpessoal, boa comunicacao escrita e verbal, que saibam utilizar do raciocinio logico e visao estrategica para resolver as situacoes do dia a dia e gerar solucoes eficazes.'

job = Job(
    id=str(uuid.uuid4()),
    name=name,
    main_activies=activies,
    prerequisities=prerequisities,
    diferentials=differentials
)

database.jobs.insert(job.model_dump()) # Inseri um dicionário