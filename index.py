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
        elif self.tokenAtual().tokens_type in ("IF", "ELSE", "WHILE", "FOR", "SWITCH", "BREAK", "CONTINUE", "RETURN"):
            self.EstruturaControle()
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

    def comentario(self): #Verifica se o comentário está correto e consome os tokens correspondentes
        if self.tokenAtual().tokens_type in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
            self.consumir(self.tokenAtual().tokens_type)
        else:
            self.erro("comentario")
    
    def expressao(self): #Verifica se a expressão está correta e consome os tokens correspondentes
        if self.tokenAtual().tokens_type == "ID": #Se for um identificador, consome o token e verifica se é uma atribuição ou uma chamada de função
            self.consumir("ID")
            if self.tokenAtual().tokens_type == "LBRACKET": #Se for um colchete, consome o token e a expressão
                self.Array() 
        elif self.tokenAtual().tokens_type in ("NUM_INT", "NUM_FLOAT", "STRING"): #Se for um número inteiro, número float ou string, consome o token
            self.consumir(self.tokenAtual().tokens_type)
        else:
            self.erro("expressao")
    
    def atribuicao(self): 
        if self.tokenAtual().tokens_type == "ID":
            self.consumir("ID")
            if self.tokenAtual().tokens_type in ("EQUAL", "PLUS_EQUAL", "MINUS_EQUAL", "MULTIPLY_EQUAL", "DIVIDE_EQUAL", "MODULO_EQUAL", "AND_EQUAL", "OR_EQUAL"): #Se for um sinal de atribuição, consome o token e a expressão
                self.consumir(self.tokenAtual().tokens_type)
                self.expressao()
            else: 
                if self.tokenAtual().tokens_type in ("NUM_INT", "NUM_FLOAT", "STRING"): # Se for um número inteiro, número float ou string, consome o token
                    self.consumir(self.tokenAtual().tokens_type)
                else:
                    self.erro("expressao")
    
    def EstruturaControle(self): #Verifica o tipo de estrutura de controle e chama a função correspondente
        if self.tokenAtual().tokens_type == "IF":
            self.Estrutura_if()
        elif self.tokenAtual().tokens_type == "WHILE":
            self.Estrutura_while()
        elif self.tokenAtual().tokens_type == "FOR":
            self.Estrutura_for()
        elif self.tokenAtual().tokens_type == "SWITCH":
            self.Estrutura_switch()
        elif self.tokenAtual().tokens_type == "BREAK":
            self.Estrutura_break()
        elif self.tokenAtual().tokens_type == "CONTINUE":
            self.Estrutura_continue()
        elif self.tokenAtual().tokens_type == "RETURN":
            self.Estrutura_return()
        else:
            self.erro("estrutura de controle")

    
    def Estrutura_if(self): #Verifica se a estrutura if está correta e consome os tokens correspondentes
        self.consumir("IF")
        self.consumir("LPAREN")
        self.expressao()
        self.consumir("RPAREN")
        self.bloco()
        if self.tokenAtual().tokens_type == "ELSE":
            self.consumir("ELSE")
            self.bloco()
        
    def Estrutura_while(self): #Verifica se a estrutura while está correta e consome os tokens correspondentes
        self.consumir("WHILE")
        self.consumir("LPAREN")
        self.expressao()
        self.consumir("RPAREN")
        self.bloco()
    
    def Estrutura_for(self): #Verifica se a estrutura for está correta e consome os tokens correspondentes
        self.consumir("FOR")
        self.consumir("LPAREN")
        self.expressao()
        self.consumir("SEMICOLON")
        self.expressao()
        self.consumir("SEMICOLON")
        self.expressao()
        self.consumir("RPAREN")
        self.bloco()
    
    def Estrutura_switch(self): #Verifica se a estrutura switch está correta e consome os tokens correspondentes
        self.consumir("SWITCH")
        self.consumir("LPAREN")
        self.expressao()
        self.consumir("RPAREN")
        self.case_list() # Lista de cases dentro do switch
    
    def case_list(self):  
        self.consumir("LBRACE")
        while self.tokenAtual().tokens_type in ("CASE", "DEFAULT"): # Enquanto não encontrar o colchete direito, consome os cases
            self.case_decl() #Chama a função que trata os cases
        self.consumir("RBRACE")

           
    def case_decl(self): 
        if self.tokenAtual().tokens_type == "CASE": #Verifica se o token atual é um case
            self.consumir("CASE")
            self.expressao()
            self.consumir("COLON")
            self.bloco()
        elif self.tokenAtual().tokens_type == "DEFAULT": #Verifica se o token atual é um default
            self.consumir("DEFAULT")
            self.consumir("COLON")
            self.bloco()
        else:
            self.erro("declaração de case")
    
    def Estrutura_break(self): #Verifica se a estrutura break está correta e consome os tokens correspondentes
        self.consumir("BREAK")
        self.consumir("SEMICOLON")
    
    def Estrutura_continue(self): #Verifica se a estrutura continue está correta e consome os tokens correspondentes
        self.consumir("CONTINUE")
        self.consumir("SEMICOLON")
    
    def Estrutura_return(self): #Verifica se a estrutura return está correta e consome os tokens correspondentes
        self.consumir("RETURN")
        self.expressao()
        self.consumir("SEMICOLON")

    def Array(self): #Verifica se o token atual é um array e consome os tokens correspondentes
        self.consumir("ID")
        self.consumir("LBRACKET")
        if self.tokenAtual().tokens_type != "RBRACKET": #Se não for um colchete direito
            self.expressao() #Chama a função de expressão
        self.consumir("RBRACKET")

    def Array_inicializacao(self): #Verifica se é uma inicialização de array 
        self.consumir("LBRACE")
        if self.tokenAtual().tokens_type != "RBRACE": #Se não for um colchete direito
            self.Expressao_lista() #Chama a função de lista de expressões
        self.consumir("RBRACE")

    def Expressao_lista(self):
        self.expressao()
        while self.tokenAtual().tokens_type == "COMMA": # Se for uma vírgula, consome o token e a próxima expressão
            self.consumir("COMMA")
            self.expressao()    
  