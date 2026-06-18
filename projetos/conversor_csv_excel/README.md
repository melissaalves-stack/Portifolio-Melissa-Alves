# 📊 Conversor CSV → Excel

Transforma qualquer CSV em planilha Excel com cabeçalho formatado, resumo estatístico e gráfico automático.

## Como usar

```bash
pip install pandas openpyxl

python conversor.py dados.csv
python conversor.py dados.csv --saida relatorio
```

## O que é gerado

| Aba | Conteúdo |
|-----|----------|
| **Dados** | Tabela com cabeçalho azul, linhas alternadas, filtro automático |
| **Resumo** | Estatísticas descritivas (média, mín, máx, desvio padrão) |
| **Gráfico** | Gráfico de barras da primeira coluna numérica |

## Tecnologias
- **pandas** — leitura do CSV, `describe()` para estatísticas
- **openpyxl** — formatação de células e criação de gráficos
