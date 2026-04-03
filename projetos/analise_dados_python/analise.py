"""
ANÁLISE DE DADOS — RELATÓRIO DE FELICIDADE MUNDIAL
Análise completa de um dataset real com estatísticas e gráficos.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
O QUE É ANÁLISE DE DADOS?
  É o processo de examinar um conjunto de dados para encontrar
  padrões, tirar conclusões e contar uma história com números.
  É uma das habilidades mais pedidas em vagas de TI hoje em dia.

O QUE É UM DATAFRAME?
  É a estrutura principal do pandas — pensa nele como uma planilha
  do Excel em memória. Tem linhas (cada observação) e colunas
  (cada variável). Você pode filtrar, agrupar, calcular e plotar.

O QUE É CORRELAÇÃO?
  Mede o quanto duas variáveis se movem juntas.
    +1.0 → quando uma sobe, a outra sempre sobe junto
     0.0 → sem relação nenhuma
    -1.0 → quando uma sobe, a outra sempre cai
  Ex: PIB e felicidade têm correlação positiva alta (~0.8)

O QUE É SEABORN?
  Uma biblioteca de visualização construída em cima do matplotlib.
  Gera gráficos estatísticos mais bonitos com menos código.
  Ideal para heatmaps, boxplots e scatter plots com agrupamentos.

DATASET:
  World Happiness Report — ranking de felicidade de 150+ países
  baseado em: PIB per capita, suporte social, expectativa de vida,
  liberdade, generosidade e percepção de corrupção.

  Baixe em: https://kaggle.com/datasets/unsdsn/world-happiness
  Ou rode o script — ele gera dados de exemplo automaticamente.

INSTALAR:
  pip install pandas matplotlib seaborn numpy

RODAR:
  python analise.py             → análise completa, salva gráficos
  python analise.py --mostrar   → também abre os gráficos na tela
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns     # visualizações estatísticas mais bonitas
import numpy as np        # operações numéricas (médias, regressão, etc.)
import argparse
from pathlib import Path


# ─────────────────────────────────────────────────────────────
#  CONFIGURAÇÕES VISUAIS
#
#  sns.set_theme() aplica um tema global para todos os gráficos.
#  "whitegrid" → fundo branco com grade cinza
#  font_scale  → aumenta o tamanho de todos os textos
# ─────────────────────────────────────────────────────────────

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
plt.rcParams["figure.dpi"] = 130   # resolução dos gráficos (pontos por polegada)

PASTA_GRAFICOS = Path("graficos")
PASTA_GRAFICOS.mkdir(exist_ok=True)   # cria a pasta se não existir


# ─────────────────────────────────────────────────────────────
#  GERAR DADOS DE EXEMPLO
#  Cria um dataset realista se o arquivo real não estiver disponível.
# ─────────────────────────────────────────────────────────────

def gerar_dados_exemplo():
    """
    Gera dados fictícios mas com relações realistas entre as variáveis.
    np.random.seed(42) garante que os dados sejam sempre os mesmos
    a cada execução — isso se chama "reprodutibilidade".
    """
    np.random.seed(42)
    n = 155

    paises = [
        "Finlândia", "Dinamarca", "Islândia", "Suíça", "Holanda",
        "Noruega", "Suécia", "Nova Zelândia", "Áustria", "Austrália",
        "Israel", "Alemanha", "Canadá", "Irlanda", "Costa Rica",
        "Reino Unido", "República Checa", "Bélgica", "França", "Bahrain",
        "Brasil", "México", "Tailândia", "Filipinas", "China",
        "Japão", "Coreia do Sul", "Espanha", "Chile", "Itália",
        "Polônia", "Ucrânia", "Rússia", "Peru", "Bangladesh",
        "Nepal", "Índia", "Etiópia", "Paquistão", "Nigéria",
        "Gana", "Quênia", "Egito", "Marrocos", "Zimbabwe",
        "Tanzânia", "Uganda", "Burundi", "Afeganistão", "Haiti",
    ] + [f"País_{i}" for i in range(n - 50)]
    paises = paises[:n]

    # PIB distribuído uniformemente em escala logarítmica
    pib = np.random.uniform(6.5, 11.5, n)

    # Felicidade correlacionada com PIB + ruído aleatório
    # Isso simula a relação real: países mais ricos tendem a ser mais felizes,
    # mas nem sempre — o ruído representa outros fatores
    felicidade = 0.6 * (pib - 6.5) / 5.0 * 5 + 2.5 + np.random.normal(0, 0.5, n)
    felicidade = np.clip(felicidade, 2.0, 8.0)   # limita entre 2 e 8

    suporte_social  = np.clip(0.7 * felicidade / 8 + np.random.uniform(0.3, 0.6, n), 0, 1)
    expectativa_vida = np.clip(40 + 0.5 * felicidade * 7 + np.random.normal(0, 5, n), 40, 80)
    liberdade       = np.clip(np.random.uniform(0.2, 1.0, n), 0, 1)
    generosidade    = np.clip(np.random.normal(0.1, 0.2, n), -0.3, 0.7)
    corrupcao       = np.clip(np.random.uniform(0.0, 0.5, n), 0, 1)

    regioes = np.random.choice([
        "Europa Ocidental", "América do Norte", "América Latina",
        "Europa Oriental", "Ásia Oriental", "Sul da Ásia",
        "Sudeste Asiático", "África Subsaariana", "Oriente Médio",
    ], n)

    df = pd.DataFrame({
        "Pais":              paises,
        "Regiao":            regioes,
        "Felicidade":        felicidade.round(3),
        "PIB_per_Capita":    pib.round(3),
        "Suporte_Social":    suporte_social.round(3),
        "Expectativa_Vida":  expectativa_vida.round(3),
        "Liberdade":         liberdade.round(3),
        "Generosidade":      generosidade.round(3),
        "Corrupcao":         corrupcao.round(3),
    })

    caminho = Path("felicidade.csv")
    df.to_csv(caminho, index=False)
    print(f"  ✅ Dados de exemplo criados: {len(df)} países → {caminho}\n")
    return df


# ─────────────────────────────────────────────────────────────
#  CARREGAR E LIMPAR DADOS
# ─────────────────────────────────────────────────────────────

def carregar():
    """Carrega o CSV ou gera dados de exemplo."""
    caminho = Path("felicidade.csv")
    if caminho.exists():
        df = pd.read_csv(caminho)
        print(f"  Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
    else:
        print("  Arquivo não encontrado — gerando dados de exemplo...")
        df = gerar_dados_exemplo()
    return df


def limpar(df):
    """
    Limpa problemas comuns em datasets reais:
    - Linhas sem o valor principal (Felicidade)
    - Valores ausentes em outras colunas (preenchidos com a mediana)
    - Países duplicados (mantém o mais recente)

    O que é mediana?
    É o valor do meio quando você ordena todos os valores.
    Diferente da média, ela não é afetada por valores extremos.
    Ex: [1, 2, 3, 100] → média = 26,5 | mediana = 2,5
    Usamos a mediana para preencher valores ausentes porque é
    mais robusta a outliers (valores muito fora do padrão).
    """
    antes = len(df)

    # dropna remove linhas onde a coluna Felicidade está vazia
    df = df.dropna(subset=["Felicidade"])

    # Preenche valores ausentes nas colunas numéricas com a mediana
    numericas = df.select_dtypes(include="number").columns
    for col in numericas:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    print(f"  Limpeza: {antes} → {len(df)} linhas\n")
    return df.reset_index(drop=True)


# ─────────────────────────────────────────────────────────────
#  ANÁLISE ESTATÍSTICA
# ─────────────────────────────────────────────────────────────

def estatisticas(df):
    """Imprime estatísticas descritivas e correlações."""

    print("=" * 55)
    print("  ESTATÍSTICAS — FELICIDADE MUNDIAL")
    print("=" * 55)

    score = df["Felicidade"]
    print(f"\n  Países analisados : {len(df)}")
    print(f"  Média de felicidade: {score.mean():.2f}")
    print(f"  Mediana            : {score.median():.2f}")
    print(f"  Desvio padrão      : {score.std():.2f}")

    # O que é desvio padrão?
    # Mede o quanto os valores se afastam da média.
    # Um desvio alto = os países variam muito entre si.
    # Um desvio baixo = os países são parecidos em felicidade.

    print(f"\n  5 países mais felizes:")
    for _, r in df.nlargest(5, "Felicidade").iterrows():
        print(f"    {r['Pais']:<25} {r['Felicidade']:.2f}")

    print(f"\n  5 países menos felizes:")
    for _, r in df.nsmallest(5, "Felicidade").iterrows():
        print(f"    {r['Pais']:<25} {r['Felicidade']:.2f}")

    # Correlação de cada fator com a felicidade
    fatores = ["PIB_per_Capita", "Suporte_Social", "Expectativa_Vida",
               "Liberdade", "Generosidade", "Corrupcao"]
    fatores = [f for f in fatores if f in df.columns]

    print(f"\n  Correlação com Felicidade:")
    correlacoes = df[fatores].corrwith(df["Felicidade"]).sort_values(ascending=False)
    for fator, corr in correlacoes.items():
        barra = "█" * int(abs(corr) * 20)
        sinal = "+" if corr >= 0 else "-"
        print(f"    {fator:<22} {sinal}{abs(corr):.3f}  {barra}")
    print()


# ─────────────────────────────────────────────────────────────
#  GRÁFICOS
# ─────────────────────────────────────────────────────────────

def salvar(fig, nome, mostrar):
    """Salva o gráfico como PNG e opcionalmente exibe na tela."""
    caminho = PASTA_GRAFICOS / nome
    fig.savefig(caminho, bbox_inches="tight")
    print(f"  ✅ {caminho}")
    if mostrar:
        plt.show()
    plt.close()


def grafico_ranking(df, mostrar):
    """
    Gráfico de barras horizontal: top 15 e bottom 15 países.
    Dois gráficos lado a lado usando subplots.

    O que é subplots?
    É dividir a figura em múltiplos painéis. fig, axes = plt.subplots(1, 2)
    cria 1 linha e 2 colunas de gráficos — dois painéis lado a lado.
    axes[0] é o da esquerda, axes[1] é o da direita.
    """
    top    = df.nlargest(15, "Felicidade")
    bottom = df.nsmallest(15, "Felicidade")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle("Ranking de Felicidade Mundial", fontsize=14, fontweight="bold")

    for ax, dados, titulo, cor in [
        (axes[0], top,    "Top 15 Mais Felizes",   "#2ECC71"),
        (axes[1], bottom, "Bottom 15 Menos Felizes","#E74C3C"),
    ]:
        barras = ax.barh(dados["Pais"], dados["Felicidade"], color=cor, alpha=0.85)
        ax.set_title(titulo, fontweight="bold")
        ax.set_xlabel("Índice de Felicidade")
        ax.invert_yaxis()   # coloca o maior no topo

        # Adiciona o valor no final de cada barra
        for b, v in zip(barras, dados["Felicidade"]):
            ax.text(b.get_width() + 0.05,
                    b.get_y() + b.get_height() / 2,
                    f"{v:.2f}", va="center", fontsize=9)

        ax.set_xlim(0, 9)
        sns.despine(ax=ax)   # remove as bordas desnecessárias do gráfico

    plt.tight_layout()
    salvar(fig, "01_ranking_paises.png", mostrar)


def grafico_pib_vs_felicidade(df, mostrar):
    """
    Scatter plot: PIB per capita vs índice de felicidade.
    Cada ponto é um país. Cor = região geográfica.

    O que é scatter plot?
    É um gráfico de dispersão onde cada ponto representa uma
    observação. Ótimo para ver a relação entre duas variáveis.

    Linha de tendência:
    np.polyfit(x, y, 1) calcula os coeficientes de uma reta
    que melhor se ajusta aos pontos — isso se chama regressão linear.
    np.poly1d transforma esses coeficientes em uma função f(x).
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # hue="Regiao" colore cada ponto de acordo com a região do país
    # size="Expectativa_Vida" varia o tamanho do ponto com a expectativa de vida
    sns.scatterplot(
        data=df,
        x="PIB_per_Capita",
        y="Felicidade",
        hue="Regiao" if "Regiao" in df.columns else None,
        size="Expectativa_Vida" if "Expectativa_Vida" in df.columns else None,
        sizes=(40, 200),
        alpha=0.75,
        ax=ax,
    )

    # Linha de tendência (regressão linear)
    z = np.polyfit(df["PIB_per_Capita"], df["Felicidade"], 1)
    p = np.poly1d(z)   # p agora é uma função: p(x) = z[0]*x + z[1]
    x_linha = np.linspace(df["PIB_per_Capita"].min(), df["PIB_per_Capita"].max(), 100)
    ax.plot(x_linha, p(x_linha), "k--", alpha=0.4, linewidth=1.5, label="Tendência")

    # Anota os 5 países mais felizes com seus nomes no gráfico
    for _, r in df.nlargest(5, "Felicidade").iterrows():
        ax.annotate(r["Pais"],
                    xy=(r["PIB_per_Capita"], r["Felicidade"]),
                    xytext=(5, 5), textcoords="offset points",
                    fontsize=8, color="#333")

    ax.set_title("PIB per Capita vs Felicidade", fontsize=14, fontweight="bold")
    ax.set_xlabel("Log do PIB per Capita")
    ax.set_ylabel("Índice de Felicidade")
    ax.legend(loc="lower right", fontsize=8)
    sns.despine()

    salvar(fig, "02_pib_vs_felicidade.png", mostrar)


def grafico_heatmap(df, mostrar):
    """
    Heatmap de correlações entre todas as variáveis numéricas.

    O que é um heatmap?
    É uma tabela onde os números viram cores — ótimo para enxergar
    padrões em uma matriz de correlações. Verde = positivo,
    vermelho = negativo, amarelo = próximo de zero.

    df.corr() calcula a correlação entre todos os pares de colunas.
    np.triu() cria uma máscara triangular para esconder a metade
    de cima da matriz (que é idêntica à de baixo — é simétrica).
    """
    fatores = ["Felicidade", "PIB_per_Capita", "Suporte_Social",
               "Expectativa_Vida", "Liberdade", "Generosidade", "Corrupcao"]
    fatores = [f for f in fatores if f in df.columns]

    matriz = df[fatores].corr()

    # Mascara a metade superior para não mostrar dados redundantes
    mascara = np.triu(np.ones_like(matriz, dtype=bool))

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        matriz,
        mask=mascara,
        annot=True,     # mostra os números dentro das células
        fmt=".2f",      # 2 casas decimais
        cmap="RdYlGn",  # vermelho → amarelo → verde
        center=0,       # centraliza o mapa de cores no zero
        vmin=-1, vmax=1,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title("Mapa de Correlações", fontsize=14, fontweight="bold")
    plt.tight_layout()
    salvar(fig, "03_heatmap_correlacoes.png", mostrar)


def grafico_por_regiao(df, mostrar):
    """
    Boxplot: distribuição de felicidade por região geográfica.

    O que é um boxplot?
    Mostra 5 informações de uma vez para cada grupo:
      - A linha do meio = mediana
      - A caixa = onde estão 50% dos dados (quartis 25% e 75%)
      - Os "bigodes" = onde estão os demais dados
      - Os pontos soltos = outliers (valores fora do padrão)
    """
    if "Regiao" not in df.columns:
        return

    # Ordena as regiões pela mediana de felicidade (da maior para menor)
    ordem = (df.groupby("Regiao")["Felicidade"]
               .median()
               .sort_values(ascending=False)
               .index.tolist())

    fig, ax = plt.subplots(figsize=(13, 6))
    sns.boxplot(data=df, x="Regiao", y="Felicidade",
                order=ordem, palette="Set3", ax=ax)

    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.set_title("Felicidade por Região", fontsize=14, fontweight="bold")
    ax.set_xlabel("")
    sns.despine()
    plt.tight_layout()
    salvar(fig, "04_felicidade_por_regiao.png", mostrar)


def grafico_fatores(df, mostrar):
    """
    Gráfico de barras horizontal: qual fator mais influencia a felicidade?
    Barras verdes = correlação positiva, vermelhas = negativa.
    """
    fatores = ["PIB_per_Capita", "Suporte_Social", "Expectativa_Vida",
               "Liberdade", "Generosidade", "Corrupcao"]
    fatores = [f for f in fatores if f in df.columns]

    correlacoes = df[fatores].corrwith(df["Felicidade"]).sort_values()
    cores = ["#E74C3C" if v < 0 else "#2ECC71" for v in correlacoes.values]

    fig, ax = plt.subplots(figsize=(9, 5))
    barras = ax.barh(correlacoes.index, correlacoes.values, color=cores, alpha=0.85)

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Correlação com Felicidade")
    ax.set_title("O Que Mais Influencia a Felicidade?", fontsize=14, fontweight="bold")

    for b, v in zip(barras, correlacoes.values):
        xpos  = b.get_width() + (0.01 if v >= 0 else -0.01)
        alinha = "left" if v >= 0 else "right"
        ax.text(xpos, b.get_y() + b.get_height() / 2,
                f"{v:.3f}", va="center", ha=alinha, fontsize=9)

    sns.despine()
    plt.tight_layout()
    salvar(fig, "05_fatores_felicidade.png", mostrar)


# ─────────────────────────────────────────────────────────────
#  ENTRADA DO PROGRAMA
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Análise do Relatório de Felicidade Mundial.")
    parser.add_argument("--mostrar", action="store_true",
                        help="Abre os gráficos na tela (além de salvar)")
    args = parser.parse_args()

    print("\n" + "=" * 55)
    print("  🌍 ANÁLISE — FELICIDADE MUNDIAL")
    print("=" * 55 + "\n")

    df = carregar()
    df = limpar(df)

    estatisticas(df)

    print("  Gerando gráficos...")
    grafico_ranking(df, args.mostrar)
    grafico_pib_vs_felicidade(df, args.mostrar)
    grafico_heatmap(df, args.mostrar)
    grafico_por_regiao(df, args.mostrar)
    grafico_fatores(df, args.mostrar)

    print(f"\n  Todos os gráficos salvos em ./{PASTA_GRAFICOS}/\n")
