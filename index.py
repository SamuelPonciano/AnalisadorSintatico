class Tokens:
    def __init__(self, tokens_type, tokens_value, linhas, colunas): 
        self.tokens_type = tokens_type
        self.tokens_value = tokens_value
        self.linhas = linhas
        self.colunas = colunas

    
    def __repr__(self):
        return f"Tokens({self.tokens_type}, {self.tokens_value}, {self.linhas}, {self.colunas})" 

class AnalisadorSintatico:
    def __init__(self, tokens): 
        self.tokens = tokens
        self.pos = 0 
        self.tokens.append(Tokens("EOF", "EOF", linhas= -1, colunas= -1)) 

    def tokenAtual(self): 
        return self.tokens[self.pos]
    
    def proximoToken(self, k = 1):
        if self.pos + k < len(self.tokens):
            return self.tokens[self.pos + k]
        else:
            return Tokens("EOF", "EOF", linhas= -1, colunas= -1)
        
    def erro(self, mensagem): 
        token = self.tokenAtual()
        raise Exception(f"Erro de sintaxe: {mensagem} na linha {token.linhas} e coluna {token.colunas}"
                        f" token: {token.tokens_value} encontrado. Esperado: {mensagem}")
        
    def avancaToken(self, token_type): 
        token = self.tokenAtual()
        if token.tokens_type == token_type:
            self.pos += 1
        else: 
            self.erro(token_type)


    def programa(self): 
        while self.tokenAtual().tokens_type != "EOF":
            self.declaracao()
        return True
    
    def declaracao(self): 
        if self.tokenAtual().tokens_type == "VAR":
            self.variavel()
        elif self.tokenAtual().tokens_type == "FUNC":
            self.funcao()
        elif self.tokenAtual().tokens_type == "STRUCT":
            self.estrutura()
        elif self.tokenAtual().tokens_type in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
            self.comentario()
        elif self.tokenAtual().tokens_type in ("IF", "ELSE", "WHILE", "FOR", "SWITCH", "BREAK", "CONTINUE", "RETURN"):
            self.estruturaControle()
        elif self.tokenAtual().tokens_type in ("ID", "NUM_INT", "NUM_FLOAT", "STRING", "LPAREN"):
            self.expressao()
        else:
            self.erro("declaracao")
        
    def variavel(self):
        self.avancaToken("VAR")
        self.avancaToken("TYPE")
        self.avancaToken("ID")
        if self.tokenAtual().tokens_type == "EQUAL":
            self.avancaToken("EQUAL")
            self.expressao()
        self.avancaToken("SEMICOLON")
    
    def funcao(self):
        self.avancaToken("FUNC")
        self.avancaToken("TYPE")
        self.avancaToken("ID")
        self.avancaToken("LPAREN")
        if self.tokenAtual().tokens_type != "RPAREN":
            self.parametros()
        self.avancaToken("RPAREN")
        self.bloco()    
    
    def parametros(self):
        self.parametros2()
        while self.tokenAtual().tokens_type == "COMMA": 
            self.avancaToken("COMMA")
            self.parametros2()

    def parametros2(self): 
        self.avancaToken("TYPE")
        if self.tokenAtual().tokens_type == "ELIPSIS": 
            self.avancaToken("ELIPSIS")
            self.avancaToken("ID")
        else:
            self.avancaToken("ID")
            if self.tokenAtual().tokens_type == "LBRACKET": 
                self.avancaToken("LBRACKET")
                self.avancaToken("RBRACKET")

    def bloco(self): 
        self.avancaToken("LBRACE")
        while self.tokenAtual().tokens_type != "RBRACE":
            self.declaracao()
        self.avancaToken("RBRACE")

    def estrutura(self): 
        self.avancaToken("STRUCT")
        self.avancaToken("ID")
        self.avancaToken("LBRACE")
        while self.tokenAtual().tokens_type != "RBRACE": 
            self.variavel()
        self.avancaToken("RBRACE")
        self.avancaToken("SEMICOLON")

    def comentario(self): 
        if self.tokenAtual().tokens_type in ("COMENTARIO_LINHA", "COMENTARIO_BLOCO"):
            self.avancaToken(self.tokenAtual().tokens_type)
        else:
            self.erro("comentario")
    
    def expressao(self): 
        if self.tokenAtual().tokens_type == "ID": 
            self.avancaToken("ID")
            if self.tokenAtual().tokens_type == "LBRACKET": 
                self.array() 
        elif self.tokenAtual().tokens_type in ("NUM_INT", "NUM_FLOAT", "STRING"): 
            self.avancaToken(self.tokenAtual().tokens_type)
        else:
            self.erro("expressao")
    
    def atribuicao(self): 
        if self.tokenAtual().tokens_type == "ID":
            self.avancaToken("ID")
            if self.tokenAtual().tokens_type in ("EQUAL", "PLUS_EQUAL", "MINUS_EQUAL", "MULTIPLY_EQUAL", "DIVIDE_EQUAL", "MODULO_EQUAL", "AND_EQUAL", "OR_EQUAL"):
                self.avancaToken(self.tokenAtual().tokens_type)
                self.expressao()
            else: 
                if self.tokenAtual().tokens_type in ("NUM_INT", "NUM_FLOAT", "STRING"):
                    self.avancaToken(self.tokenAtual().tokens_type)
                else:
                    self.erro("expressao")
    
    def estruturaControle(self): 
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

    
    def estruturaIf(self): 
        self.avancaToken("IF")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("RPAREN")
        self.bloco()
        if self.tokenAtual().tokens_type == "ELSE":
            self.avancaToken("ELSE")
            self.bloco()
        
    def estruturaWhile(self):
        self.avancaToken("WHILE")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("RPAREN")
        self.bloco()
    
    def estruturaFor(self): 
        self.avancaToken("FOR")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("SEMICOLON")
        self.expressao()
        self.avancaToken("SEMICOLON")
        self.expressao()
        self.avancaToken("RPAREN")
        self.bloco()
    
    def estruturaSwitch(self): 
        self.avancaToken("SWITCH")
        self.avancaToken("LPAREN")
        self.expressao()
        self.avancaToken("RPAREN")
        self.caseList() 
    
    def caseList(self):  
        self.avancaToken("LBRACE")
        while self.tokenAtual().tokens_type in ("CASE", "DEFAULT"): 
            self.caseDecl() 
        self.avancaToken("RBRACE")

           
    def caseDecl(self): 
        if self.tokenAtual().tokens_type == "CASE": 
            self.avancaToken("CASE")
            self.expressao()
            self.avancaToken("COLON")
            self.bloco()
        elif self.tokenAtual().tokens_type == "DEFAULT": 
            self.avancaToken("DEFAULT")
            self.avancaToken("COLON")
            self.bloco()
        else:
            self.erro("declaração de case")
    
    def estruturaBreak(self): 
        self.avancaToken("BREAK")
        self.avancaToken("SEMICOLON")
    
    def estruturaContinue(self): 
        self.avancaToken("CONTINUE")
        self.avancaToken("SEMICOLON")
    
    def estruturaReturn(self): 
        self.avancaToken("RETURN")
        self.expressao()
        self.avancaToken("SEMICOLON")

    def array(self):
        self.avancaToken("ID")
        self.avancaToken("LBRACKET")
        if self.tokenAtual().tokens_type != "RBRACKET": 
            self.expressao()
        self.avancaToken("RBRACKET")

    def arrayInicializacao(self):
        self.avancaToken("LBRACE")
        if self.tokenAtual().tokens_type != "RBRACE":
            self.expressaoLista() 
        self.avancaToken("RBRACE")

    def expressaoLista(self):
        self.expressao()
        while self.tokenAtual().tokens_type == "COMMA":
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
        while self.tokenAtual().tokens_type in ("EQUAL", "NOT_EQUAL", "LESS_THAN", "GREATER_THAN", "LESS_EQUAL", "GREATER_EQUAL"): 
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
        self.expressaoUnaria() 
        while self.tokenAtual().tokens_type in ("MULTIPLY", "DIVIDE", "MODULO"): 
            token = self.tokenAtual().tokens_type 
            self.avancaToken(token)
            self.expressaoUnaria() 

    def expressaoUnaria(self):
        if self.tokenAtual().tokens_type == "MINUS":
            self.avancaToken("MINUS")
            self.expressaoUnaria()
        elif self.tokenAtual().tokens_type in ("PLUSPLUS", "MINUSMINUS"): 
            token = self.tokenAtual().tokens_type 
            self.avancaToken(token)  
            self.expressaoPostfix() 
        else:
            self.expressaoPostfix()

    def expressaoPostfix(self):
        self.primaria() 
        while self.tokenAtual().tokens_type in ("LBRACKET", "LPAREN", "DOT", "ARROW"):
            if self.tokenAtual().tokens_type == "LBRACKET":
                self.avancaToken("LBRACKET") 
                self.expressao() 
                self.avancaToken("RBRACKET") 
            elif self.tokenAtual().tokens_type == "LPAREN":  
                self.avancaToken("LPAREN")  
                if self.tokenAtual().tokens_type != "RPAREN":
                    self.argumentos() 
                self.avancaToken("RPAREN") 
            elif self.tokenAtual().tokens_type == "DOT": 
                self.avancaToken("DOT") 
                self.avancaToken("ID") 
            elif self.tokenAtual().tokens_type == "ARROW": 
                self.avancaToken("ARROW") 
                self.avancaToken("ID")  

    def argumentos(self):
        if self.tokenAtual().tokens_type == "RPAREN":
            return
        else:
            self.expressaoLista()

    def expressaoLista(self):
        self.expressao()
        while self.tokenAtual().tokens_type == "COMMA": 
            self.avancaToken("COMMA")
            self.expressao()

    def primaria(self):
    
        if self.tokenAtual().tokens_type == "ID":  
            self.avancaToken("ID") 
        elif self.tokenAtual().tokens_type in ("NUM_INT", "NUM_DEC"): 
            token = self.tokenAtual().tokens_type
            self.avancaToken(token)
        elif self.tokenAtual().tokens_type == "STRING":  
            self.avancaToken("STRING")  
        elif self.tokenAtual().tokens_type == "LPAREN":  
            self.avancaToken("LPAREN")
            self.expressao()  
            self.avancaToken("RPAREN") 
        else:
            self.erro("expressão primária esperada")

if __name__ == "__main__":
    tokens = [
        # Os tokens de Exemplo ficam aqui
        ]

    try:
        analisador = AnalisadorSintatico(tokens)
        if analisador.programa():
            print("Programa válido!")
    except Exception as e:
        print("Erro encontrado em:", e)