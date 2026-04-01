# 🕷️ Monitor de Preços

Rastreia preços de produtos na web automaticamente e envia alertas por e-mail quando o preço cai abaixo do seu alvo.

## Como usar

```bash
pip install requests beautifulsoup4 schedule pandas

# Verificar uma vez agora
python scraper.py

# Rodar automaticamente a cada 6 horas
python scraper.py --agendar 6

# Ver histórico de preços
python scraper.py --historico
```

## Configurar e-mail

```bash
export EMAIL_REMETENTE="seu@gmail.com"
export EMAIL_SENHA="sua_senha_de_app"     # não use a senha normal!
export EMAIL_DESTINATARIO="seu@gmail.com"
```

> Senha de App: Conta Google → Segurança → Verificação em 2 etapas → Senhas de app

## Adicionar produtos

Edite a lista `PRODUTOS` no arquivo:
```python
{
    "nome":    "Nome do produto",
    "url":     "https://url-do-produto.com",
    "seletor": ".classe-do-preco",   # seletor CSS do elemento com o preço
    "alvo":    99.90,                # avisa se baixar desse valor
}
```

## Tecnologias
- **requests** — baixa o HTML das páginas
- **BeautifulSoup** — analisa o HTML e extrai os dados
- **pandas** — salva histórico de preços em CSV
- **smtplib** — envia e-mails via Gmail SMTP
- **schedule** — agenda verificações automáticas
