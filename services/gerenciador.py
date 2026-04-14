
from typing import List, Optional
from models.curso import Curso
from models.aluno import Aluno

class GerenciadorCursos:
    _cursos: list[Curso] = []

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