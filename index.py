class Tokens:
    def __init__(self, tokens_type, tokens_value, linhas, colunas): #Contrutor da classe Tokens
        self.tokens_type = tokens_type
        self.tokens_value = tokens_value
        self.linhas = linhas
        self.colunas = colunas

    
    def __repr__(self):
        return f"Tokens({self.tokens_type}, {self.tokens_value}, {self.linhas}, {self.colunas})" #Representação da classe Tokens

class AnalisadorSintatico:
    def __init__(self, tokens): #Construtor da classe AnalisadorSintatico
        self.tokens = tokens
        self.pos = 0 #Posição atual do token
        self.tokens.append(Tokens("EOF", "EOF", linhas= -1, colunas= -1)) #Adiciona um token EOF para indicar o final

    def tokenAtual(self): #Retorna o token atual
        return self.tokens[self.pos]
    
    def proximoToken(self, k = 1): #Retorna o próximo token
        if self.pos + k < len(self.tokens):
            return self.tokens[self.pos + k]
        else:
            return Tokens("EOF", "EOF", linhas= -1, colunas= -1)
        
    def erro(self, mensagem): #Lança um erro de sintaxe
        token = self.tokenAtual()
        raise Exception(f"Erro de sintaxe: {mensagem} na linha {token.linhas} e coluna {token.colunas}"
                        f" token: {token.tokens_value} encontrado. Esperado: {mensagem}")
        
    def consumir(self, token_type): #Consome o token atual e avança para o próximo
        token = self.tokenAtual()
        if token.tokens_type == token_type:
            self.pos += 1
        else: 
            self.erro(token_type)


    def programa(self): #Inicia o programa. Enquanto não encontrar o token EOF, continua consumindo tokens. Retorna True se o programa for válido.
        while self.tokenAtual().tokens_type != "EOF":
            self.declaracao()
        return True
    
    def declaracao(self): #Verifica o tipo de declaração e chama a função correspondente
        if self.tokenAtual().tokens_type == "VAR":
            self.variavel()
        elif self.tokenAtual().tokens_type == "FUNC":
            self.funcao()
        elif self.tokenAtual().tokens_type == "STRUCT":
            self.estrutura()
        elif self.tokenAtual().tokens_type == "COMMENT":
            self.comentario()
        else:
            self.erro("declaracao")
        
    def variavel(self): #Verifica se a declaração é uma variável e consome os tokens correspondentes
        self.consumir("VAR")
        self.consumir("TYPE")
        self.consumir("ID")
        if self.tokenAtual().tokens_type == "EQUAL": #Se for um sinal de igual, consome o token e a expressão
            self.consumir("EQUAL")
            self.expressao()
        self.consumir("SEMICOLON") #Consome o ponto e vírgula no final da declaração
    
    def funcao(self): #Verifica se a declaração é uma função e consome os tokens correspondentes
        self.consumir("FUNC")
        self.consumir("TYPE")
        self.consumir("ID")
        self.consumir("LPAREN")
        if self.tokenAtual().tokens_type != "RPAREN": #Se não for um parêntese direito, consome os parâmetros
            self.parametros()
        self.consumir("RPAREN")
        self.bloco()
    
    def parametros(self): #Verifica se os parâmetros estão corretos e consome os tokens correspondentes
        self.parametro()
        while self.tokenAtual().tokens_type == "COMMA": #Se for uma vírgula, consome o token e o próximo parâmetro
            self.consumir("COMMA")
            self.parametro()

    def parametro(self): #Verifica se o parâmetro está correto e consome os tokens correspondentes
        self.consumir("TYPE")
        if self.tokenAtual().tokens_type == "ELIPSIS": #Se for um parenteses, consome o token
            self.consumir("ELIPSIS")
            self.consumir("ID")
        else:
            self.consumir("ID")
            if self.tokenAtual().tokens_type == "LBRACKET": #Se for um colchete, consome o token e o colchete direito
                self.consumir("LBRACKET")
                self.consumir("RBRACKET")

    def bloco(self): #Verifica se o bloco está correto e consome os tokens correspondentes
        self.consumir("LBRACE")
        while self.tokenAtual().tokens_type != "RBRACE":
            self.declaracao()
        self.consumir("RBRACE")

    def estrutura(self): #Verifica se a estrutura está correta e consome os tokens correspondentes
        self.consumir("STRUCT")
        self.consumir("ID")
        self.consumir("LBRACE")
        while self.tokenAtual().tokens_type != "RBRACE": #Enquanto não encontrar o colchete direito, consome os campos
            self.variavel()
        self.consumir("RBRACE")
        self.consumir("SEMICOLON")
