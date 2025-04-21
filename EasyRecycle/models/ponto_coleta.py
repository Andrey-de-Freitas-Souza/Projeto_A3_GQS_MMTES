class PontoColeta:
    def __init__(self, id, nome, endereco):
        self.id = id
        self.nome = nome
        self.endereco = endereco

    def __str__(self):
        return f"{self.nome} - {self.endereco}"
