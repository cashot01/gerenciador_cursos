"""
Testes unitários para o GerenciadorCursos (services).
Foco: Persistência JSON, CRUD de professores/alunos e exportação CSV.
"""
import pytest
import os
import json
from models.curso import Curso
from models.professor import Professor
from models.aluno import Aluno
from services.gerenciador import GerenciadorCursos


class TestGerenciadorCursos:
    """Classe de testes para GerenciadorCursos."""

    @pytest.fixture(autouse=True)
    def limpar_dados_antes_de_cada_teste(self):
        """🔧 Limpa os dados do gerenciador antes de cada teste."""
        GerenciadorCursos._cursos = []
        GerenciadorCursos._professores = []
        GerenciadorCursos._alunos = []
        yield
        # Limpa após o teste também
        GerenciadorCursos._cursos = []
        GerenciadorCursos._professores = []
        GerenciadorCursos._alunos = []

    def test_adicionar_professor(self):
        """✅ Deve adicionar professor à lista."""
        prof = Professor("Ana", "ana@email.com", "Python")
        GerenciadorCursos.adicionar_professor(prof)
        assert len(GerenciadorCursos.listar_professores()) == 1

    def test_adicionar_professor_nao_repete_por_email(self):
        """✅ Não deve adicionar professor com email duplicado."""
        prof1 = Professor("Ana", "ana@email.com", "Python")
        prof2 = Professor("Ana Silva", "ana@email.com", "Java")  # Mesmo email
        GerenciadorCursos.adicionar_professor(prof1)
        GerenciadorCursos.adicionar_professor(prof2)
        assert len(GerenciadorCursos.listar_professores()) == 1

    def test_adicionar_aluno(self):
        """✅ Deve adicionar aluno à lista."""
        aluno = Aluno("Carlos", "carlos@email.com")
        GerenciadorCursos.adicionar_aluno(aluno)
        assert len(GerenciadorCursos.listar_alunos()) == 1

    def test_adicionar_aluno_nao_repete_por_matricula(self):
        """✅ Não deve adicionar aluno com matrícula duplicada."""
        aluno1 = Aluno("Carlos", "carlos@email.com")
        aluno2 = Aluno("Carlos Jr", "carlos2@email.com")
        aluno2.matricula = aluno1.matricula  # Força mesma matrícula
        GerenciadorCursos.adicionar_aluno(aluno1)
        GerenciadorCursos.adicionar_aluno(aluno2)
        assert len(GerenciadorCursos.listar_alunos()) == 1

    def test_adicionar_curso(self):
        """✅ Deve adicionar curso à lista."""
        prof = Professor("Ana", "ana@email.com", "Python")
        curso = Curso("PY101", "Python", 40, prof)
        GerenciadorCursos.adicionar_curso(curso)
        assert len(GerenciadorCursos._cursos) == 1

    def test_salvar_e_carregar_dados_json(self, tmp_path):
        """✅ Deve salvar e carregar dados do JSON corretamente."""
        # Criar dados
        prof = Professor("Ana", "ana@email.com", "Python")
        aluno = Aluno("Carlos", "carlos@email.com")
        curso = Curso("PY101", "Python", 40, prof)
        curso.matricular(aluno)
        aluno.adicionar_nota(8.5)

        GerenciadorCursos.adicionar_professor(prof)
        GerenciadorCursos.adicionar_aluno(aluno)
        GerenciadorCursos.adicionar_curso(curso)

        # Salvar em arquivo temporário
        arquivo_teste = tmp_path / "teste.json"
        GerenciadorCursos.salvar_dados(str(arquivo_teste))

        # Limpar dados
        GerenciadorCursos._cursos = []
        GerenciadorCursos._professores = []
        GerenciadorCursos._alunos = []

        # Carregar do arquivo
        GerenciadorCursos.carregar_dados(str(arquivo_teste))

        # Verificar se os dados foram restaurados
        assert len(GerenciadorCursos.listar_professores()) == 1
        assert len(GerenciadorCursos.listar_alunos()) == 1
        assert len(GerenciadorCursos._cursos) == 1
        assert GerenciadorCursos.listar_alunos()[0].notas == [8.5]  # ✅ Notas persistiram!

    def test_exportar_csv_cria_arquivo(self, tmp_path):
        """✅ Deve criar arquivo CSV com dados dos cursos."""
        prof = Professor("Ana", "ana@email.com", "Python")
        aluno = Aluno("Carlos", "carlos@email.com")
        curso = Curso("PY101", "Python", 40, prof)
        curso.matricular(aluno)
        aluno.adicionar_nota(8.5)

        GerenciadorCursos.adicionar_professor(prof)
        GerenciadorCursos.adicionar_aluno(aluno)
        GerenciadorCursos.adicionar_curso(curso)

        arquivo_teste = tmp_path / "teste.csv"
        caminho = GerenciadorCursos.exportar_relatorio_csv(str(arquivo_teste))

        assert os.path.exists(caminho)
        with open(caminho, "r", encoding="utf-8-sig") as f:
            conteudo = f.read()
            assert "PY101" in conteudo
            assert "Carlos" in conteudo
            assert "8.5" in conteudo

    def test_buscar_aluno_por_matricula(self):
        """✅ Deve encontrar aluno pela matrícula."""
        aluno = Aluno("Maria", "maria@email.com")
        GerenciadorCursos.adicionar_aluno(aluno)
        encontrado = GerenciadorCursos.buscar_aluno_por_matricula(aluno.matricula)
        assert encontrado == aluno

    def test_buscar_aluno_nao_encontrado_retorna_none(self):
        """✅ Deve retornar None se aluno não existir."""
        resultado = GerenciadorCursos.buscar_aluno_por_matricula("M9999")
        assert resultado is None

    def test_editar_aluno_atualiza_dados(self):
        """✅ Deve atualizar nome e email do aluno."""
        aluno = Aluno("Carlos", "carlos@email.com")
        GerenciadorCursos.adicionar_aluno(aluno)
        GerenciadorCursos.editar_aluno(aluno.matricula, "Carlos Jr", "carlos.jr@email.com")
        assert aluno.nome == "Carlos Jr"
        assert aluno.email == "carlos.jr@email.com"

    def test_excluir_aluno_remove_da_lista(self):
        """✅ Deve remover aluno da lista."""
        aluno = Aluno("Pedro", "pedro@email.com")
        GerenciadorCursos.adicionar_aluno(aluno)
        GerenciadorCursos.excluir_aluno(aluno.matricula)
        assert len(GerenciadorCursos.listar_alunos()) == 0