"""
Testes unitários para a classe Pessoa.
Foco: Validação de email e métodos básicos.
"""
import pytest
from models.pessoa import Pessoa


class TestPessoa:
    """Classe de testes para Pessoa (agrupa todos os testes relacionados)."""

    def test_criar_pessoa_com_email_valido(self):
        """✅ Deve criar pessoa com email válido."""
        pessoa = Pessoa("João Silva", "joao@email.com")
        assert pessoa.nome == "João Silva"
        assert pessoa.email == "joao@email.com"

    def test_email_e_normalizado_para_minusculo(self):
        """✅ Email deve ser convertido para minúsculas."""
        pessoa = Pessoa("Maria", "MARIA@EMAIL.COM")
        assert pessoa.email == "maria@email.com"

    def test_email_invalido_sem_arroba(self):
        """✅ Deve levantar erro se email não tiver @."""
        with pytest.raises(ValueError, match="Email inválido"):
            Pessoa("Pedro", "pedroemail.com")

    def test_email_invalido_sem_ponto(self):
        """✅ Deve levantar erro se email não tiver ."""
        with pytest.raises(ValueError, match="Email inválido"):
            Pessoa("Ana", "ana@emailcom")

    def test_str_retorna_formato_esperado(self):
        """✅ __str__ deve retornar formato 'Nome <email>'."""
        pessoa = Pessoa("Carlos", "carlos@teste.com")
        assert str(pessoa) == "Carlos <carlos@teste.com>"

    def test_to_dict_retorna_dicionario_correto(self):
        """✅ to_dict deve retornar dict com nome e email."""
        pessoa = Pessoa("Lucas", "lucas@email.com")
        d = pessoa.to_dict()
        assert d == {"nome": "Lucas", "email": "lucas@email.com"}

    def test_from_dict_cria_objeto_a_partir_de_dicionario(self):
        """✅ from_dict deve recriar objeto Pessoa."""
        dados = {"nome": "Fernanda", "email": "fernanda@email.com"}
        pessoa = Pessoa.from_dict(dados)
        assert pessoa.nome == "Fernanda"
        assert pessoa.email == "fernanda@email.com"