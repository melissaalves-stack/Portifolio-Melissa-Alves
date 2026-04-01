"""
CONTROLE DE GASTOS
Registra despesas e mostra um resumo com gráfico.

USO:
  python gastos.py

INSTALAR:
  pip install pandas matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

ARQUIVO = Path("gastos.csv")

CATEGORIAS = [
    "Alimentação", "Transporte", "Moradia", "Saúde",
    "Educação", "Lazer", "Roupas", "Outros",
]


def carregar():
    if ARQUIVO.exists():
        df = pd.read_csv(ARQUIVO)
        df["data"] = pd.to_datetime(df["data"])
        return df
    return pd.DataFrame(columns=["data", "valor", "categoria", "descricao"])


def salvar(df):
    df.to_csv(ARQUIVO, index=False)


def adicionar(df):
    print("\n── Novo gasto ───────────────────────────")

    while True:
        try:
            valor = float(input("  Valor (R$): ").replace(",", "."))
            if valor > 0:
                break
            print("  ⚠  Digite um valor maior que zero.")
        except ValueError:
            print("  ⚠  Número inválido. Ex: 25.50")

    print("\n  Categorias:")
    for i, cat in enumerate(CATEGORIAS, 1):
        print(f"    {i}. {cat}")

    while True:
        try:
            n = int(input("  Escolha: "))
            if 1 <= n <= len(CATEGORIAS):
                categoria = CATEGORIAS[n - 1]
                break
            print(f"  ⚠  Digite entre 1 e {len(CATEGORIAS)}")
        except ValueError:
            print("  ⚠  Digite um número.")

    descricao = input("  Descrição (opcional): ").strip() or categoria

    nova = pd.DataFrame([{
        "data":      datetime.now(),
        "valor":     round(valor, 2),
        "categoria": categoria,
        "descricao": descricao,
    }])

    # pd.concat empilha dois DataFrames — adiciona a nova linha ao existente
    df = pd.concat([df, nova], ignore_index=True)
    salvar(df)
    print(f"\n  ✅ R$ {valor:.2f} salvo em {categoria}.")
    return df


def resumo(df):
    if df.empty:
        print("\n  Nenhum gasto ainda.")
        return

    # groupby agrupa por categoria e soma os valores de cada grupo
    por_cat = df.groupby("categoria")["valor"].sum().sort_values(ascending=False)

    print("\n── Resumo por categoria ─────────────────")
    for cat, total in por_cat.items():
        print(f"  {cat:<15}  R$ {total:.2f}")
    print(f"  {'─'*28}")
    print(f"  {'TOTAL':<15}  R$ {df['valor'].sum():.2f}")


def ultimos(df, n=10):
    if df.empty:
        print("\n  Nenhum gasto ainda.")
        return

    recentes = df.sort_values("data", ascending=False).head(n)
    print(f"\n── Últimos {n} gastos ────────────────────")
    for _, r in recentes.iterrows():
        print(f"  {r['data'].strftime('%d/%m/%Y')}  R$ {r['valor']:>7.2f}  {r['categoria']:<15}  {r['descricao']}")


def grafico(df):
    if df.empty:
        print("\n  Nenhum dado para gerar gráfico.")
        return

    por_cat = df.groupby("categoria")["valor"].sum().sort_values()

    fig, ax = plt.subplots(figsize=(9, 5))
    barras = ax.barh(por_cat.index, por_cat.values, color="#4C72B0")

    # Adiciona o valor no final de cada barra
    for b, v in zip(barras, por_cat.values):
        ax.text(b.get_width() + por_cat.max() * 0.01,
                b.get_y() + b.get_height() / 2,
                f"R$ {v:.2f}", va="center", fontsize=10)

    ax.set_title("Gastos por Categoria", fontweight="bold")
    ax.set_xlabel("Total (R$)")
    ax.set_xlim(0, por_cat.max() * 1.3)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig("grafico_gastos.png", dpi=150)
    plt.show()
    print("\n  ✅ Gráfico salvo como grafico_gastos.png")


def main():
    print("╔══════════════════════════════════╗")
    print("║      💰 CONTROLE DE GASTOS       ║")
    print("╚══════════════════════════════════╝")

    df = carregar()
    print(f"\n  {len(df)} gasto(s) carregado(s).")

    while True:
        print("\n── Menu ─────────────────────────────────")
        print("  1. Adicionar gasto")
        print("  2. Ver resumo")
        print("  3. Ver últimos gastos")
        print("  4. Gerar gráfico")
        print("  5. Sair")

        op = input("\n  Escolha: ").strip()

        if op == "1":   df = adicionar(df)
        elif op == "2": resumo(df)
        elif op == "3": ultimos(df)
        elif op == "4": grafico(df)
        elif op == "5": print("\n  Até logo! 👋\n"); break
        else:           print("  ⚠  Opção inválida.")


if __name__ == "__main__":
    main()
