/*
EXERCÍCIOS DE ALGORITMOS — BEECROWD
Soluções de problemas clássicos de programação competitiva.

O QUE É BEECROWD?
  Uma plataforma online onde você submete seu código e ele é
  testado automaticamente contra casos de teste. Se passar em
  todos, você resolve o problema. Ótimo para praticar lógica
  e algoritmos. Acesse: judge.beecrowd.com

COMO COMPILAR UM EXERCÍCIO ESPECÍFICO:
  g++ exercicios.cpp -o exercicios
  ./exercicios

CADA FUNÇÃO ABAIXO É UMA SOLUÇÃO INDEPENDENTE.
*/

#include <iostream>
#include <vector>
#include <algorithm>  /* sort, min, max */
#include <string>
#include <map>
#include <numeric>    /* accumulate */

using namespace std;


/* ═════════════════════════════════════════════════════════════
   PROBLEMA 1 — SOMA SIMPLES (Beecrowd 1001)
   Lê dois números inteiros e imprime a soma.
   Parece trivial, mas é o "Hello World" do Beecrowd.
═════════════════════════════════════════════════════════════ */

void soma_simples() {
    cout << "\n━━ Problema 1: Soma Simples ━━━━━━━━━━━━━\n";

    int a = 10, b = 9;
    cout << "  " << a << " + " << b << " = " << a + b << "\n";

    /* Em C++, cout é o "print" — envia texto para a tela.
       << é o operador de inserção — "insere" o valor no fluxo.
       "\n" pula linha (equivalente ao \n do Python). */
}


/* ═════════════════════════════════════════════════════════════
   PROBLEMA 2 — NÚMERO PRIMO
   Verifica se um número é primo.

   O que é número primo?
   É um número maior que 1 que só é divisível por 1 e por ele mesmo.
   Ex: 2, 3, 5, 7, 11, 13...

   Otimização: só precisamos testar divisores até a raiz quadrada
   do número. Se n = 36, basta testar até 6 — se não achou divisor
   até lá, não vai achar depois.
═════════════════════════════════════════════════════════════ */

bool eh_primo(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;  /* elimina todos os pares */

    /* i * i <= n é mais eficiente que i <= sqrt(n) */
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

void verificar_primos() {
    cout << "\n━━ Problema 2: Números Primos ━━━━━━━━━━━\n";

    vector<int> testes = {1, 2, 3, 4, 17, 18, 97, 100};

    for (int n : testes) {
        /* O laço "for (tipo var : coleção)" percorre cada elemento.
           É equivalente ao "for n in lista" do Python. */
        cout << "  " << n << " → " << (eh_primo(n) ? "primo" : "não primo") << "\n";
    }

    cout << "  Primos até 50: ";
    for (int i = 2; i <= 50; i++)
        if (eh_primo(i)) cout << i << " ";
    cout << "\n";
}


/* ═════════════════════════════════════════════════════════════
   PROBLEMA 3 — FIBONACCI
   Calcula o N-ésimo número da sequência de Fibonacci.

   Sequência: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...
   Cada número é a soma dos dois anteriores.

   Versão iterativa (recomendada) vs recursiva:
   A recursiva é mais elegante mas ineficiente — recalcula
   os mesmos valores muitas vezes. A iterativa é O(n).
═════════════════════════════════════════════════════════════ */

long long fibonacci(int n) {
    if (n <= 1) return n;
    long long a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        long long temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

void calcular_fibonacci() {
    cout << "\n━━ Problema 3: Fibonacci ━━━━━━━━━━━━━━━━\n";
    cout << "  Primeiros 10 termos: ";
    for (int i = 0; i < 10; i++)
        cout << fibonacci(i) << " ";
    cout << "\n";
    cout << "  Fibonacci(30) = " << fibonacci(30) << "\n";
    cout << "  Fibonacci(50) = " << fibonacci(50) << "\n";
}


/* ═════════════════════════════════════════════════════════════
   PROBLEMA 4 — ANAGRAMA
   Verifica se duas palavras são anagramas uma da outra.

   O que é anagrama?
   Duas palavras são anagramas se têm as mesmas letras,
   possivelmente em ordem diferente.
   Ex: "roma" e "amor", "listen" e "silent"

   Solução: ordena as letras das duas palavras e compara.
   Se ficarem iguais, são anagramas.
═════════════════════════════════════════════════════════════ */

bool eh_anagrama(string a, string b) {
    /* Converte para minúsculas para comparação sem distinção */
    for (char &c : a) c = tolower(c);
    for (char &c : b) c = tolower(b[&c - &b[0]]);

    /* sort ordena os caracteres alfabeticamente */
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());

    return a == b;
}

void verificar_anagramas() {
    cout << "\n━━ Problema 4: Anagramas ━━━━━━━━━━━━━━━━\n";

    vector<pair<string,string>> pares = {
        {"roma", "amor"},
        {"listen", "silent"},
        {"hello", "world"},
        {"triangle", "integral"},
    };

    for (auto &p : pares) {
        string a = p.first, b = p.second;
        sort(a.begin(), a.end());
        sort(b.begin(), b.end());
        bool anagrama = (a == b);
        cout << "  \"" << p.first << "\" e \"" << p.second << "\": "
             << (anagrama ? "anagramas ✓" : "não são anagramas ✗") << "\n";
    }
}


/* ═════════════════════════════════════════════════════════════
   PROBLEMA 5 — CONTAGEM DE FREQUÊNCIA
   Conta quantas vezes cada caractere aparece em um texto.

   Usa std::map — equivalente ao dict do Python.
   map<char, int> → chave é um char, valor é um int (contagem).
═════════════════════════════════════════════════════════════ */

void contar_frequencia() {
    cout << "\n━━ Problema 5: Frequência de Caracteres ━\n";

    string texto = "programacao";
    map<char, int> freq;

    /* Percorre cada caractere e incrementa o contador */
    for (char c : texto) {
        freq[c]++;  /* se não existe ainda, começa em 0 e vira 1 */
    }

    cout << "  Texto: \"" << texto << "\"\n";
    cout << "  Frequência:\n";

    /* map é sempre ordenado pela chave (alfabeticamente) */
    for (auto &par : freq) {
        cout << "    '" << par.first << "' → " << par.second << "x\n";
    }
}


/* ═════════════════════════════════════════════════════════════
   PROBLEMA 6 — BUSCA BINÁRIA (implementação em C++)
   Busca eficiente em um vetor ordenado.

   Complexidade: O(log n) — para 1 milhão de elementos,
   faz no máximo ~20 comparações. Incrível!
═════════════════════════════════════════════════════════════ */

int busca_binaria(vector<int> &arr, int alvo) {
    int esq = 0, dir = arr.size() - 1;
    while (esq <= dir) {
        int meio = esq + (dir - esq) / 2;  /* evita overflow */
        if (arr[meio] == alvo) return meio;
        if (arr[meio] < alvo)  esq = meio + 1;
        else                   dir = meio - 1;
    }
    return -1;
}

void demonstrar_busca_binaria() {
    cout << "\n━━ Problema 6: Busca Binária ━━━━━━━━━━━━\n";

    vector<int> arr = {2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91};

    cout << "  Vetor: ";
    for (int x : arr) cout << x << " ";
    cout << "\n";

    vector<int> alvos = {23, 45, 99};
    for (int alvo : alvos) {
        int idx = busca_binaria(arr, alvo);
        if (idx != -1)
            cout << "  Buscar " << alvo << ": encontrado no índice " << idx << "\n";
        else
            cout << "  Buscar " << alvo << ": não encontrado\n";
    }
}


/* ─────────────────────────────────────────────────────────────
   PROGRAMA PRINCIPAL
───────────────────────────────────────────────────────────── */

int main() {
    cout << "╔══════════════════════════════════════════╗\n";
    cout << "║   ALGORITMOS E RESOLUÇÃO DE PROBLEMAS   ║\n";
    cout << "╚══════════════════════════════════════════╝\n";

    soma_simples();
    verificar_primos();
    calcular_fibonacci();
    verificar_anagramas();
    contar_frequencia();
    demonstrar_busca_binaria();

    cout << "\n  ✅ Todos os exercícios concluídos!\n\n";
    return 0;
}
