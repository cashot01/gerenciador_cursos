from pessoa import Pessoa

class Aluno(Pessoa):
    _contador_matricula = 1000

    def __init__(self, nome: str, email: str):
        super().__init__(nome, email)
        self.matricula = f"M{Aluno._contador_matricula}"
        Aluno._contador_matricula += 1
        self.notas : list[float] = []

    def adicionar_nota(self, nota: float):
        if not 0 <= nota <= 10:
            raise ValueError("Nota deve estar entre 0 e 10")
        self.notas.append(nota)

    def caucular_media(self) -> float:
        return sum(self.notas) / len(self.notas) if self.notas else 0.0
    
    def __str__(self):
        return f"[{self.matricula}] {super().__str__()} | Media: {self.caucular_media():.1f}"
    
    