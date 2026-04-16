"""
Testes unitários para a classe Professor.
Foco: Especialidade e disciplinas.
"""
import pytest
from models.professor import Professor


class TestProfessor:
    """Classe de testes para Professor."""

    def test_criar_professor_com_especialidade(self):
        """✅ Deve criar professor com especialidade."""
        prof = Professor("Ana Silva", "ana@email.com", "Python")
        assert prof.especialidade == "Python"

    def test_atribuir_disciplina_adiciona_a_lista(self):
        """✅ Deve adicionar disciplina à lista."""
        prof = Professor("Pedro", "pedro@email.com", "Matemática")
        prof.atribuir_disciplina("Álgebra")
        assert "Álgebra" in prof.disciplinas

    def test_atribuir_disciplina_nao_repete(self):
        """✅ Não deve adicionar disciplina duplicada."""
        prof = Professor("Maria", "maria@email.com", "Física")
        prof.atribuir_disciplina("Mecânica")
        prof.atribuir_disciplina("Mecânica")  # Tenta adicionar de novo
        assert prof.disciplinas.count("Mecânica") == 1

    def test_to_dict_inclui_especialidade_e_disciplinas(self):
        """✅ to_dict deve incluir todos os campos."""
        prof = Professor("João", "joao@email.com", "Química")
        prof.atribuir_disciplina("Orgânica")
        d = prof.to_dict()
        assert d["especialidade"] == "Química"
        assert d["disciplinas"] == ["Orgânica"]

    def test_from_dict_cria_professor_completo(self):
        """✅ from_dict deve recriar professor com disciplinas."""
        dados = {
            "nome": "Carla",
            "email": "carla@email.com",
            "especialidade": "Biologia",
            "disciplinas": ["Genética", "Ecologia"]
        }
        prof = Professor.from_dict(dados)
        assert prof.especialidade == "Biologia"
        assert len(prof.disciplinas) == 2

    def test_to_dict_inclui_disciplinas_vazias(self):
        """✅ to_dict deve incluir disciplinas mesmo se vazia."""
        prof = Professor("Teste", "teste@email.com", "Esp")
        d = prof.to_dict()
        assert "disciplinas" in d
        assert d["disciplinas"] == []

    def test_from_dict_com_disciplinas_vazias(self):
        """✅ from_dict deve funcionar com lista vazia de disciplinas."""
        dados = {
            "nome": "Teste",
            "email": "teste@email.com", 
            "especialidade": "Esp",
            "disciplinas": []
        }
        prof = Professor.from_dict(dados)
        assert prof.disciplinas == []