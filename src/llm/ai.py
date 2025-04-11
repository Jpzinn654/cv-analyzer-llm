from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import re

load_dotenv()

class GroqClient:
    
    def __init__(self, model_id='llama-3.3-70b-versatile'): # For local use llama 3.2 for Groq API use llama-3.3-70b-versatile
        self.model_id = model_id
        # Escolha uma das opções abaixo:
        # self.client = ChatOllama(model=self.model_id, base_url='http://localhost:11434')
        # Ou para usar Groq:
        self.client = ChatGroq(model_name=self.model_id)

    def generate_Response(self, prompt):
        response = self.client.invoke(prompt)
        return response.content # Devolvendo o conteudo da resposta da llm
    
    def resum_cv(self, cv):
        prompt = f"""
        Solicitação de Resumo de Currículo em markdown

        Currículo do candidato para resumir:
        {cv}

        Por favor, gere um resumo do currículo fornecido, formatado em markdown, seguindo rigorosamente o modelo abaixo.
        Não adicione seção extras, tabelas ou qualquer outro tipo de formatação diferente da específicada,
        Preencha cada seção com as informações relevantes, garantindo que o resumo seja preciso e focado

        **FORMATO DE OUTPUT ESPERADO:**

        ```markdown
        ## Nome Completo
        nome_completo aqui

        ## Experiências
        experiências aqui

        ## Habilidades
        habilidades aqui

        ## Educação
        educação aqui
        
        ## Idiomas
        idiomas aqui
        """

        result_raw = self.generate_Response(prompt)
        
        try:
            result = result_raw.split('```markdown')[1]
        except:
            result = result_raw

        return result
    
    def generate_score(self, cv, job, max_attempt=10):
        prompt = f""""
        Objetivo: Avaliar um currículo com base em uma vaga especifica e calcular a pontuação final. A notá máxima é 10.0.

        Instruções:

        1. Experiência (Peso: 30%)**: Avalie a relevância da experiência em relação à vaga.
        2. Habilidade Técnica (Peso: 25%): ** Verifique o alinhamento das habilidades técnicas com os requisitos da vaga.
        3. Educação (Peso: 10%)**: Avalie a relevância da formação acadêmica para à vaga.
        4. Idiomas: (Peso: 10%)**: Avalie os idiomas e proêfiencia em ralção a vaga lembrando que se tiver Inglês é um baita diferencial.
        5. Pontos Fortes: (Peso: 15%)**: Avalie a relevância dos pontos fortes em realção a vaga.
        6. Pontos Fracos: (Desonto de até 10%)**: Avalie a gravidade dos pontos fracos em relação à vaga.

        Currículo do candidato:

        {cv}

        Vaga que o candidato está se candidatando

        {job}

        Output Esperado:
        ```
        Pontuaçao Final: x.x
        ```

        Atenção: Seja rigoroso ao tribuir as notas. A **nota máxima é 10.0**, e o output deve conter apenas  ** Pontuação Final: x.x **.
        """

        for attempt in range(max_attempt):
            result_raw = self.generate_Response(prompt)
            score = self.extract_score_from_result(result_raw)

            if score is not None:
                return score # Caso não encontre o score ele volta o loop até gerar o score
    
    def extract_score_from_result(self, result_raw):
        pattern = r"(?i)Pontuação Final[:\s]*([\d,.]+(?:/\d{1,2})?)"

        match = re.search(pattern, result_raw)
        if match:
            score_str = match.group(1)
            if '/' in score_str:
                score_str = score_str.split('/')[0]

            return float(score_str.replace(',', '.'))
        
        return None
    
    def generate_opnion(self, cv, job):
        prompt = f"""

            Por favor, analise o currículo fornecido em relação à descrição da vaga aplicada e crie uma opinião ultra crítica e detalhada. A sua análise deve incluir os seguintes pontos:
            Você deve pensar como o recrutador chefe que está analisando e gerando uma opnião descritiva sobre o curriculo do canditato que se candidatou para a vaga
            
            Formate a resposta de forma profissional, coloque titulos grandes nas sessões.

            1. **Pontos de Alinhamento**: Identifique e discuta os aspectos do currículo que estão diretamente alinhados com os requisitos da vaga. Inclua exemplos específicos de experiências, habilidades ou qualificações que correspondem ao que a vaga está procurando.

            2. **Pontos de Desalinhamento**: Destaque e discuta as áreas onde o candidato não atende aos requisitos da vaga. Isso pode incluir falta de experiência em áreas chave, ausência de habilidades técnicas específicas, ou qualificações que não correspondem às expectativas da vaga.

            3. **Pontos de Atenção**: Identifique e discuta características do currículo que merecem atenção especial. Isso pode incluir aspectos como a frequência com que o candidato troca de emprego, lacunas no histórico de trabalho, ou características pessoais que podem influenciar o desempenho no cargo, tanto de maneira positiva quanto negativa.

            Sua análise deve ser objetiva, baseada em evidências apresentadas no currículo e na descrição da vaga. Seja detalhado e forneça uma avaliação honesta dos pontos fortes e fracos do candidato em relação à vaga.

            **Currículo Original:**
            {cv}

            **Descrição da Vaga:**
            {job}
            
            Você deve devolver essa analise critica formatada como se fosse um relatorio analitico do curriculum com a vaga, deve estar formatado com titulos grandes em destaques
        
        """

        return self.generate_Response(prompt)
    