# 🌍 Análise de Dados — Felicidade Mundial

Análise completa do World Happiness Report com estatísticas descritivas, correlações e 5 gráficos — gera dados de exemplo automaticamente se não tiver o CSV.

## Como usar

```bash
pip install pandas matplotlib seaborn numpy

# Roda a análise e salva os gráficos em ./graficos/
python analise.py

# Também abre os gráficos na tela
python analise.py --mostrar
```

## Gráficos gerados

| Arquivo | O que mostra |
|---------|-------------|
| `01_ranking_paises.png` | Top 15 e Bottom 15 países |
| `02_pib_vs_felicidade.png` | Scatter com linha de tendência |
| `03_heatmap_correlacoes.png` | Correlação entre todas as variáveis |
| `04_felicidade_por_regiao.png` | Boxplot por região geográfica |
| `05_fatores_felicidade.png` | Qual fator mais influencia a felicidade |

## Dataset real

Baixe em: https://kaggle.com/datasets/unsdsn/world-happiness  
Salve como `felicidade.csv` na mesma pasta.  
Ou simplesmente rode — o script gera dados de exemplo automaticamente.

## Tecnologias
- **pandas** — carregar, limpar e calcular correlações
- **matplotlib** — base dos gráficos
- **seaborn** — heatmap, boxplot, scatter com agrupamento
- **numpy** — regressão linear, operações numéricas
