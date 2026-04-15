
from models.pessoa import Pessoa

class Professor(Pessoa):
    def __init__(self, nome: str, email: str, especialidade: str):
        super().__init__(nome, email)
        self.especialidade = especialidade
        self.disciplinas: list[str] = []

    def atribuir_disciplina(self, disciplina: str):
        if disciplina not in self.disciplinas:
            self.disciplinas.append(disciplina)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"especialidade": self.especialidade, "disciplinas": self.disciplinas})
        return d

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(dados["nome"], dados["email"], dados["especialidade"])

    def __str__(self):
        return f"Prof. {self.nome} | Esp: {self.especialidade}"