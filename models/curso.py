
from aluno import Aluno
from professor import Professor

class Curso:
    def __init__(self, codigo: str, nome: str, carga_horaria: int, professor: Professor):
        self.codigo = codigo.upper()
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.professor = professor
        self.alunos: list[Aluno] = []

    def matricular(self, aluno: Aluno):
        if aluno in self.alunos:
            raise ValueError("Aluno ja matriculado nesse curso")
        self.alunos.append(aluno)

    def desmatricular(self, aluno: Aluno):
        if aluno in self.alunos:
            raise ValueError("Aluno não encontrado nesse curso")
        self.alunos.remove(aluno)

    def listar_alunos(self) -> list[Aluno]:
        return self.alunos.copy()
    
    def __str__(self):
        return f"{self.codigo} - {self.nome} | {len(self.alunos)} alunos | Prof: {self.professor.nome}"