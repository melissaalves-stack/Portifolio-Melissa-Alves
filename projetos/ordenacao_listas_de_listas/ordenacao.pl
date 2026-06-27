% TRABALHO DE PROGRAMACAO LOGICA - ORDENACAO DE LISTAS DE LISTAS
% Aluna: Melissa Hollanda de Oliveira Alves
% Disciplina: DCE672


% ==============================================================
% PARTE A - lsort/2: ordenacao pelo TAMANHO das sublistas
% ==============================================================

% Tarefa 1: calcular o tamanho de uma lista
tamanho([], 0).
tamanho([_ | Cauda], N) :-
    tamanho(Cauda, N_Resto),
    N is N_Resto + 1.

% Tarefa 2: associar cada sublista ao seu comprimento (usando a estrutura par/2 do slide)
associa_tam([], []).
associa_tam([Sub | Resto], [par(N, Sub) | Resto_Pares]) :-
    tamanho(Sub, N),
    associa_tam(Resto, Resto_Pares).

% Tarefa 3: ordenar as sublistas com base no comprimento (insertion sort)
ordena_pares(Pares, Resultado) :-
    insertion_sort(Pares, Pares_Ordenados),
    so_sublistas(Pares_Ordenados, Resultado).

insertion_sort([], []).
insertion_sort([Par | Resto], Ordenado) :-
    insertion_sort(Resto, Resto_Ordenado),
    insere(Par, Resto_Ordenado, Ordenado).

% Algoritmo de insercao adaptado perfeitamente dos Slides 65 e 66 da UNIFAL:
insere(par(C, S), [par(C2, S2) | R], [par(C2, S2) | R2]) :- 
    C > C2, 
    !, 
    insere(par(C, S), R, R2).
insere(Par, Lista, [Par | Lista]).

so_sublistas([], []).
so_sublistas([par(_, Sub) | Resto], [Sub | Resto2]) :-
    so_sublistas(Resto, Resto2).

% Tarefa 4: predicado principal
lsort(Entrada, Saida) :-
    associa_tam(Entrada, Pares),
    ordena_pares(Pares, Saida).


% ==============================================================
% PARTE B - lfsort/2: ordenacao pela FREQUENCIA dos tamanhos
% ==============================================================

% Tarefa 1: tamanho de cada sublista (reusa tamanho/2 da Parte A)
tamanhos([], []).
tamanhos([Sub | Resto], [N | Resto_N]) :-
    tamanho(Sub, N),
    tamanhos(Resto, Resto_N).

% Tarefa 2: calcular a frequencia de cada comprimento (usando a estrutura par/2 do slide)
frequencias([], []).
frequencias([N | Resto], Mapa) :-
    frequencias(Resto, Mapa_Resto),
    incrementa(N, Mapa_Resto, Mapa).

incrementa(N, [], [par(N, 1)]).
incrementa(N, [par(N, Qtd) | Resto], [par(N, Qtd2) | Resto]) :- !, Qtd2 is Qtd + 1.
incrementa(N, [Par | Resto], [Par | Resto2]) :-
    incrementa(N, Resto, Resto2).

% Tarefa 3: associar cada sublista a frequencia do seu comprimento
associa_freq([], _, []).
associa_freq([Sub | Resto], Mapa, [par(Freq, Sub) | Resto_Pares]) :-
    tamanho(Sub, N),
    busca(N, Mapa, Freq),
    associa_freq(Resto, Mapa, Resto_Pares).

busca(N, [par(N, Qtd) | _], Qtd) :- !.
busca(N, [_ | Resto], Qtd) :- busca(N, Resto, Qtd).

% Tarefa 4: predicado principal
lfsort(Entrada, Saida) :-
    tamanhos(Entrada, Tamanhos),
    frequencias(Tamanhos, Mapa),
    associa_freq(Entrada, Mapa, Pares),
    ordena_pares(Pares, Saida).


% ==============================================================
% TAREFA 5 - Execução e Comparação Direta dos Resultados
% ==============================================================
% Este predicado atende a Tarefa 5 executando a mesma lista de entrada 
% em ambos os metodos simultaneamente para podermos comparar as saidas.
%
% Exemplo de consulta para o teste no SWISH:
% ?- tarefa5([[a,b,c],[d,e],[f,g,h],[d,e],[i,j,k,l],[m,n],[o]], R_Lsort, R_Lfsort).
tarefa5(Entrada, R_Lsort, R_Lfsort) :-
    lsort(Entrada, R_Lsort),
    lfsort(Entrada, R_Lfsort).

/*
 ANÁLISE COMPARATIVA DAS SAÍDAS (JUSTIFICATIVA CONCEITUAL):
 
 Entrada padrão do enunciado: 
 [[a,b,c], [d,e], [f,g,h], [d,e], [i,j,k,l], [m,n], [o]]

 1. RESULTADO DO lsort/2:
    R_Lsort = [[o], [d,e], [d,e], [m,n], [a,b,c], [f,g,h], [i,j,k,l]]
    - Justificativa: Este predicado avalia puramente o comprimento bruto de cada 
      sublista de forma crescente. A sublista [o] tem apenas 1 elemento (a menor 
      de todas), portanto ganha a primeira posicao. Já a sublista [i,j,k,l] tem 
      tamanho 4 (a maior de todas), sendo colocada no final da lista.

 2. RESULTADO DO lfsort/2:
    R_Lfsort = [[i,j,k,l], [o], [a,b,c], [f,g,h], [d,e], [d,e], [m,n]]
    - Justificativa: Este predicado ignora o tamanho individual bruto e avalia 
      a frequencia (raridade) com que esse tamanho aparece na lista completa.
      Nesta entrada, o tamanho 4 (da lista [i,j,k,l]) e o tamanho 1 (da lista [o]) 
      sao os mais raros, pois aparecem apenas 1 unica vez cada na estrutura toda.
      Por possuírem a menor frequencia (1x), ganham prioridade no topo. 
      Em contrapartida, as listas de tamanho 2 aparecem 3 vezes no total; por serem 
      as mais comuns, sao jogadas para o fim da fila.
*/
