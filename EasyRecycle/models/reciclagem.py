class Reciclagem:
    def __init__(self, usuario, item, ponto_coleta, data):
        self.usuario = usuario
        self.item = item
        self.ponto_coleta = ponto_coleta
        self.data = data

    def resumo(self):
        return f"{self.usuario.nome} reciclou {self.item.nome} em {self.ponto_coleta.nome} na data {self.data}"
