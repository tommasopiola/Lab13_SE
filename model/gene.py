from dataclasses import dataclass

@dataclass
class Gene:
    id: int
    funzione: int
    essenziale: int
    cromosoma: int

    def __str__(self):
        return f'{self.cromosoma_id}'

    def __repr__(self):
        return f'{self.cromosoma_id}'

    def __hash__(self):
        return hash(self.cromosoma_id)