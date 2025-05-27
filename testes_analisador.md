## Testes

### Teste 1: Declaração de variável e função

```python
test1 = [
    Tokens("VAR", "var", 1, 1),
    Tokens("TYPE", "int", 1, 5),
    Tokens("ID", "x", 1, 9),
    Tokens("FUNC", "func", 2, 1),
    Tokens("TYPE", "void", 2, 6),
    Tokens("ID", "main", 2, 11),
    Tokens("LPAREN", "(", 2, 16),
    Tokens("RPAREN", ")", 2, 17),
    Tokens("LBRACE", "{", 2, 18),
    Tokens("RBRACE", "}", 3, 1)
]
```

### Teste 2: Variável com atribuição

```python
test2 = [
    Tokens("VAR", "var", 1, 1),
    Tokens("TYPE", "int", 1, 5),
    Tokens("ID", "x", 1, 9),
    Tokens("EQUAL", "=", 1, 11),
    Tokens("NUM_INT", "10", 1, 13)
]
```

### Teste 3: Função com parâmetros e corpo simples

```python
test3 = [
    Tokens("FUNC", "func", 1, 1),
    Tokens("TYPE", "int", 1, 6),
    Tokens("ID", "sum", 1, 10),
    Tokens("LPAREN", "(", 1, 13),
    Tokens("TYPE", "int", 1, 14),
    Tokens("ID", "a", 1, 18),
    Tokens("COMMA", ",", 1, 19),
    Tokens("TYPE", "int", 1, 21),
    Tokens("ID", "b", 1, 25),
    Tokens("RPAREN", ")", 1, 26),
    Tokens("LBRACE", "{", 1, 27),
    Tokens("VAR", "var", 2, 1),
    Tokens("TYPE", "int", 2, 5),
    Tokens("ID", "result", 2, 9),
    Tokens("EQUAL", "=", 2, 16),
    Tokens("ID", "a", 2, 18),
    Tokens("PLUS", "+", 2, 20),
    Tokens("ID", "b", 2, 22),
    Tokens("RBRACE", "}", 3, 1)
]
```

### Teste 4: Declaração de estrutura

```python
test4 = [
    Tokens("STRUCT", "struct", 1, 1),
    Tokens("ID", "MyStruct", 1, 8),
    Tokens("LBRACE", "{", 1, 17),
    Tokens("VAR", "var", 2, 1),
    Tokens("TYPE", "int", 2, 5),
    Tokens("ID", "field", 2, 9),
    Tokens("RBRACE", "}", 3, 1)
]
```

### Teste 5: Comentário

```python
test5 = [
    Tokens("COMENTARIO_LINHA", "// This is a comment", 1, 1)
]
```

### Teste 6: Estrutura If

```python
test6 = [
    Tokens("IF", "if", 1, 1),
    Tokens("LPAREN", "(", 1, 4),
    Tokens("ID", "x", 1, 5),
    Tokens("GREATER_THAN", ">", 1, 7),
    Tokens("NUM_INT", "10", 1, 9),
    Tokens("RPAREN", ")", 1, 11),
    Tokens("LBRACE", "{", 1, 13),
    Tokens("RETURN", "return", 2, 1),
    Tokens("ID", "x", 2, 8),
    Tokens("RBRACE", "}", 3, 1)
]
```

### Teste 7: Estrutura While com atribuição interna

```python
test7 = [
    Tokens("WHILE", "while", 1, 1),
    Tokens("LPAREN", "(", 1, 7),
    Tokens("ID", "x", 1, 8),
    Tokens("LESS_THAN", "<", 1, 10),
    Tokens("NUM_INT", "20", 1, 12),
    Tokens("RPAREN", ")", 1, 14),
    Tokens("LBRACE", "{", 1, 16),
    Tokens("ID", "x", 2, 1),
    Tokens("EQUAL", "=", 2, 3),
    Tokens("ID", "x", 2, 5),
    Tokens("PLUS", "+", 2, 7),
    Tokens("NUM_INT", "1", 2, 9),
    Tokens("RBRACE", "}", 3, 1)
]
```

### Teste 8: Erro - Declaração de variável incompleta

```python
test8 = [
    Tokens("VAR", "var", 1, 1),
    Tokens("TYPE", "int", 1, 5),
    Tokens("ID", "x", 1, 9)
]
```

### Teste 9: Erro - Função sem parêntese de fechamento

```python
test9 = [
    Tokens("FUNC", "func", 1, 1),
    Tokens("TYPE", "void", 1, 6),
    Tokens("ID", "main", 1, 11),
    Tokens("LPAREN", "(", 1, 16),
    Tokens("LBRACE", "{", 1, 18),
    Tokens("RBRACE", "}", 2, 1)
]
```

### Teste 10: Erro - If sem parêntese de fechamento

```python
test10 = [
    Tokens("IF", "if", 1, 1),
    Tokens("LPAREN", "(", 1, 4),
    Tokens("ID", "x", 1, 5),
    Tokens("GREATER_THAN", ">", 1, 7),
    Tokens("NUM_INT", "10", 1, 9),
    Tokens("LBRACE", "{", 1, 13),
    Tokens("RETURN", "return", 2, 1),
    Tokens("ID", "x", 2, 8),
    Tokens("RBRACE", "}", 3, 1)
]
```

```python
test_cases = [
    ("Test 1: Variável e Função", test1),
    ("Test 2: Variável com Atribuição", test2),
    ("Test 3: Função com Parâmetros", test3),
    ("Test 4: Declaração de Estrutura", test4),
    ("Test 5: Comentário", test5),
    ("Test 6: Estrutura If", test6),
    ("Test 7: Estrutura While", test7),
    ("Test 8: Erro - Declaração de Variável Incompleta", test8),
    ("Test 9: Erro - Função Sem ')' ", test9),
    ("Test 10: Erro - If Sem ')'", test10)
]

