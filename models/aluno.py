from models.pessoa import Pessoa

class Aluno(Pessoa):
    _contador_matricula = 1000

    def __init__(self, nome: str, email: str, matricula: str = None):
        super().__init__(nome, email)
        if matricula:
            self.matricula = matricula
        else:
            self.matricula = f"M{Aluno._contador_matricula}"
            Aluno._contador_matricula += 1
        self.notas: list[float] = []

    def adicionar_nota(self, nota: float):
        if not 0 <= nota <= 10:
            raise ValueError("Nota deve estar entre 0 e 10.")
        self.notas.append(nota)

    def calcular_media(self) -> float:
        return sum(self.notas) / len(self.notas) if self.notas else 0.0

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"matricula": self.matricula, "notas": self.notas})
        return d

    @classmethod
    def from_dict(cls, data: dict):
        # Recria sem incrementar o contador automaticamente
        return cls(data["nome"], data["email"], matricula=data["matricula"])

    def __str__(self):
        return f"[{self.matricula}] {super().__str__()} | Média: {self.calcular_media():.1f}"
    
    