class Util:
    @staticmethod
    def transformListNome(list):
        dadosDeTreino = list()
        for nome in list:
            dadosDeTreino.append({(nome.upper(),{"entities": [(0, len(nome), "PERSON")]})})
            dadosDeTreino.append({(nome.lower(), {"entities": [(0, len(nome), "PERSON")]})})
        return dadosDeTreino