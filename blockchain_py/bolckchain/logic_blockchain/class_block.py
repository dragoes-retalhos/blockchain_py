
import hashlib
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class Bloco:

    # Definicao atributos
    def __init__(self, index, dados, hash_bloco_anterior):
        self.index = index  
        self.timestamp = time.time()  
        self.dados = self._criptografar_dados(dados)  
        self.hash_bloco_anterior = hash_bloco_anterior 
        self.nonce = 0 
        self.hash = self._calcular_hash()  
   
    # Utilizando AES para criptografar os dados
    def _criptografar_dados(self, dados):
        chave = get_random_bytes(16)  
        cipher = AES.new(chave, AES.MODE_GCM)
        nonce = cipher.nonce
        dados_criptografados, tag = cipher.encrypt_and_digest(dados.encode())
        return base64.b64encode(nonce + dados_criptografados).decode('utf-8')

    # Calcula o hash do bloco com base no conteúdo
    def _calcular_hash(self):
        conteudo = str(self.index) + str(self.timestamp) + self.dados + self.hash_bloco_anterior + str(self.nonce)
        return hashlib.sha256(conteudo.encode()).hexdigest()

    # Função de mineração, se for usar Proof of Work
    def mine_bloco(self, dificuldade):
        padrao = '0' * dificuldade
        while self.hash[:dificuldade] != padrao:
            self.nonce += 1
            self.hash = self._calcular_hash()

    # Nao exencial
    def __repr__(self):
        return f"Bloco(index={self.index}, hash={self.hash}, dados={self.dados})"






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
