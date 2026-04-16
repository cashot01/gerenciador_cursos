"""
Testes unitários para a classe Aluno.
Foco: Matrícula única, notas, média e persistência.
"""
import pytest
from models.aluno import Aluno


class TestAluno:
    """Classe de testes para Aluno."""

    def test_criar_aluno_gera_matricula_automatica(self):
        """✅ Deve gerar matrícula automática no formato M####."""
        aluno = Aluno("Carlos", "carlos@email.com")
        assert aluno.matricula.startswith("M")
        assert len(aluno.matricula) == 5  # M + 4 dígitos

    def test_matriculas_sao_sequenciais(self):
        """✅ Matrículas devem ser incrementadas sequencialmente."""
        aluno1 = Aluno("Ana", "ana@email.com")
        aluno2 = Aluno("Bruno", "bruno@email.com")
        num1 = int(aluno1.matricula.replace("M", ""))
        num2 = int(aluno2.matricula.replace("M", ""))
        assert num2 == num1 + 1

    def test_adicionar_nota_valida(self):
        """✅ Deve adicionar nota entre 0 e 10."""
        aluno = Aluno("Pedro", "pedro@email.com")
        aluno.adicionar_nota(8.5)
        assert 8.5 in aluno.notas
        assert len(aluno.notas) == 1

    def test_adicionar_nota_invalida_menor_que_zero(self):
        """✅ Deve recusar nota negativa."""
        aluno = Aluno("Maria", "maria@email.com")
        with pytest.raises(ValueError, match="Nota deve estar entre 0 e 10"):
            aluno.adicionar_nota(-1.0)

    def test_adicionar_nota_invalida_maior_que_dez(self):
        """✅ Deve recusar nota acima de 10."""
        aluno = Aluno("João", "joao@email.com")
        with pytest.raises(ValueError, match="Nota deve estar entre 0 e 10"):
            aluno.adicionar_nota(11.0)

    def test_calcular_media_com_notas(self):
        """✅ Média deve ser calculada corretamente."""
        aluno = Aluno("Lucas", "lucas@email.com")
        aluno.adicionar_nota(8.0)
        aluno.adicionar_nota(9.0)
        aluno.adicionar_nota(7.0)
        assert aluno.calcular_media() == 8.0

    def test_calcular_media_sem_notas_retorna_zero(self):
        """✅ Média deve ser 0 se não houver notas."""
        aluno = Aluno("Ana", "ana@email.com")
        assert aluno.calcular_media() == 0.0

    def test_to_dict_inclui_notas_e_matricula(self):
        """✅ to_dict deve incluir todas as propriedades."""
        aluno = Aluno("Carlos", "carlos@email.com")
        aluno.adicionar_nota(8.5)
        d = aluno.to_dict()
        assert d["matricula"] == aluno.matricula
        assert d["notas"] == [8.5]
        assert d["nome"] == "Carlos"

    def test_from_dict_restaura_notas(self):
        """✅ from_dict deve restaurar as notas salvas."""
        dados = {
            "nome": "Fernanda",
            "email": "fernanda@email.com",
            "matricula": "M1005",
            "notas": [7.5, 8.0, 9.0]
        }
        aluno = Aluno.from_dict(dados)
        assert aluno.notas == [7.5, 8.0, 9.0]
        
        # ✅ Use pytest.approx para comparação de floats
        assert aluno.calcular_media() == pytest.approx(8.166666666666666)
        
        # ✅ Ou compare com a fórmula exata:
        # assert aluno.calcular_media() == (7.5 + 8.0 + 9.0) / 3