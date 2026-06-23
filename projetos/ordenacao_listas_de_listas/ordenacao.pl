% TRABALHO DE PROGRAMAÇÃO LÓGICA - ORDENAÇÃO DE LISTAS DE LISTAS
% Aluna: Melissa Hollanda de Oliveira Alves
% Disciplina: DCE672

% LISTA DE TAREFAS
% TAREFA 1: Determinar o comprimento de cada sublista
% - O que faz: Mede o tamanho de cada pedaço da lista.
% - No Exemplo: [a,b] tem 2 elementos | [c] tem 1 | [a,b] tem 2.
% - Resultado: [2, 1, 2]

% TAREFA 2: Calcular a frequência de cada comprimento
% - O que faz: Conta quantas vezes cada tamanho se repetiu na Tarefa 1.
% - No Exemplo: O tamanho 2 apareceu 2 vezes. O tamanho 1 apareceu 1 vez.
% - Resultado: [2-2, 1-1]  (Significa: Tamanho-VezesQueAparece)

% TAREFA 3: Associar cada sublista à frequência do seu comprimento
% - O que faz: Cria pares grudando a "Raridade" (Frequência) na frente da lista.
% - No Exemplo: Como [c] tem um tamanho que só aparece 1 vez, vira: 1-[c]
%               Como [a,b] tem um tamanho que aparece 2 vezes, vira: 2-[a,b]
% - Resultado: [2-[a,b], 1-[c], 2-[a,b]]

% TAREFA 4: Ordenar as sublistas pela frequência (ordem crescente)
% - O que faz: Ordena os pares da Tarefa 3 pelo número da frente (menor frequência primeiro).
%   Depois, apaga os números e deixa só as listas limpas.
% - Passo 1 (Ordenar): [1-[c], 2-[a,b], 2-[a,b]]  (O número 1 veio antes do 2)
% - Passo 2 (Limpar):  [[c], [a,b], [a,b]]

% TAREFA 5: Comparar os resultados obtidos por lsort/2 e lfsort/2
% - lsort/2:  Olha o tamanho bruto. Listas menores vêm primeiro.
% - lfsort/2: Olha a raridade. Listas com tamanhos que aparecem menos vezes vêm primeiro.

%-----------------------------------------------------------------------------------------------------------------

% Medir uma lista isolada
% Caso 1 (base): a lista não tem elementos, lista vazia tem tamanho 0:
comprimento_de_uma_lista([], 0).

% Caso 2: a lista tem elementos
comprimento_de_uma_lista([_ | Cauda_da_Lista], Tamanho_Total) :- 
    comprimento_de_uma_lista(Cauda_da_Lista, Tamanho_do_Resto), 
    Tamanho_Total is Tamanho_do_Resto + 1.



%====================== TAREFA 1: O transformador da lista de listas
% Caso 1 (base): Se a lista de entrada for vazia [], a lista com os tamanhos também é vazia []
obter_tamanhos([], []).

% Caso 2: Se a lista tem sublistas dentro dela
obter_tamanhos([Primeira_Sublista | Resto_das_Sublistas], [Tamanho_Dela | Lista_com_os_Outros_Tamanhos]) :-
    comprimento_de_uma_lista(Primeira_Sublista, Tamanho_Dela),
    obter_tamanhos(Resto_das_Sublistas, Lista_com_os_Outros_Tamanhos).



%===================== TAREFA 2: Contar a frequência de cada tamanho da lista
% Se não há números para contar ([]), o mapa de frequências também fica vazio
calcular_frequencias([], []).

% Separamos o primeiro número da lista (Tamanho_Atual) e mandamos o Resto_dos_Tamanhos para a recursão.
calcular_frequencias([Tamanho_Atual | Resto_dos_Tamanhos], Mapa_Final) :-

    % O Prolog vai primeiro descobrir a frequência de todo o resto da lista e guardar em um Mapa_Provisorio.
    calcular_frequencias(Resto_dos_Tamanhos, Mapa_Provisorio),

    % Agora que o resto está calculado, pegamos o Tamanho_Atual que guardamos lá no começo e jogamos ele dentro do mapa. Daqui vai sair o nosso Mapa_Final.
    incrementar_ou_inserir(Tamanho_Atual, Mapa_Provisorio, Mapa_Final).

% FUNÇÃO AUXILIAR: Adiciona +1 no contador ou cria um par novo
% Se o tamanho nunca apareceu antes, ele cria o primeiro par: Tamanho-1
incrementar_ou_inserir(Tamanho, [], [Tamanho-1]).

% Se o número que queremos inserir é igual ao que está na frente do mapa, ele entra nessa regra. Ele faz a conta: Quantidade_Nova is Quantidade_Antiga + 1 e atualiza o par.
incrementar_ou_inserir(Tamanho, [Tamanho-Quantidade_Antiga | Resto_do_Mapa], [Tamanho-Quantidade_Nova | Resto_do_Mapa]) :-
    Quantidade_Nova is Quantidade_Antiga + 1.

% Se o número for diferente do que está na frente do mapa, o Prolog ignora esse atual, deixa ele quieto na lista e pula para o próximo (Resto_do_Mapa) procurando o lugar certo para somar.
incrementar_ou_inserir(Tamanho, [Outro_Tamanho-Qtd | Resto_do_Mapa], [Outro_Tamanho-Qtd | Mapa_Atualizado]) :-
    Tamanho \= Outro_Tamanho,
    incrementar_ou_inserir(Tamanho, Resto_do_Mapa, Mapa_Atualizado).



%===================== TAREFA 3: Associar cada sublista à frequência do seu comprimento
% Caso Base: Se a lista original estiver vazia, o resultado final também é vazio
associar_frequencias([], _, []).

% Caso Geral: Processa a primeira sublista e depois faz o resto
associar_frequencias([Primeira_Sublista | Resto_das_Sublistas], Mapa_de_Frequencias, [Freq_Dela-Primeira_Sublista | Lista_Final_Com_Pares]) :-
    % 1. Descobre o tamanho dessa sublista específica
    comprimento_de_uma_lista(Primeira_Sublista, Tamanho_Dela),
    
    % 2. Procura esse tamanho no mapa para descobrir a frequência dele
    buscar_frequencia(Tamanho_Dela, Mapa_de_Frequencias, Freq_Dela),
    
    % 3. Manda rodar o resto das sublistas recursivamente
    associar_frequencias(Resto_das_Sublistas, Mapa_de_Frequencias, Lista_Final_Com_Pares).


% FUNÇÃO AUXILIAR: Varre o mapa procurando o número do tamanho e traz a quantidade
buscar_frequencia(Tamanho_Procurado, [Tamanho_Procurado-Quantidade | _], Quantidade).
buscar_frequencia(Tamanho_Procurado, [_ | Resto_do_Mapa], Quantidade) :-
    buscar_frequencia(Tamanho_Procurado, Resto_do_Mapa, Quantidade).



%===================== TAREFA 4: Ordenar as sublistas pela frequência (ordem crescente)
% Função Principal: Recebe os pares bagunçados e devolve as sublistas limpas e ordenadas
ordenar_por_frequencia(Lista_de_Pares_Baguncada, Lista_Final_Limpa) :-
    algoritmo_ordenacao(Lista_de_Pares_Baguncada, Lista_de_Pares_Ordenada),
    limpar_chaves_numericas(Lista_de_Pares_Ordenada, Lista_Final_Limpa).

% --- SUB-BLOCO A: O Algoritmo de Ordenação (Insertion Sort) ---
algoritmo_ordenacao([], []).
algoritmo_ordenacao([Par_Atual | Resto_dos_Pares], Lista_Ordenada) :-
    algoritmo_ordenacao(Resto_dos_Pares, Lista_Do_Resto_Ordenada),
    inserir_na_posicao_correta(Par_Atual, Lista_Do_Resto_Ordenada, Lista_Ordenada).

% --- SUB-BLOCO B: Encontrar o lugar certo de cada par ---
% Caso 1: Se a lista estiver vazia, o par fica nela mesma
inserir_na_posicao_correta(Par, [], [Par]).

% Caso 2: Se a frequência do Par_Novo for menor ou igual à do Par_Que_Ja_Estava, ele entra na frente!
inserir_na_posicao_correta(Freq_Nova-Sub_Nova, [Freq_Antiga-Sub_Antiga | Resto], [Freq_Nova-Sub_Nova, Freq_Antiga-Sub_Antiga | Resto]) :-
    Freq_Nova =< Freq_Antiga.

% Caso 3: Se a frequência for maior, ele pula para trás e tenta se encaixar no resto da lista
inserir_na_posicao_correta(Freq_Nova-Sub_Nova, [Freq_Antiga-Sub_Antiga | Resto], [Freq_Antiga-Sub_Antiga | Lista_Atualizada]) :-
    Freq_Nova > Freq_Antiga,
    inserir_na_posicao_correta(Freq_Nova-Sub_Nova, Resto, Lista_Atualizada).

% --- SUB-BLOCO C: Limpar os números e deixar só as listas ---
limpar_chaves_numericas([], []).
limpar_chaves_numericas([_Frequencia - Sublista | Resto_dos_Pares], [Sublista | Resto_das_Sublistas]) :-
    limpar_chaves_numericas(Resto_dos_Pares, Resto_das_Sublistas).



%======================== TAREFA 5: O Predicado Principal (lfsort/2)
lfsort(Lista_Original_de_Sublistas, Lista_Final_Ordenada) :-
    % Canos 1: Pega as sublistas e descobre os tamanhos brutos delas (Tarefa 1)
    obter_tamanhos(Lista_Original_de_Sublistas, Lista_de_Tamanhos),
    
    % Cano 2: Pega os tamanhos e monta o mapa de frequências (Tarefa 2)
    calcular_frequencias(Lista_de_Tamanhos, Mapa_de_Frequencias),
    
    % Cano 3: Junta a lista original com o mapa criando os pares Frequencia-Sublista (Tarefa 3)
    associar_frequencias(Lista_Original_de_Sublistas, Mapa_de_Frequencias, Lista_de_Pares_Baguncada),
    
    % Cano 4: Ordena tudo por frequência e limpa os números, cuspindo o resultado (Tarefa 4)
    ordenar_por_frequencia(Lista_de_Pares_Baguncada, Lista_Final_Ordenada).