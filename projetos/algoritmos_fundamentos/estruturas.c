/*
ALGORITMOS E ESTRUTURAS DE DADOS
Implementacoes do zero em C: lista ligada, pilha, fila e arvore binaria.

COMO COMPILAR E RODAR:
  gcc estruturas.c -o estruturas
  ./estruturas

  Ou no Windows:
  gcc estruturas.c -o estruturas.exe
  estruturas.exe
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/*
   O QUE E UM PONTEIRO?
   Um ponteiro e uma variavel que guarda um ENDERECO de memoria,
   nao um valor diretamente. Em vez de guardar o numero 42,
   ele guarda "o numero 42 esta na posicao 0x7fff5abc da memoria".

   int x = 42;      -> x guarda o valor 42
   int *p = &x;     -> p guarda o endereco de x
   *p               -> "vai ate o endereco" e le o valor (42)

   O QUE E malloc?
   malloc(n) reserva n bytes na memoria heap e retorna um ponteiro
   para esse espaco. E como pedir um pedaco de papel em branco.
   free(p) devolve esse espaco quando nao precisamos mais.
*/


/*
   1. LISTA LIGADA (Linked List)

   O que e?
   Uma sequencia de nos onde cada no guarda um valor e um ponteiro
   para o proximo no. Diferente de um array, os elementos nao
   ficam em posicoes consecutivas na memoria.

   Array:  [10][20][30][40]     -> posicoes fixas e consecutivas
   Lista:  10 -> 20 -> 30 -> 40 -> NULL  -> cada no aponta para o proximo

   Vantagem: inserir/remover no inicio e O(1) (instantaneo)
   Desvantagem: acessar o elemento do meio e O(n) (precisa percorrer)
*/

typedef struct No {
    int valor;
    struct No *proximo;
} No;

No* lista_inserir(No *cabeca, int valor) {
    No *novo = (No*) malloc(sizeof(No));
    novo->valor   = valor;
    novo->proximo = cabeca;
    return novo;
}

void lista_exibir(No *cabeca) {
    printf("  Lista: ");
    No *atual = cabeca;
    while (atual != NULL) {
        printf("%d", atual->valor);
        if (atual->proximo != NULL) printf(" -> ");
        atual = atual->proximo;
    }
    printf(" -> NULL\n");
}

int lista_buscar(No *cabeca, int valor) {
    No *atual = cabeca;
    while (atual != NULL) {
        if (atual->valor == valor) return 1;
        atual = atual->proximo;
    }
    return 0;
}

void lista_liberar(No *cabeca) {
    No *atual = cabeca;
    while (atual != NULL) {
        No *proximo = atual->proximo;
        free(atual);
        atual = proximo;
    }
}


/*
   2. PILHA (Stack)

   O que e?
   Uma estrutura LIFO: Last In, First Out (ultimo a entrar,
   primeiro a sair). Como uma pilha de pratos.

   Operacoes:
     push(x) -> empilha x no topo
     pop()   -> desempilha e retorna o topo
     peek()  -> olha o topo sem remover

   Usos reais: historico de desfazer em editores, call stack,
   navegacao de paginas no navegador.
*/

#define TAMANHO_MAX 100

typedef struct {
    int dados[TAMANHO_MAX];
    int topo;
} Pilha;

void pilha_iniciar(Pilha *p) {
    p->topo = -1;
}

int pilha_vazia(Pilha *p) {
    return p->topo == -1;
}

void pilha_push(Pilha *p, int valor) {
    if (p->topo >= TAMANHO_MAX - 1) {
        printf("  AVISO: Pilha cheia!\n");
        return;
    }
    p->topo++;
    p->dados[p->topo] = valor;
}

int pilha_pop(Pilha *p) {
    if (pilha_vazia(p)) {
        printf("  AVISO: Pilha vazia!\n");
        return -1;
    }
    int valor = p->dados[p->topo];
    p->topo--;
    return valor;
}

int pilha_peek(Pilha *p) {
    if (pilha_vazia(p)) return -1;
    return p->dados[p->topo];
}

void pilha_exibir(Pilha *p) {
    printf("  Pilha (topo -> base): ");
    for (int i = p->topo; i >= 0; i--) {
        printf("%d ", p->dados[i]);
    }
    printf("\n");
}


/*
   3. FILA (Queue)

   O que e?
   Uma estrutura FIFO: First In, First Out (primeiro a entrar,
   primeiro a sair). Como uma fila de banco.

   Operacoes:
     enqueue(x) -> entra no final da fila
     dequeue()  -> sai do inicio da fila

   Usos reais: fila de impressao, requisicoes de servidor web,
   sistemas de mensagens.
*/

typedef struct {
    int dados[TAMANHO_MAX];
    int inicio;
    int fim;
    int tamanho;
} Fila;

void fila_iniciar(Fila *f) {
    f->inicio  = 0;
    f->fim     = 0;
    f->tamanho = 0;
}

int fila_vazia(Fila *f) {
    return f->tamanho == 0;
}

void fila_enqueue(Fila *f, int valor) {
    if (f->tamanho >= TAMANHO_MAX) {
        printf("  AVISO: Fila cheia!\n");
        return;
    }
    f->dados[f->fim] = valor;
    f->fim = (f->fim + 1) % TAMANHO_MAX;
    f->tamanho++;
}

int fila_dequeue(Fila *f) {
    if (fila_vazia(f)) {
        printf("  AVISO: Fila vazia!\n");
        return -1;
    }
    int valor  = f->dados[f->inicio];
    f->inicio  = (f->inicio + 1) % TAMANHO_MAX;
    f->tamanho--;
    return valor;
}

void fila_exibir(Fila *f) {
    printf("  Fila (inicio -> fim): ");
    for (int i = 0; i < f->tamanho; i++) {
        printf("%d ", f->dados[(f->inicio + i) % TAMANHO_MAX]);
    }
    printf("\n");
}


/*
   4. ARVORE BINARIA DE BUSCA (Binary Search Tree)

   O que e?
   Uma estrutura onde cada no tem ate dois filhos.
   Regra: valores menores ficam a esquerda, maiores a direita.

   Exemplo com valores 50, 30, 70, 20, 40:

            50
           /  \
         30    70
        /  \
       20   40

   Buscar 40: 50 -> esquerda -> 30 -> direita -> encontrou!
   Cada passo elimina metade da arvore -> busca muito eficiente.
*/

typedef struct NoArvore {
    int valor;
    struct NoArvore *esquerda;
    struct NoArvore *direita;
} NoArvore;

NoArvore* arvore_inserir(NoArvore *raiz, int valor) {
    if (raiz == NULL) {
        NoArvore *novo = (NoArvore*) malloc(sizeof(NoArvore));
        novo->valor    = valor;
        novo->esquerda = NULL;
        novo->direita  = NULL;
        return novo;
    }
    if (valor < raiz->valor)
        raiz->esquerda = arvore_inserir(raiz->esquerda, valor);
    else if (valor > raiz->valor)
        raiz->direita = arvore_inserir(raiz->direita, valor);
    return raiz;
}

int arvore_buscar(NoArvore *raiz, int valor) {
    if (raiz == NULL)         return 0;
    if (valor == raiz->valor) return 1;
    if (valor < raiz->valor)
        return arvore_buscar(raiz->esquerda, valor);
    return arvore_buscar(raiz->direita, valor);
}

void arvore_em_ordem(NoArvore *raiz) {
    if (raiz == NULL) return;
    arvore_em_ordem(raiz->esquerda);
    printf("%d ", raiz->valor);
    arvore_em_ordem(raiz->direita);
}

void arvore_liberar(NoArvore *raiz) {
    if (raiz == NULL) return;
    arvore_liberar(raiz->esquerda);
    arvore_liberar(raiz->direita);
    free(raiz);
}


/*
   5. ORDENACAO E BUSCA

   Bubble Sort: compara pares adjacentes e troca se estiver errado.
   Simples de entender, mas lento para arrays grandes: O(n2).

   Binary Search: busca eficiente em array JA ORDENADO.
   A cada passo elimina metade dos elementos: O(log n).
*/

void bubble_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp   = arr[j];
                arr[j]     = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

int binary_search(int arr[], int n, int alvo) {
    int esq = 0, dir = n - 1;
    while (esq <= dir) {
        int meio = (esq + dir) / 2;
        if (arr[meio] == alvo)  return meio;
        if (arr[meio] < alvo)   esq = meio + 1;
        else                    dir = meio - 1;
    }
    return -1;
}

void imprimir_array(int arr[], int n) {
    printf("  [");
    for (int i = 0; i < n; i++) {
        printf("%d", arr[i]);
        if (i < n - 1) printf(", ");
    }
    printf("]\n");
}


/*
   PROGRAMA PRINCIPAL
*/

int main() {
    printf("==========================================\n");
    printf("   ALGORITMOS E ESTRUTURAS DE DADOS\n");
    printf("==========================================\n\n");

    /* -- Lista Ligada -- */
    printf("-- 1. LISTA LIGADA ---------------------------\n");
    No *lista = NULL;
    lista = lista_inserir(lista, 10);
    lista = lista_inserir(lista, 20);
    lista = lista_inserir(lista, 30);
    lista = lista_inserir(lista, 40);
    lista_exibir(lista);
    printf("  Buscar 20: %s\n", lista_buscar(lista, 20) ? "encontrado" : "nao encontrado");
    printf("  Buscar 99: %s\n", lista_buscar(lista, 99) ? "encontrado" : "nao encontrado");
    lista_liberar(lista);

    /* -- Pilha -- */
    printf("\n-- 2. PILHA (LIFO) ---------------------------\n");
    Pilha pilha;
    pilha_iniciar(&pilha);
    pilha_push(&pilha, 10);
    pilha_push(&pilha, 20);
    pilha_push(&pilha, 30);
    pilha_exibir(&pilha);
    printf("  Topo: %d\n", pilha_peek(&pilha));
    printf("  Pop: %d\n",  pilha_pop(&pilha));
    printf("  Pop: %d\n",  pilha_pop(&pilha));
    pilha_exibir(&pilha);

    /* -- Fila -- */
    printf("\n-- 3. FILA (FIFO) ----------------------------\n");
    Fila fila;
    fila_iniciar(&fila);
    fila_enqueue(&fila, 10);
    fila_enqueue(&fila, 20);
    fila_enqueue(&fila, 30);
    fila_exibir(&fila);
    printf("  Dequeue: %d\n", fila_dequeue(&fila));
    printf("  Dequeue: %d\n", fila_dequeue(&fila));
    fila_exibir(&fila);

    /* -- Arvore Binaria -- */
    printf("\n-- 4. ARVORE BINARIA DE BUSCA ----------------\n");
    NoArvore *arvore = NULL;
    int valores[] = {50, 30, 70, 20, 40, 60, 80};
    int qtd = sizeof(valores) / sizeof(valores[0]);
    for (int i = 0; i < qtd; i++)
        arvore = arvore_inserir(arvore, valores[i]);

    printf("  Em ordem (deve sair crescente): ");
    arvore_em_ordem(arvore);
    printf("\n");
    printf("  Buscar 40: %s\n", arvore_buscar(arvore, 40) ? "encontrado" : "nao encontrado");
    printf("  Buscar 99: %s\n", arvore_buscar(arvore, 99) ? "encontrado" : "nao encontrado");
    arvore_liberar(arvore);

    /* -- Ordenacao e Busca -- */
    printf("\n-- 5. ORDENACAO E BUSCA ----------------------\n");
    int nums[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(nums) / sizeof(nums[0]);

    printf("  Antes:  ");
    imprimir_array(nums, n);

    bubble_sort(nums, n);

    printf("  Depois: ");
    imprimir_array(nums, n);

    int alvo = 25;
    int idx  = binary_search(nums, n, alvo);
    printf("  Busca binaria por %d: ", alvo);
    if (idx != -1)
        printf("encontrado no indice %d\n", idx);
    else
        printf("nao encontrado\n");

    printf("\n  Tudo funcionando!\n\n");
    return 0;
}