class CategoriaItem:
    def __init__(self, id, nome, descricao):
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return f"{self.nome} - {self.descricao}"

class ItemReciclavel:
    def __init__(self, id, nome, categoria: CategoriaItem, peso):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.peso = peso

    def __str__(self):
        return f"{self.nome} ({self.categoria.nome}) - {self.peso}g"
