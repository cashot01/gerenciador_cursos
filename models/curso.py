
from models.aluno import Aluno
from models.professor import Professor

class Curso:
    def __init__(self, codigo: str, nome: str, carga_horaria: int, professor: Professor):
        self.codigo = codigo.upper()
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.professor = professor
        self.alunos: list[Aluno] = []

    def matricular(self, aluno: Aluno):
        if aluno in self.alunos:
            raise ValueError("Aluno já está matriculado neste curso.")
        self.alunos.append(aluno)

    def desmatricular(self, aluno: Aluno):
        if aluno not in self.alunos:
            raise ValueError("Aluno não encontrado neste curso.")
        self.alunos.remove(aluno)

    def listar_alunos(self) -> list[Aluno]:
        return self.alunos.copy()

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "carga_horaria": self.carga_horaria,
            "professor": self.professor.to_dict(),
            "alunos": [a.to_dict() for a in self.alunos]
        }

    @classmethod
    def from_dict(cls, data: dict):
        prof = Professor.from_dict(data["professor"])
        curso = cls(data["codigo"], data["nome"], data["carga_horaria"], prof)
        curso.alunos = [Aluno.from_dict(a_data) for a_data in data.get("alunos", [])]
        return curso

    def __str__(self):
        return f"{self.codigo} - {self.nome} | {len(self.alunos)} alunos | Prof: {self.professor.nome}"