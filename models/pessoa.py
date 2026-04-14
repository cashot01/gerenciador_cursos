
class Pessoa:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    @property
    def email(self) -> str:
        return self.email
    
    @email.setter
    def email(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise ValueError("Email invalido, ex: nome@dominio.com")
        self.email = valor.lower()

    def __str__(self):
        return f"{self.nome} <{self.email}>"
        