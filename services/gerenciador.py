import json
import os
import csv
from typing import List, Optional
from models.curso import Curso
from models.aluno import Aluno
from models.professor import Professor

class GerenciadorCursos:
    _cursos: List[Curso] = []
    _professores: List[Professor] = []
    _alunos: List[Aluno] = []
    ARQUIVO_PADRAO = "dados_cursos.json"
    ARQUIVO_CSV = "relatorio_cursos.csv"

    # ==================== CURSOS ====================
    @classmethod
    def adicionar_curso(cls, curso: Curso):
        cls._cursos.append(curso)

    @classmethod
    def buscar_curso_por_codigo(cls, codigo: str) -> Optional[Curso]:
        for curso in cls._cursos:
            if curso.codigo == codigo.upper():
                return curso
        return None

    # ==================== PROFESSORES ====================
    @classmethod
    def adicionar_professor(cls, professor: Professor):
        if not any(p.email == professor.email for p in cls._professores):
            cls._professores.append(professor)

    @classmethod
    def listar_professores(cls) -> List[Professor]:
        return cls._professores.copy()

    @classmethod
    def editar_professor(cls, email_antigo: str, novo_professor: Professor) -> bool:
        for i, prof in enumerate(cls._professores):
            if prof.email == email_antigo:
                cls._professores[i] = novo_professor
                for curso in cls._cursos:
                    if curso.professor.email == email_antigo:
                        curso.professor = novo_professor
                return True
        return False

    @classmethod
    def excluir_professor(cls, email: str) -> bool:
        for i, prof in enumerate(cls._professores):
            if prof.email == email:
                cls._professores.pop(i)
                return True
        return False

    # ==================== ALUNOS ====================
    @classmethod
    def adicionar_aluno(cls, aluno: Aluno):
        if not any(a.matricula == aluno.matricula for a in cls._alunos):
            cls._alunos.append(aluno)

    @classmethod
    def listar_alunos(cls) -> List[Aluno]:
        return cls._alunos.copy()  # ⚠️ Retorna cópia, mas referências dos objetos são as mesmas

    @classmethod
    def buscar_aluno_por_matricula(cls, matricula: str) -> Optional[Aluno]:
        for aluno in cls._alunos:
            if aluno.matricula == matricula:
                return aluno
        return None

    @classmethod
    def editar_aluno(cls, matricula: str, novo_nome: str, novo_email: str) -> bool:
        for aluno in cls._alunos:
            if aluno.matricula == matricula:
                aluno.nome = novo_nome
                aluno.email = novo_email
                return True
        return False

    @classmethod
    def excluir_aluno(cls, matricula: str) -> bool:
        for i, aluno in enumerate(cls._alunos):
            if aluno.matricula == matricula:
                for curso in cls._cursos:
                    if aluno in curso.alunos:
                        curso.desmatricular(aluno)
                cls._alunos.pop(i)
                return True
        return False

    # ==================== RELATÓRIOS ====================
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

    # ==================== PERSISTÊNCIA JSON ====================
    @classmethod
    def salvar_dados(cls, caminho: str = None) -> str:
        path = caminho or cls.ARQUIVO_PADRAO
        
        # ✅ Coletar TODOS os alunos (incluindo os que estão só nos cursos)
        todos_alunos = {a.matricula: a for a in cls._alunos}
        for curso in cls._cursos:
            for aluno in curso.alunos:
                todos_alunos[aluno.matricula] = aluno
        
        dados = {
            "cursos": [curso.to_dict() for curso in cls._cursos],
            "professores": [prof.to_dict() for prof in cls._professores],
            "alunos": [aluno.to_dict() for aluno in todos_alunos.values()]  # ✅ Salva todos os alunos com notas
        }
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        # Debug: mostrar o que foi salvo
        print(f"\n🔍 DEBUG: Salvando {len(todos_alunos)} alunos no JSON")
        for matricula, aluno in todos_alunos.items():
            print(f"   - {matricula}: {aluno.nome} | Notas: {aluno.notas}")
        
        return path

    @classmethod
    def carregar_dados(cls, caminho: str = None) -> bool:
        path = caminho or cls.ARQUIVO_PADRAO
        if not os.path.exists(path):
            return False
        
        with open(path, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        # Carregar professores
        cls._professores = [Professor.from_dict(p) for p in dados.get("professores", [])]
        
        # Carregar alunos (com notas)
        cls._alunos = [Aluno.from_dict(a) for a in dados.get("alunos", [])]
        
        # Carregar cursos
        cls._cursos = [Curso.from_dict(c) for c in dados.get("cursos", [])]
        
        # Debug: mostrar o que foi carregado
        print(f"\n🔍 DEBUG: Carregando {len(cls._alunos)} alunos do JSON")
        for aluno in cls._alunos:
            print(f"   - {aluno.matricula}: {aluno.nome} | Notas: {aluno.notas}")
        
        # Sincronizar contador
        cls._sincronizar_contador_matriculas()
        
        return True

    @classmethod
    def _sincronizar_contador_matriculas(cls):
        from models.aluno import Aluno
        maior_matricula = 1000
        for aluno in cls._alunos:
            try:
                num = int(aluno.matricula.replace("M", ""))
                if num >= maior_matricula:
                    maior_matricula = num
            except (ValueError, AttributeError):
                pass
        Aluno._contador_matricula = maior_matricula + 1

    # ==================== EXPORTAÇÃO CSV ====================
    @classmethod
    def exportar_relatorio_csv(cls, caminho: str = None) -> str:
        path = caminho or cls.ARQUIVO_CSV
        
        if not cls._cursos:
            raise ValueError("Nenhum curso cadastrado para exportar.")
        
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            
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