
class Pessoa:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email  # ✅ Aciona o setter (validação)

    @property
    def email(self) -> str:
        return self._email  # ✅ Retorna o atributo interno

    @email.setter
    def email(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise ValueError("Email inválido. Ex: nome@dominio.com")
        self._email = valor.lower()  # ✅ Atribui ao atributo interno (NÃO à propriedade)

    def __str__(self):
        return f"{self.nome} <{self.email}>"
        