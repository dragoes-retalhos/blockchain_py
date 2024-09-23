import class_block

class Blockchain:
    def __init__(self):
        self.cadeia = [self._criar_bloco_genesis()]
        self.dificuldade = 2  # Dificuldade para a mineração (opcional)

    def _criar_bloco_genesis(self):
        # Primeiro bloco da blockchain, com dados iniciais
        return Bloco(0, "Bloco Gênesis", "0")

    def adicionar_bloco(self, dados):
        bloco_anterior = self.cadeia[-1]
        novo_bloco = Bloco(len(self.cadeia), dados, bloco_anterior.hash)
        novo_bloco.mine_bloco(self.dificuldade)  # Mineração, se aplicável
        self.cadeia.append(novo_bloco)

    def verificar_integridade(self):
        for i in range(1, len(self.cadeia)):
            bloco_atual = self.cadeia[i]
            bloco_anterior = self.cadeia[i-1]
            if bloco_atual.hash != bloco_atual._calcular_hash():
                print(f"Bloco {i} foi corrompido!")
                return False
            if bloco_atual.hash_bloco_anterior != bloco_anterior.hash:
                print(f"Bloco {i} perdeu o link com o bloco anterior!")
                return False
        return True

# Exemplo de uso
blockchain = Blockchain()
blockchain.adicionar_bloco("Coordenadas: 37.7749° N, 122.4194° W")
blockchain.adicionar_bloco("Coordenadas: 48.8566° N, 2.3522° E")

for bloco in blockchain.cadeia:
    print(bloco)
