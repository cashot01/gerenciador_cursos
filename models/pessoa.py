
class Pessoa:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        # ✅ Remove espaços em branco antes de validar
        valor_limpo = valor.strip()
        
        if "@" not in valor_limpo or "." not in valor_limpo:
            raise ValueError("Email inválido. Ex: nome@dominio.com")
        self._email = valor_limpo.lower()  # ✅ Usa o valor limpo

    def to_dict(self) -> dict:
        return {"nome": self.nome, "email": self.email}

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(dados["nome"], dados["email"])

    def __str__(self):
        return f"{self.nome} <{self.email}>"
        