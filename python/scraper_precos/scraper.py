"""
MONITOR DE PREÇOS
Rastreia o preço de produtos na web e avisa por e-mail quando cai.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
O QUE É WEB SCRAPING?
  É a prática de ler o HTML de um site com código e extrair
  informações específicas dele — como preço, título, estoque.
  Em vez de você abrir o site todo dia para checar o preço,
  o seu programa faz isso automaticamente.

COMO FUNCIONA NA PRÁTICA:
  1. requests.get(url) baixa o HTML da página (como um navegador,
     mas sem renderizar nada visualmente)
  2. BeautifulSoup analisa esse HTML e monta uma árvore de elementos
  3. soup.select(".preco") encontra os elementos pelo seletor CSS
  4. Extraímos o texto, limpamos, convertemos para número
  5. Comparamos com o preço alvo — se baixou, manda e-mail

O QUE É HTML?
  É a linguagem que descreve a estrutura de uma página web.
  Cada "pedaço" da página é um elemento com uma tag:
    <h1>Título</h1>
    <p class="preco">R$ 49,90</p>
  O seletor CSS ".preco" encontra elementos com class="preco".

O QUE É SMTP?
  É o protocolo (conjunto de regras) para enviar e-mails.
  Assim como o HTTP é para acessar sites, o SMTP é para e-mails.
  Usamos o servidor SMTP do Gmail para enviar os alertas.

SITE USADO NOS EXEMPLOS:
  books.toscrape.com → site gratuito feito para praticar scraping.
  Sem bloqueios, sem captcha, sem termos proibindo automação.

INSTALAR:
  pip install requests beautifulsoup4 schedule pandas

RODAR:
  python scraper.py               → roda uma vez agora
  python scraper.py --agendar 6  → roda a cada 6 horas
  python scraper.py --historico  → mostra histórico de preços
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import requests                   # faz requisições HTTP (baixa páginas web)
from bs4 import BeautifulSoup     # analisa HTML e permite buscar elementos
import pandas as pd               # salva e carrega histórico de preços em CSV
import smtplib                    # envia e-mails via protocolo SMTP
import schedule                   # agenda tarefas para rodar periodicamente
import time                       # pausar o programa entre verificações
import os
import argparse
from email.mime.text import MIMEText          # monta o corpo do e-mail
from email.mime.multipart import MIMEMultipart # monta e-mail com múltiplas partes
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────────────────────
#  CONFIGURAÇÕES
#  Preencha com seus dados antes de rodar.
# ─────────────────────────────────────────────────────────────

# Credenciais de e-mail
# Dica: use variáveis de ambiente em vez de deixar senha no código.
# No terminal: export EMAIL_REMETENTE="seu@gmail.com"
# Depois, os.getenv("EMAIL_REMETENTE") pega esse valor.
EMAIL_REMETENTE  = os.getenv("EMAIL_REMETENTE",  "seu_email@gmail.com")
EMAIL_SENHA      = os.getenv("EMAIL_SENHA",       "sua_senha_de_app")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO", "seu_email@gmail.com")

HISTORICO = Path("historico_precos.csv")

# ─────────────────────────────────────────────────────────────
#  PRODUTOS MONITORADOS
#  Adicione quantos quiser. O seletor CSS diz onde está o preço.
#
#  Como descobrir o seletor?
#  Abra o site no Chrome → clique com botão direito no preço →
#  "Inspecionar" → veja a tag e a classe do elemento.
# ─────────────────────────────────────────────────────────────

PRODUTOS = [
    {
        "nome":     "A Light in the Attic",
        "url":      "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "seletor":  ".price_color",   # seletor CSS do elemento com o preço
        "alvo":     60.0,             # avisa se o preço ficar abaixo disso
    },
    {
        "nome":     "Tipping the Velvet",
        "url":      "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
        "seletor":  ".price_color",
        "alvo":     55.0,
    },
]

# Headers simulam um navegador real — alguns sites bloqueiam
# requisições que não parecem vir de um navegador.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


# ─────────────────────────────────────────────────────────────
#  SCRAPING
# ─────────────────────────────────────────────────────────────

def baixar_pagina(url):
    """
    Baixa o HTML de uma URL e retorna um objeto BeautifulSoup.

    requests.get() faz uma requisição HTTP GET — o mesmo que
    seu navegador faz quando você digita um endereço.
    A resposta tem um campo .text com o HTML da página em texto.

    BeautifulSoup recebe esse texto e monta uma estrutura
    navegável — como um mapa do HTML — que você pode pesquisar.
    "html.parser" é o analisador padrão do Python, sem instalar nada extra.
    """
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=15)

        # raise_for_status() lança uma exceção se o servidor
        # retornou erro. Códigos 2xx = ok. 4xx/5xx = erro.
        # Ex: 404 = página não encontrada, 403 = acesso negado.
        resposta.raise_for_status()

        return BeautifulSoup(resposta.text, "html.parser")

    except requests.RequestException as e:
        print(f"    ❌ Falha ao acessar {url}: {e}")
        return None


def extrair_preco(soup, seletor):
    """
    Encontra o elemento com o preço usando um seletor CSS
    e converte o texto para número float.

    Seletores CSS mais comuns:
      ".nome-classe"  → elemento com aquela classe
      "#id"           → elemento com aquele id
      "tag"           → elemento HTML (h1, p, span...)
      "tag.classe"    → tag com aquela classe

    soup.select_one() retorna o primeiro elemento que bater,
    ou None se não encontrar nenhum.
    """
    elemento = soup.select_one(seletor)
    if not elemento:
        return None

    # get_text() extrai só o texto, sem as tags HTML
    # strip=True remove espaços das bordas
    texto = elemento.get_text(strip=True)

    # Remove tudo que não for dígito ou ponto
    # Converte "£51.77" ou "R$51,77" para "51.77"
    apenas_numeros = ""
    for caractere in texto:
        if caractere.isdigit() or caractere == ".":
            apenas_numeros += caractere

    try:
        return float(apenas_numeros)
    except ValueError:
        return None


def verificar_produto(produto):
    """
    Acessa a página do produto, extrai o preço e retorna
    um dicionário com os dados coletados.
    """
    print(f"  Verificando: {produto['nome']}")

    soup = baixar_pagina(produto["url"])
    if soup is None:
        return None

    preco = extrair_preco(soup, produto["seletor"])
    if preco is None:
        print(f"    ⚠  Não consegui extrair o preço.")
        return None

    alerta = preco < produto["alvo"]
    print(f"    Preço atual: {preco:.2f} | Alvo: {produto['alvo']:.2f} {'⚠️ ALERTA!' if alerta else '✅'}")

    return {
        "nome":      produto["nome"],
        "preco":     preco,
        "alvo":      produto["alvo"],
        "alerta":    alerta,
        "data":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ─────────────────────────────────────────────────────────────
#  HISTÓRICO
# ─────────────────────────────────────────────────────────────

def salvar_historico(resultado):
    """Adiciona uma linha ao CSV de histórico de preços."""
    df_novo = pd.DataFrame([resultado])

    if HISTORICO.exists():
        # pd.concat empilha dois DataFrames verticalmente
        df_antigo = pd.read_csv(HISTORICO)
        df = pd.concat([df_antigo, df_novo], ignore_index=True)
    else:
        df = df_novo

    df.to_csv(HISTORICO, index=False)


def mostrar_historico():
    """Exibe o histórico de preços de todos os produtos."""
    if not HISTORICO.exists():
        print("\n  Nenhum histórico encontrado. Rode o scraper primeiro.")
        return

    df = pd.read_csv(HISTORICO)

    print("\n── Histórico de Preços ──────────────────────────")
    for nome, grupo in df.groupby("nome"):
        print(f"\n  📦 {nome}")
        print(f"  {'Data':<22} {'Preço':>8} {'Alvo':>8}")
        print("  " + "─" * 42)
        for _, linha in grupo.iterrows():
            alerta = " ⚠️" if linha["alerta"] else ""
            print(f"  {linha['data']:<22} {linha['preco']:>8.2f} {linha['alvo']:>8.2f}{alerta}")


# ─────────────────────────────────────────────────────────────
#  ALERTA POR E-MAIL
# ─────────────────────────────────────────────────────────────

def enviar_email(alertas):
    """
    Envia um e-mail listando os produtos que baixaram de preço.

    Como funciona o SMTP com Python:
      1. Conectamos ao servidor SMTP do Gmail (smtp.gmail.com, porta 587)
      2. Chamamos starttls() para criptografar a conexão (TLS)
      3. Fazemos login com e-mail e senha de app
      4. Enviamos o e-mail montado com MIMEMultipart
      5. Fechamos a conexão

    O que é TLS?
      Transport Layer Security — criptografa a comunicação para
      que ninguém no meio do caminho consiga ler os dados.

    Senha de App do Gmail:
      Não use sua senha normal. Vá em: Conta Google → Segurança →
      Verificação em duas etapas → Senhas de app → Gerar uma.
    """
    if not alertas:
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🔔 Alerta de Preço — {len(alertas)} produto(s) abaixo do alvo!"
    msg["From"]    = EMAIL_REMETENTE
    msg["To"]      = EMAIL_DESTINATARIO

    # Corpo em texto simples (para e-mail clients sem suporte a HTML)
    corpo = f"Alerta de Preço — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    for r in alertas:
        corpo += f"• {r['nome']}\n"
        corpo += f"  Preço atual: {r['preco']:.2f}\n"
        corpo += f"  Seu alvo:    {r['alvo']:.2f}\n\n"

    msg.attach(MIMEText(corpo, "plain"))

    try:
        # "with" garante que a conexão seja fechada mesmo se der erro
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()                              # ativa criptografia
            servidor.login(EMAIL_REMETENTE, EMAIL_SENHA)    # autentica
            servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg.as_string())
        print(f"\n  ✅ E-mail enviado para {EMAIL_DESTINATARIO}")
    except Exception as e:
        print(f"\n  ❌ Falha ao enviar e-mail: {e}")
        print("     Verifique se está usando uma Senha de App do Gmail.")


# ─────────────────────────────────────────────────────────────
#  VERIFICAÇÃO PRINCIPAL
# ─────────────────────────────────────────────────────────────

def verificar_todos():
    """Verifica todos os produtos e envia alertas se necessário."""
    print(f"\n{'='*50}")
    print(f"  🕷  Verificando preços — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*50}")

    resultados = []
    for i, produto in enumerate(PRODUTOS):
        resultado = verificar_produto(produto)
        if resultado:
            salvar_historico(resultado)
            resultados.append(resultado)

        # Pausa educada entre requisições — não sobrecarrega o servidor
        if i < len(PRODUTOS) - 1:
            print("    Aguardando 3s...")
            time.sleep(3)

    alertas = [r for r in resultados if r["alerta"]]
    if alertas:
        enviar_email(alertas)
    else:
        print("\n  Nenhum preço abaixo do alvo no momento.")


# ─────────────────────────────────────────────────────────────
#  ENTRADA DO PROGRAMA
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitora preços e envia alertas.")
    parser.add_argument("--agendar",   type=int, default=None,
                        metavar="HORAS", help="Roda automaticamente a cada N horas")
    parser.add_argument("--historico", action="store_true",
                        help="Mostra o histórico de preços")
    args = parser.parse_args()

    if args.historico:
        mostrar_historico()

    elif args.agendar:
        print(f"\n  ⏰ Agendado para rodar a cada {args.agendar} hora(s). Ctrl+C para parar.\n")
        verificar_todos()

        # schedule.every(N).hours.do(func) registra uma tarefa recorrente
        schedule.every(args.agendar).hours.do(verificar_todos)

        while True:
            # run_pending() verifica se alguma tarefa agendada está na hora de rodar
            schedule.run_pending()
            time.sleep(60)   # checa a cada minuto

    else:
        verificar_todos()
