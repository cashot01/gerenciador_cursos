import json
import os
import csv
from typing import List, Optional
from models.curso import Curso
from models.aluno import Aluno

class GerenciadorCursos:
    _cursos: List[Curso] = []
    ARQUIVO_PADRAO = "dados_cursos.json"
    ARQUIVO_CSV = "relatorio_cursos.csv"

    @classmethod
    def adicionar_curso(cls, curso: Curso):
        cls._cursos.append(curso)

    @classmethod
    def buscar_curso_por_codigo(cls, codigo: str) -> Optional[Curso]:
        for curso in cls._cursos:
            if curso.codigo == codigo.upper():
                return curso
        return None

    @staticmethod
    def buscar_aluno_por_matricula(alunos: List[Aluno], matricula: str) -> Optional[Aluno]:
        for aluno in alunos:
            if aluno.matricula == matricula:
                return aluno
        return None

    @classmethod
    def gerar_relatorio_turmas(cls) -> str:
        if not cls._cursos:
            return "📭 Nenhum curso cadastrado."
        
        relatorio = "📊 RELATÓRIO DE TURMAS\n" + "="*35 + "\n"
        for curso in cls._cursos:
            relatorio += f"• {curso}\n"
            relatorio += f"  Carga horária: {curso.carga_horaria}h\n"
            if curso.alunos:
                media_turma = sum(a.calcular_media() for a in curso.alunos) / len(curso.alunos)
                relatorio += f"  Média da turma: {media_turma:.1f}\n"
            else:
                relatorio += "  Sem alunos matriculados.\n"
            relatorio += "-"*35 + "\n"
        return relatorio

    @classmethod
    def salvar_dados(cls, caminho: str = None) -> str:
        path = caminho or cls.ARQUIVO_PADRAO
        dados = {"cursos": [curso.to_dict() for curso in cls._cursos]}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return path

    @classmethod
    def carregar_dados(cls, caminho: str = None) -> bool:
        path = caminho or cls.ARQUIVO_PADRAO
        if not os.path.exists(path):
            return False
        with open(path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        cls._cursos = [Curso.from_dict(c) for c in dados.get("cursos", [])]
        
        # 🔥 Sincronizar contador de matrículas após carregar
        cls._sincronizar_contador_matriculas()
        
        return True

    @classmethod
    def _sincronizar_contador_matriculas(cls):
        """
        Percorre todos os alunos em todos os cursos e atualiza o contador
        para garantir que a próxima matrícula seja única.
        """
        from models.aluno import Aluno
        
        maior_matricula = 1000  # Valor inicial padrão
        
        for curso in cls._cursos:
            for aluno in curso.alunos:
                try:
                    num = int(aluno.matricula.replace("M", ""))
                    if num >= maior_matricula:
                        maior_matricula = num
                except (ValueError, AttributeError):
                    pass
        
        # Define o contador como o maior valor encontrado + 1
        Aluno._contador_matricula = maior_matricula + 1

    @classmethod
    def exportar_relatorio_csv(cls, caminho: str = None) -> str:
        """
        Exporta relatório completo de cursos, alunos e notas para CSV.
        """
        path = caminho or cls.ARQUIVO_CSV
        
        if not cls._cursos:
            raise ValueError("Nenhum curso cadastrado para exportar.")
        
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            
            # Cabeçalho
            writer.writerow([
                "Código do Curso",
                "Nome do Curso",
                "Carga Horária",
                "Professor",
                "Especialidade do Professor",
                "Matrícula do Aluno",
                "Nome do Aluno",
                "Email do Aluno",
                "Notas (separadas por vírgula)",
                "Quantidade de Notas",
                "Média Final",
                "Situação"
            ])
            
            # Dados
            for curso in cls._cursos:
                if curso.alunos:
                    for aluno in curso.alunos:
                        media = aluno.calcular_media()
                        situacao = "Aprovado" if media >= 6.0 else "Reprovado" if aluno.notas else "Sem Notas"
                        
                        writer.writerow([
                            curso.codigo,
                            curso.nome,
                            f"{curso.carga_horaria}h",
                            curso.professor.nome,
                            curso.professor.especialidade,
                            aluno.matricula,
                            aluno.nome,
                            aluno.email,
                            ", ".join(str(n) for n in aluno.notas),
                            len(aluno.notas),
                            f"{media:.2f}" if aluno.notas else "0.00",
                            situacao
                        ])
                else:
                    writer.writerow([
                        curso.codigo,
                        curso.nome,
                        f"{curso.carga_horaria}h",
                        curso.professor.nome,
                        curso.professor.especialidade,
                        "—",
                        "—",
                        "—",
                        "—",
                        "0",
                        "0.00",
                        "Sem Alunos"
                    ])
        
        return path