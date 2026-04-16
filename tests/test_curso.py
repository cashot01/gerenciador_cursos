"""
Testes unitários para a classe Curso.
Foco: Matrícula, desmatrícula e vínculo com professor/aluno.
"""
import pytest
from models.curso import Curso
from models.professor import Professor
from models.aluno import Aluno


class TestCurso:
    """Classe de testes para Curso."""

    @pytest.fixture
    def professor(self):
        """🔧 Cria um professor para usar nos testes (reutilizável)."""
        return Professor("Ana", "ana@email.com", "Python")

    @pytest.fixture
    def curso(self, professor):
        """🔧 Cria um curso para usar nos testes."""
        return Curso("PY101", "Python Básico", 40, professor)

    @pytest.fixture
    def aluno(self):
        """🔧 Cria um aluno para usar nos testes."""
        return Aluno("Carlos", "carlos@email.com")

    def test_criar_curso_com_professor(self, curso, professor):
        """✅ Curso deve ser criado com professor vinculado."""
        assert curso.professor == professor
        assert curso.codigo == "PY101"
        assert curso.carga_horaria == 40

    def test_codigo_e_normalizado_para_maiusculo(self, professor):
        """✅ Código do curso deve ser convertido para maiúsculas."""
        curso = Curso("py101", "Python", 40, professor)
        assert curso.codigo == "PY101"

    def test_matricular_aluno_adiciona_a_lista(self, curso, aluno):
        """✅ Matrícula deve adicionar aluno à lista."""
        curso.matricular(aluno)
        assert aluno in curso.alunos
        assert len(curso.alunos) == 1

    def test_matricular_aluno_repetido_levanta_erro(self, curso, aluno):
        """✅ Não deve permitir matrícula duplicada."""
        curso.matricular(aluno)
        with pytest.raises(ValueError, match="já está matriculado"):
            curso.matricular(aluno)

    def test_desmatricular_remove_aluno(self, curso, aluno):
        """✅ Desmatrícula deve remover aluno da lista."""
        curso.matricular(aluno)
        curso.desmatricular(aluno)
        assert aluno not in curso.alunos
        assert len(curso.alunos) == 0

    def test_desmatricular_aluno_nao_matriculado_levanta_erro(self, curso, aluno):
        """✅ Deve erro ao desmatricular aluno não matriculado."""
        with pytest.raises(ValueError, match="não encontrado"):
            curso.desmatricular(aluno)

    def test_to_dict_serializa_curso_completo(self, curso, aluno):
        """✅ to_dict deve serializar curso com professor e alunos."""
        curso.matricular(aluno)
        d = curso.to_dict()
        assert d["codigo"] == "PY101"
        assert d["professor"]["nome"] == "Ana"
        assert len(d["alunos"]) == 1

    def test_from_dict_restaura_curso_com_alunos(self, professor):
        """✅ from_dict deve restaurar curso com alunos e notas."""
        dados = {
            "codigo": "JS201",
            "nome": "JavaScript",
            "carga_horaria": 60,
            "professor": professor.to_dict(),
            "alunos": [
                {
                    "nome": "Pedro",
                    "email": "pedro@email.com",
                    "matricula": "M1000",
                    "notas": [8.0, 9.0]
                }
            ]
        }
        curso = Curso.from_dict(dados)
        assert curso.codigo == "JS201"
        assert len(curso.alunos) == 1
        assert curso.alunos[0].notas == [8.0, 9.0]