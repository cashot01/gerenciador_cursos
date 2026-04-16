"""
Testes unitários para as Views (interface Rich CLI).
Foco: Mock de inputs do usuário e validação da lógica de negócio.
"""
import pytest
from unittest.mock import patch, MagicMock, call
from rich.console import Console

from models.professor import Professor
from models.aluno import Aluno
from models.curso import Curso
from services.gerenciador import GerenciadorCursos

# Import das views
from views.professor_view import criar_professor, listar_professores, editar_professor, excluir_professor
from views.aluno_view import criar_aluno, listar_alunos, editar_aluno, excluir_aluno
from views.curso_view import criar_curso, listar_cursos, matricular_aluno, adicionar_nota


# ============================================================================
# 🎯 FIXTURES COMUNS (DEVEM FICAR NO TOPO DO ARQUIVO)
# ============================================================================

@pytest.fixture(autouse=True)
def limpar_gerenciador():
    """🔧 Limpa os dados do GerenciadorCursos antes de cada teste."""
    GerenciadorCursos._cursos = []
    GerenciadorCursos._professores = []
    GerenciadorCursos._alunos = []
    yield
    GerenciadorCursos._cursos = []
    GerenciadorCursos._professores = []
    GerenciadorCursos._alunos = []


@pytest.fixture
def console_professor_mock():
    """🔧 Mock do console para tests de professor_view."""
    with patch("views.professor_view.console") as mock:
        yield mock


@pytest.fixture
def console_aluno_mock():
    """🔧 Mock do console para tests de aluno_view."""
    with patch("views.aluno_view.console") as mock:
        yield mock


@pytest.fixture
def console_curso_mock():
    """🔧 Mock do console para tests de curso_view."""
    with patch("views.curso_view.console") as mock:
        yield mock


@pytest.fixture
def professor_valido():
    """🔧 Cria um professor válido para testes."""
    return Professor("Ana Silva", "ana@email.com", "Python")


@pytest.fixture
def aluno_valido():
    """🔧 Cria um aluno válido para testes."""
    return Aluno("Carlos Souza", "carlos@email.com")


@pytest.fixture
def curso_valido(professor_valido):
    """🔧 Cria um curso válido para testes (depende do fixture professor_valido)."""
    return Curso("PY101", "Python Básico", 40, professor_valido)


# ============================================================================
# TESTES: PROFESSOR_VIEW
# ============================================================================

class TestProfessorView:
    """Testes para as funções da view de Professor."""

    def test_criar_professor_sucesso(self):
        """✅ Deve criar professor quando inputs são válidos."""
        # Mock dos inputs do usuário
        with patch("views.professor_view.Prompt.ask") as mock_ask:
            mock_ask.side_effect = ["Ana Silva", "ana@email.com", "Python"]
            
            resultado = criar_professor()
            
            # Verificações
            assert resultado is not None
            assert resultado.nome == "Ana Silva"
            assert resultado.email == "ana@email.com"
            assert resultado.especialidade == "Python"
            
            # Verifica se Prompt.ask foi chamado 3 vezes (nome, email, especialidade)
            assert mock_ask.call_count == 3

    def test_criar_professor_email_invalido(self, console_professor_mock):
        """✅ Deve mostrar erro quando email é inválido."""
        with patch("views.professor_view.Prompt.ask") as mock_ask:
            mock_ask.side_effect = ["Pedro", "email-invalido", "Java"]
            
            resultado = criar_professor()
            
            # Deve retornar None por causa do erro
            assert resultado is None
            
            # Deve ter chamado console.print para mostrar erro
            console_professor_mock.print.assert_any_call(
                "  ❌ [red]Erro: Email inválido. Ex: nome@dominio.com[/red]"
            )

    def test_listar_professores_vazio(self, console_professor_mock):
        """✅ Deve mostrar mensagem quando não há professores."""
        # Garantir que a lista está vazia
        GerenciadorCursos._professores = []
        
        listar_professores()
        
        # Verifica se mostrou a mensagem de "nenhum professor"
        console_professor_mock.print.assert_any_call("  📭 [dim]Nenhum professor cadastrado.[/dim]")

    def test_listar_professores_com_dados(self, console_professor_mock, professor_valido):
        """✅ Deve mostrar tabela quando há professores cadastrados."""
        # Adicionar professor ao gerenciador
        GerenciadorCursos.adicionar_professor(professor_valido)
        
        with patch("views.professor_view.Table") as MockTable:
            mock_table = MagicMock()
            MockTable.return_value = mock_table
            
            listar_professores()
            
            # Verifica se Table foi criado com os parâmetros corretos
            MockTable.assert_called_once()
            
            # Verifica se add_row foi chamado para o professor
            mock_table.add_row.assert_called()

    def test_editar_professor_sucesso(self):
        """✅ Deve editar professor quando inputs são válidos."""
        # Criar e adicionar professor
        prof_original = Professor("Ana", "ana@email.com", "Python")
        GerenciadorCursos.adicionar_professor(prof_original)
        
        # Mock dos inputs: selecionar índice 0, depois novos valores
        with patch("views.professor_view.IntPrompt.ask") as mock_int, \
             patch("views.professor_view.Prompt.ask") as mock_prompt:
            
            mock_int.return_value = 1  # Seleciona primeiro professor
            mock_prompt.side_effect = ["Ana Silva", "ana.nova@email.com", "Python Avançado"]
            
            editar_professor()
            
            # Verifica se o professor foi atualizado
            prof_atualizado = GerenciadorCursos.listar_professores()[0]
            assert prof_atualizado.nome == "Ana Silva"
            assert prof_atualizado.email == "ana.nova@email.com"
            assert prof_atualizado.especialidade == "Python Avançado"

    def test_excluir_professor_com_confirmacao(self):
        """✅ Deve excluir professor quando confirmado."""
        prof = Professor("Pedro", "pedro@email.com", "Java")
        GerenciadorCursos.adicionar_professor(prof)
        
        with patch("views.professor_view.IntPrompt.ask") as mock_int, \
             patch("views.professor_view.Confirm.ask") as mock_confirm:
            
            mock_int.return_value = 1  # Seleciona primeiro professor
            mock_confirm.return_value = True  # Confirma exclusão
            
            excluir_professor()
            
            # Verifica se professor foi removido
            assert len(GerenciadorCursos.listar_professores()) == 0

    def test_excluir_professor_cancelado(self):
        """✅ Não deve excluir se usuário cancelar."""
        prof = Professor("Maria", "maria@email.com", "C#")
        GerenciadorCursos.adicionar_professor(prof)
        
        with patch("views.professor_view.IntPrompt.ask") as mock_int, \
             patch("views.professor_view.Confirm.ask") as mock_confirm:
            
            mock_int.return_value = 1
            mock_confirm.return_value = False  # Cancela exclusão
            
            excluir_professor()
            
            # Verifica se professor AINDA está na lista
            assert len(GerenciadorCursos.listar_professores()) == 1


# ============================================================================
# TESTES: ALUNO_VIEW
# ============================================================================

class TestAlunoView:
    """Testes para as funções da view de Aluno."""

    def test_criar_aluno_sucesso(self):
        """✅ Deve criar aluno com matrícula automática."""
        with patch("views.aluno_view.Prompt.ask") as mock_ask:
            mock_ask.side_effect = ["Carlos", "carlos@email.com"]
            
            resultado = criar_aluno()
            
            assert resultado is not None
            assert resultado.matricula.startswith("M")
            assert resultado.nome == "Carlos"

    def test_listar_alunos_com_media(self, console_aluno_mock, aluno_valido):
        """✅ Deve mostrar média ao listar alunos."""
        # Adicionar notas ao aluno
        aluno_valido.adicionar_nota(8.0)
        aluno_valido.adicionar_nota(9.0)
        GerenciadorCursos.adicionar_aluno(aluno_valido)
        
        with patch("views.aluno_view.Table") as MockTable:
            mock_table = MagicMock()
            MockTable.return_value = mock_table
            
            listar_alunos()
            
            # Verifica se a média foi incluída na tabela (8.5)
            # O add_row deve ter sido chamado com a média formatada
            mock_table.add_row.assert_called()
            
            # Pega os argumentos da chamada
            args, kwargs = mock_table.add_row.call_args
            # A última coluna deve conter a média "8.5"
            assert "8.5" in str(args)

    def test_editar_aluno_atualiza_email(self):
        """✅ Deve atualizar email do aluno com validação."""
        aluno = Aluno("João", "joao@email.com")
        GerenciadorCursos.adicionar_aluno(aluno)
        
        with patch("views.aluno_view.IntPrompt.ask") as mock_int, \
             patch("views.aluno_view.Prompt.ask") as mock_prompt:
            
            mock_int.return_value = 1
            mock_prompt.side_effect = ["João Silva", "joao.silva@email.com"]
            
            editar_aluno()
            
            # Verifica atualização
            assert aluno.email == "joao.silva@email.com"

    def test_excluir_aluno_com_matricula_ativa(self):
        """✅ Deve desmatricular automaticamente ao excluir aluno."""
        aluno = Aluno("Pedro", "pedro@email.com")
        prof = Professor("Ana", "ana@email.com", "Python")
        curso = Curso("PY101", "Python", 40, prof)
        
        # Matricular aluno no curso
        curso.matricular(aluno)
        
        GerenciadorCursos.adicionar_aluno(aluno)
        GerenciadorCursos.adicionar_curso(curso)
        
        with patch("views.aluno_view.IntPrompt.ask") as mock_int, \
             patch("views.aluno_view.Confirm.ask") as mock_confirm:
            
            mock_int.return_value = 1  # Seleciona aluno
            mock_confirm.return_value = True  # Confirma exclusão
            
            excluir_aluno()
            
            # Verifica se aluno foi removido da lista global
            assert len(GerenciadorCursos.listar_alunos()) == 0
            # Verifica se foi desmatriculado do curso
            assert aluno not in curso.alunos


# ============================================================================
# TESTES: CURSO_VIEW
# ============================================================================

class TestCursoView:
    """Testes para as funções da view de Curso."""

    def test_criar_curso_sucesso(self, professor_valido):
        """✅ Deve criar curso vinculado ao professor selecionado."""
        # Adicionar professor ao gerenciador
        GerenciadorCursos.adicionar_professor(professor_valido)
        
        with patch("views.curso_view.IntPrompt.ask") as mock_int, \
             patch("views.curso_view.Prompt.ask") as mock_prompt:
            
            mock_int.side_effect = [1, 40]  # Seleciona professor 1, carga 40h
            mock_prompt.side_effect = ["PY101", "Python Básico"]
            
            resultado = criar_curso()
            
            assert resultado is not None
            assert resultado.codigo == "PY101"
            assert resultado.professor == professor_valido

    def test_listar_cursos_vazio(self, console_curso_mock):  # ✅ Usa o mock correto
        """✅ Deve mostrar mensagem quando não há cursos."""
        GerenciadorCursos._cursos = []
        
        listar_cursos()
        
        # ✅ Agora o mock está no módulo correto
        console_curso_mock.print.assert_any_call("  📭 [dim]Nenhum curso cadastrado ainda.[/dim]")

    def test_matricular_aluno_sucesso(self, professor_valido, aluno_valido):
        """✅ Deve matricular aluno em curso existente."""
        # Criar curso e aluno
        curso = Curso("PY101", "Python", 40, professor_valido)
        GerenciadorCursos.adicionar_curso(curso)
        GerenciadorCursos.adicionar_aluno(aluno_valido)
        
        with patch("views.curso_view.IntPrompt.ask") as mock_int:
            mock_int.side_effect = [1, 1]  # Seleciona curso 1, aluno 1
            
            matricular_aluno()
            
            # Verifica matrícula
            assert aluno_valido in curso.alunos

    def test_adicionar_nota_sucesso(self, professor_valido, aluno_valido):
        """✅ Deve adicionar nota ao aluno matriculado."""
        # Setup: curso com aluno matriculado
        curso = Curso("PY101", "Python", 40, professor_valido)
        curso.matricular(aluno_valido)
        GerenciadorCursos.adicionar_curso(curso)
        
        with patch("views.curso_view.IntPrompt.ask") as mock_int, \
             patch("views.curso_view.FloatPrompt.ask") as mock_float:
            
            mock_int.side_effect = [1, 1]  # Curso 1, Aluno 1
            mock_float.return_value = 8.5  # Nota 8.5
            
            adicionar_nota()
            
            # Verifica se nota foi adicionada
            assert 8.5 in aluno_valido.notas
            assert aluno_valido.calcular_media() == 8.5

    def test_adicionar_nota_invalida(self, professor_valido, aluno_valido, console_curso_mock):  # ✅ Mock correto
        """✅ Deve recusar nota fora do intervalo 0-10."""
        curso = Curso("PY101", "Python", 40, professor_valido)
        curso.matricular(aluno_valido)
        GerenciadorCursos.adicionar_curso(curso)
        
        with patch("views.curso_view.IntPrompt.ask") as mock_int, \
            patch("views.curso_view.FloatPrompt.ask") as mock_float:
            
            mock_int.side_effect = [1, 1]
            mock_float.return_value = 15.0  # Nota inválida
            
            adicionar_nota()
            
            # ✅ Agora o mock captura a chamada correta
            console_curso_mock.print.assert_any_call(
                "  ❌ [red]Erro: Nota deve estar entre 0 e 10.[/red]"
            )


# ============================================================================
# TESTES AVANÇADOS: Mock de Console Rich
# ============================================================================

class TestRichConsoleIntegration:
    """Testes que validam integração com a biblioteca Rich."""

    def test_console_print_chamado_com_panel(self):
        """✅ Funções de view devem usar Panel para títulos."""
        with patch("views.professor_view.console") as mock_console, \
             patch("views.professor_view.Prompt.ask") as mock_ask:
            
            from rich.panel import Panel
            mock_ask.side_effect = ["Teste", "teste@email.com", "Esp"]
            
            criar_professor()
            
            # Verifica se Panel foi usado para o título
            # (Isso valida que a UI está usando os componentes Rich corretamente)
            calls = [str(call) for call in mock_console.print.call_args_list]
            # Pelo menos uma chamada deve conter "Panel" ou formatação Rich
            assert any("[bold]" in str(c) or "Panel" in str(c) for c in calls)

    def test_tabela_rich_tem_cabecalhos(self):
        """✅ Tabelas devem ter cabeçalhos formatados."""
        from views.aluno_view import listar_alunos
        
        aluno = Aluno("Teste", "teste@email.com")
        GerenciadorCursos.adicionar_aluno(aluno)
        
        with patch("views.aluno_view.Table") as MockTable:
            mock_table = MagicMock()
            MockTable.return_value = mock_table
            
            listar_alunos()
            
            # Verifica se add_column foi chamado para os cabeçalhos esperados
            columns_added = [call[0][0] for call in mock_table.add_column.call_args_list]
            assert "Matrícula" in columns_added
            assert "Nome" in columns_added
            assert "Média" in columns_added


# ============================================================================
# TESTES DE EDGE CASES (CORRIGIDO)
# ============================================================================

class TestViewEdgeCases:
    """Testes para casos extremos e validações de entrada."""

    def test_selecionar_indice_invalido_no_menu(self, console_professor_mock, professor_valido):
        """✅ Deve tratar índice fora do intervalo."""
        GerenciadorCursos.adicionar_professor(professor_valido)
        
        with patch("views.professor_view.IntPrompt.ask") as mock_int:
            mock_int.return_value = 999  # Índice inválido
            
            editar_professor()
            
            # Deve mostrar erro de "Professor inválido"
            console_professor_mock.print.assert_any_call("  ❌ [red]Professor inválido[/red]")

    def test_tentar_editar_lista_vazia(self, console_professor_mock):
        """✅ Deve tratar tentativa de editar lista vazia."""
        GerenciadorCursos._professores = []
        
        editar_professor()
        
        console_professor_mock.print.assert_any_call("  ⚠️ [yellow]Nenhum professor cadastrado.[/yellow]")

    def test_email_com_whitespace_e_normalizado(self):
        """✅ Email com espaços deve ser tratado corretamente."""
        with patch("views.professor_view.Prompt.ask") as mock_ask:
            # Simula usuário digitando email com espaços (comum em copy-paste)
            mock_ask.side_effect = ["Teste", "  teste@email.com  ", "Esp"]
            
            resultado = criar_professor()
            
            # O setter da classe Pessoa deve normalizar (após nossa correção)
            assert resultado.email == "teste@email.com"