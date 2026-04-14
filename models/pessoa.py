
class Pessoa:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise ValueError("Email inválido. Ex: nome@dominio.com")
        self._email = valor.lower()

    def to_dict(self) -> dict:
        return {"nome": self.nome, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["nome"], data["email"])

    def __str__(self):
        return f"{self.nome} <{self.email}>"
        