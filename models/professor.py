
from pessoa import Pessoa

class Professor(Pessoa):

    def __init__(self, nome: str, email: str, especialidade: str):
        super().__init__(nome, email)
        self.especialidade = especialidade
        self.disciplinas: list[str] = []

    def atribuir_disciplina(self, disciplina: str):
        if disciplina not in self.disciplinas:
            self.disciplinas.append(disciplina)

    def __str__(self):
        return f"Prof. {self.nome} | Esp: {self.especialidade}"