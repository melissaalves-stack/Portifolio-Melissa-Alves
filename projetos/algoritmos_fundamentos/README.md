# 🧩 Algoritmos e Estruturas de Dados

Implementações do zero em C e C++: lista ligada, pilha, fila, árvore binária, ordenação e exercícios de programação competitiva.

## Como compilar e rodar

```bash
# Estruturas de dados (C)
gcc estruturas.c -o estruturas
./estruturas

# Exercícios de algoritmos (C++)
g++ exercicios.cpp -o exercicios
./exercicios
```

## O que está implementado

### `estruturas.c` — C
| Estrutura | O que é |
|-----------|---------|
| Lista Ligada | Nós conectados por ponteiros |
| Pilha (Stack) | LIFO — último a entrar, primeiro a sair |
| Fila (Queue) | FIFO — primeiro a entrar, primeiro a sair |
| Árvore Binária de Busca | Busca eficiente com hierarquia |
| Bubble Sort | Ordenação por comparação de pares |
| Busca Binária | Busca em O(log n) em array ordenado |

### `exercicios.cpp` — C++
Soluções de problemas estilo Beecrowd (judge.beecrowd.com):
- Verificação de número primo
- Sequência de Fibonacci (iterativo)
- Detecção de anagramas
- Contagem de frequência de caracteres com `std::map`
- Busca binária em vetor

## Tecnologias
- **C** — ponteiros, alocação de memória (`malloc`/`free`), structs
- **C++** — STL (`vector`, `map`, `string`, `sort`), referências
