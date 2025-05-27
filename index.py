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
        
    def avancaToken(self, token_type): #Consome o token atual e avança para o próximo
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
            self.estruturaControle()
        else:
            self.erro("declaracao")
        
    def variavel(self): #Verifica se a declaração é uma variável e consome os tokens correspondentes
        self.avancaToken("VAR")
        self.avancaToken("TYPE")
        self.avancaToken("ID")
        if self.tokenAtual().tokens_type == "EQUAL": #Se for um sinal de igual, consome o token e a expressão
            self.avancaToken("EQUAL")
            self.expressao()
        self.avancaToken("SEMICOLON") #Consome o ponto e vírgula no final da declaração
    
    def funcao(self): #Verifica se a declaração é uma função e consome os tokens correspondentes
        self.avancaToken("FUNC")
        self.avancaToken("TYPE")
        self.avancaToken("ID")
        self.avancaToken("LPAREN")
        if self.tokenAtual().tokens_type != "RPAREN": #Se não for um parêntese direito, consome os parâmetros
            self.parametros()
        self.avancaToken("RPAREN")
        self.bloco()    
    
    def parametros(self): #Verifica se os parâmetros estão corretos e consome os tokens correspondentes
        self.parametros2()
        while self.tokenAtual().tokens_type == "COMMA": #Se for uma vírgula, consome o token e o próximo parâmetro
            self.avancaToken("COMMA")
            self.parametros2()

    def parametros2(self): #Verifica se o parâmetro está correto e consome os tokens correspondentes
        self.avancaToken("TYPE")
        if self.tokenAtual().tokens_type == "ELIPSIS": #Se for um parenteses, consome o token
            self.avancaToken("ELIPSIS")
            self.avancaToken("ID")
        else:
            self.avancaToken("ID")
            if self.tokenAtual().tokens_type == "LBRACKET": #Se for um colchete, consome o token e o colchete direito
                self.avancaToken("LBRACKET")
                self.avancaToken("RBRACKET")

    def bloco(self): #Verifica se o bloco está correto e consome os tokens correspondentes
        self.avancaToken("LBRACE")
        while self.tokenAtual().tokens_type != "RBRACE":
            self.declaracao()
        self.avancaToken("RBRACE")

    def estrutura(self): #Verifica se a estrutura está correta e consome os tokens correspondentes
        self.avancaToken("STRUCT")
        self.avancaToken("ID")
        self.avancaToken("LBRACE")
        while self.tokenAtual().tokens_type != "RBRACE": #Enquanto não encontrar o colchete direito, consome os campos
            self.variavel()
        self.avancaToken("RBRACE")
        self.avancaToken("SEMICOLON")

    def comentario(self): #Verifica se o comentário está correto e consome os tokens correspondentes
        if self.tokenAtual().tokens_type in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
            self.avancaToken(self.tokenAtual().tokens_type)
        else:
            self.erro("comentario")
    
    def expressao(self): #Verifica se a expressão está correta e consome os tokens correspondentes
        if self.tokenAtual().tokens_type == "ID": #Se for um identificador, consome o token e verifica se é uma atribuição ou uma chamada de função
            self.avancaToken("ID")
            if self.tokenAtual().tokens_type == "LBRACKET": #Se for um colchete, consome o token e a expressão
                self.array() 
        elif self.tokenAtual().tokens_type in ("NUM_INT", "NUM_FLOAT", "STRING"): #Se for um número inteiro, número float ou string, consome o token
            self.avancaToken(self.tokenAtual().tokens_type)
        else:
            self.erro("expressao")
    
    def atribuicao(self): 
        if self.tokenAtual().tokens_type == "ID":
            self.avancaToken("ID")
            if self.tokenAtual().tokens_type in ("EQUAL", "PLUS_EQUAL", "MINUS_EQUAL", "MULTIPLY_EQUAL", "DIVIDE_EQUAL", "MODULO_EQUAL", "AND_EQUAL", "OR_EQUAL"): #Se for um sinal de atribuição, consome o token e a expressão
                self.avancaToken(self.tokenAtual().tokens_type)
                self.expressao()
            else: 
                if self.tokenAtual().tokens_type in ("NUM_INT", "NUM_FLOAT", "STRING"): # Se for um número inteiro, número float ou string, consome o token
                    self.avancaToken(self.tokenAtual().tokens_type)
                else:
                    self.erro("expressao")
    
    def estruturaControle(self): #Verifica o tipo de estrutura de controle e chama a função correspondente
        if self.tokenAtual().tokens_type == "IF":
            self.estruturaIf()
        elif self.tokenAtual().tokens_type == "WHILE":
            self.estruturaWhile()
        elif self.tokenAtual().tokens_type == "FOR":
            self.estruturaFor()
        elif self.tokenAtual().tokens_type == "SWITCH":
            self.estruturaSwitch()
        elif self.tokenAtual().tokens_type == "BREAK":
            self.estruturaBreak()
        elif self.tokenAtual().tokens_type == "CONTINUE":
            self.estruturaContinue()
        elif self.tokenAtual().tokens_type == "RETURN":
            self.estruturaReturn()
        else:
            self.erro("estrutura de controle")

    
    def estruturaIf(self): #Verifica se a estrutura if está correta e consome os tokens correspondentes
        self.avancaToken("IF")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("RPAREN")
        self.bloco()
        if self.tokenAtual().tokens_type == "ELSE":
            self.avancaToken("ELSE")
            self.bloco()
        
    def estruturaWhile(self): #Verifica se a estrutura while está correta e consome os tokens correspondentes
        self.avancaToken("WHILE")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("RPAREN")
        self.bloco()
    
    def estruturaFor(self): #Verifica se a estrutura for está correta e consome os tokens correspondentes
        self.avancaToken("FOR")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("SEMICOLON")
        self.expressao()
        self.avancaToken("SEMICOLON")
        self.expressao()
        self.avancaToken("RPAREN")
        self.bloco()
    
    def estruturaSwitch(self): #Verifica se a estrutura switch está correta e consome os tokens correspondentes
        self.avancaToken("SWITCH")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("RPAREN")
        self.caseList() # Lista de cases dentro do switch
    
    def caseList(self):  
        self.avancaToken("LBRACE")
        while self.tokenAtual().tokens_type in ("CASE", "DEFAULT"): # Enquanto não encontrar o colchete direito, consome os cases
            self.caseDecl() #Chama a função que trata os cases
        self.avancaToken("RBRACE")

           
    def caseDecl(self): 
        if self.tokenAtual().tokens_type == "CASE": #Verifica se o token atual é um case
            self.avancaToken("CASE")
            self.expressao()
            self.avancaToken("COLON")
            self.bloco()
        elif self.tokenAtual().tokens_type == "DEFAULT": #Verifica se o token atual é um default
            self.avancaToken("DEFAULT")
            self.avancaToken("COLON")
            self.bloco()
        else:
            self.erro("declaração de case")
    
    def estruturaBreak(self): #Verifica se a estrutura break está correta e consome os tokens correspondentes
        self.avancaToken("BREAK")
        self.avancaToken("SEMICOLON")
    
    def estruturaContinue(self): #Verifica se a estrutura continue está correta e consome os tokens correspondentes
        self.avancaToken("CONTINUE")
        self.avancaToken("SEMICOLON")
    
    def estruturaReturn(self): #Verifica se a estrutura return está correta e consome os tokens correspondentes
        self.avancaToken("RETURN")
        self.expressao()
        self.avancaToken("SEMICOLON")

    def array(self): #Verifica se o token atual é um array e consome os tokens correspondentes
        self.avancaToken("ID")
        self.avancaToken("LBRACKET")
        if self.tokenAtual().tokens_type != "RBRACKET": #Se não for um colchete direito
            self.expressao() #Chama a função de expressão
        self.avancaToken("RBRACKET")

    def arrayInicializacao(self): #Verifica se é uma inicialização de array 
        self.avancaToken("LBRACE")
        if self.tokenAtual().tokens_type != "RBRACE": #Se não for um colchete direito
            self.expressaoLista() #Chama a função de lista de expressões
        self.avancaToken("RBRACE")

    def expressaoLista(self):
        self.expressao()
        while self.tokenAtual().tokens_type == "COMMA": # Se for uma vírgula, consome o token e a próxima expressão
            self.avancaToken("COMMA")
            self.expressao()
    
    def expressao(self):
        self.expressaoLogica()

    def expressaoLogica(self):
        if self.tokenAtual().tokens_type == "NOT": 
            self.avancaToken("NOT")
            self.expressaoLogica()
        else:
            self.expressaoRelacional()
        while self.tokenAtual().tokens_type in ("AND", "OR"): 
            token = self.tokenAtual().tokens_type
            self.avancaToken(token)
            self.expressaoRelacional()

    def expressaoRelacional(self):
        self.expressaoAritmetica()
        while self.tokenAtual().tokens_type in ("EQUAL", "NOT_EQUAL", "LESS_THAN", "GREATER_THAN", "LESS_EQUAL", "GREATER_EQUAL"): # < less than, > greater than, <= less equal, >= greater equal
            token = self.tokenAtual().tokens_type
            self.avancaToken(token)
            self.expressaoAritmetica()

    def expressaoAritmetica(self):
        self.expressaoMultiplicativa()
        while self.tokenAtual().tokens_type in ("PLUS", "MINUS"):
            token = self.tokenAtual().tokens_type
            self.avancaToken(token)
            self.expressaoMultiplicativa()
            ##


def expressaoMultiplicativa(self):
  #analisa expressao multiplicativa
    self.expressaoUnaria()  # começa analisando expressões unarias (+,-, ...)
    while self.tokenAtual().tokens_type in ("MULTIPLY", "DIVIDE", "MODULO"):  # verifica operadores de multiplicacao
        token = self.tokenAtual().tokens_type  # pega o operador
        self.avancaToken()  # consome o operador
        self.expressaoUnaria()  # passa para a proxima expressao depois do multiplicativo

def expressaoUnaria(self):
 #analisa expressao unaria
    if self.tokenAtual().tokens_type in ("PLUS", "MINUS"):  # checa se é mais(+) ou menos(-)
        self.avancaToken()  # consome
        self.expressaoUnaria() 
    elif self.tokenAtual().tokens_type == "NOT":  # se for ! ele consome
        self.avancaToken()
        self.expressaoRelacional()
    elif self.tokenAtual().tokens_type in ("ID", "NUM_INT", "NUM_FLOAT", "STRING", "TEXTO"):  # checa se é valor literal
        self.avancaToken()  #consome
    elif self.tokenAtual().tokens_type == "LPAREN":  # checa se é parentese
        self.avancaToken()
        self.expressao()  
        self.avancaToken()  
    else:
        self.erro("expressão unária esperada")

def expressaoPostfix(self):
   # analisa expressao postfix
    self.primaria()  # analisa tokens primarios
    while self.tokenAtual().tokens_type in ("LBRACKET", "LPAREN", "DOT", "ARROW"):
        if self.tokenAtual().tokens_type == "LBRACKET":  # se for um arrat
            self.avancaToken()  # consome o Lbracket
            self.expressao()  # analisa expressao
            self.avancaToken()  # consome
        elif self.tokenAtual().tokens_type == "LPAREN":  
            self.avancaToken()  # consome parenteses
            if self.tokenAtual().tokens_type != "RPAREN":
                self.argumentos()  # analisa args
            self.avancaToken()  # consome parenteses
        elif self.tokenAtual().tokens_type == "DOT":  #objeto-> campo
            self.avancaToken()  # consome ponto
            self.avancaToken() 
        elif self.tokenAtual().tokens_type == "ARROW":  # acesso a objeto -> campo
            self.avancaToken()  # consome ->
            self.avancaToken()  # consome identificador

def argumentos(self):
    self.expressaoLista()

    def expressaoLista(self):
        self.expressao()
        while self.tokenAtual().tokens_type == "COMMA": #se houver virgula consome e analisa.
            self.avancaToken()
            self.expressao()
def primaria(self):
 
    if self.tokenAtual().tokens_type == "ID":  
        self.avancaToken() 
    elif self.tokenAtual().tokens_type in ("NUM_INT", "NUM_DEC"):  
        self.avancaToken() 
    elif self.tokenAtual().tokens_type == "TEXTO":  
        self.avancaToken()  
    elif self.tokenAtual().tokens_type == "LPAREN":  
        self.avancaToken()
        self.expressao()  
        self.avancaToken() 
    else:
        self.erro("expressão primária esperada")