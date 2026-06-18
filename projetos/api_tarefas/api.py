"""
API DE TAREFAS
Uma API REST completa para gerenciar tarefas, feita com Flask e SQLite.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
O QUE É UMA API?
  API significa "Interface de Programação de Aplicações".
  É basicamente um servidor que recebe pedidos e devolve dados.
  Pensa assim: o garçom de um restaurante é uma API —
  você (cliente) faz um pedido, o garçom leva para a cozinha
  (servidor) e traz de volta o resultado (dados).

O QUE É REST?
  É um estilo de organizar esses pedidos usando o protocolo HTTP.
  Cada pedido tem um MÉTODO que diz o que você quer fazer:
    GET    → buscar dados        ("me dá a lista de tarefas")
    POST   → criar algo novo     ("cria essa nova tarefa")
    PUT    → atualizar tudo      ("substitui essa tarefa por completo")
    PATCH  → atualizar um campo  ("só muda o status desta tarefa")
    DELETE → apagar              ("apaga essa tarefa")

O QUE É FLASK?
  Um framework web minimalista para Python. Com poucas linhas
  você sobe um servidor HTTP que responde a requisições.

O QUE É SQLITE?
  Um banco de dados que vive em um único arquivo .db no seu
  computador. Não precisa instalar nada, não precisa de servidor.
  Perfeito para projetos pequenos e médios.

O QUE É JSON?
  É o formato de dados mais usado em APIs. Parece um dicionário
  Python, mas é texto puro — funciona em qualquer linguagem.
  Exemplo: {"id": 1, "titulo": "Estudar Python", "status": "pendente"}

ROTAS DISPONÍVEIS:
  GET    /tarefas          → lista todas as tarefas
  POST   /tarefas          → cria uma nova tarefa
  GET    /tarefas/<id>     → busca uma tarefa pelo ID
  PATCH  /tarefas/<id>     → atualiza campos de uma tarefa
  DELETE /tarefas/<id>     → apaga uma tarefa
  GET    /tarefas/resumo   → estatísticas gerais

INSTALAR:
  pip install flask

RODAR:
  python api.py

TESTAR (em outro terminal):
  curl http://localhost:5000/tarefas
  curl -X POST http://localhost:5000/tarefas \
       -H "Content-Type: application/json" \
       -d '{"titulo": "Estudar Flask"}'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sqlite3                          # banco de dados embutido no Python
from flask import Flask, request, jsonify, g
from datetime import datetime


# ─────────────────────────────────────────────────────────────
#  INICIALIZAÇÃO DO FLASK
#  Flask(__name__) cria a aplicação. O __name__ é uma variável
#  especial do Python que contém o nome do arquivo atual.
#  O Flask usa isso para saber onde estão os arquivos do projeto.
# ─────────────────────────────────────────────────────────────

app = Flask(__name__)
BANCO = "tarefas.db"


# ─────────────────────────────────────────────────────────────
#  BANCO DE DADOS
#
#  O que é "g" do Flask?
#  É um objeto especial que existe durante o tempo de vida de
#  UMA requisição. Quando a requisição termina, ele some.
#  Usamos ele para guardar a conexão com o banco — assim abrimos
#  a conexão uma vez por requisição e fechamos no final.
# ─────────────────────────────────────────────────────────────

def banco():
    """
    Retorna a conexão com o banco de dados para a requisição atual.
    Se ainda não abriu, abre agora e guarda no objeto 'g'.
    """
    if "db" not in g:
        g.db = sqlite3.connect(BANCO)

        # row_factory faz com que cada linha retornada seja um dicionário
        # Em vez de row[0], row[1]... você usa row["titulo"], row["status"]
        g.db.row_factory = sqlite3.Row

    return g.db


@app.teardown_appcontext
def fechar_banco(erro):
    """
    @app.teardown_appcontext é um DECORATOR.

    O que é um decorator?
    É uma função que "envolve" outra função para adicionar
    comportamento antes ou depois dela. O @ é a sintaxe do Python
    para aplicar um decorator.

    Aqui: teardown_appcontext diz ao Flask para chamar fechar_banco()
    automaticamente ao final de cada requisição — mesmo que dê erro.
    """
    db = g.pop("db", None)   # remove do 'g' e retorna o valor
    if db:
        db.close()


def criar_tabela():
    """
    Cria a tabela de tarefas no banco se ela ainda não existir.
    "IF NOT EXISTS" torna isso seguro de chamar várias vezes.

    O que é SQL?
    É a linguagem para falar com bancos de dados relacionais.
    CREATE TABLE cria uma tabela, como uma planilha com colunas definidas.

    Tipos de coluna usados:
      INTEGER PRIMARY KEY AUTOINCREMENT → número inteiro gerado automaticamente
      TEXT NOT NULL                     → texto obrigatório
      TEXT DEFAULT 'valor'              → texto com valor padrão
      CHECK(x IN ('a','b'))             → só aceita esses valores
    """
    db = sqlite3.connect(BANCO)
    db.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT    NOT NULL,
            descricao   TEXT    DEFAULT '',
            prioridade  TEXT    DEFAULT 'media'   CHECK(prioridade IN ('baixa', 'media', 'alta')),
            status      TEXT    DEFAULT 'pendente' CHECK(status IN ('pendente', 'em_andamento', 'concluida')),
            criada_em   TEXT    NOT NULL,
            atualizada  TEXT    NOT NULL
        )
    """)
    db.commit()
    db.close()


# ─────────────────────────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────────────────────

def agora():
    """Retorna a data e hora atual no formato ISO 8601 (padrão internacional)."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def erro(mensagem, codigo):
    """
    Retorna uma resposta JSON de erro padronizada.

    jsonify() converte um dicionário Python em uma resposta HTTP
    com o cabeçalho Content-Type: application/json.
    O segundo valor da tupla (codigo) é o status HTTP:
      200 → OK
      201 → Criado com sucesso
      400 → Requisição inválida (erro do cliente)
      404 → Não encontrado
    """
    return jsonify({"erro": mensagem}), codigo


# ─────────────────────────────────────────────────────────────
#  ROTAS (ENDPOINTS)
#
#  O que é uma rota?
#  É a URL que o cliente acessa. Cada rota está associada a uma
#  função Python que o Flask chama quando recebe aquele pedido.
#
#  @app.route("/tarefas", methods=["GET"]) é um decorator que
#  diz: "quando chegarem requisições GET para /tarefas, chame
#  esta função".
# ─────────────────────────────────────────────────────────────


# ── GET /tarefas → lista todas ──────────────────────────────
@app.route("/tarefas", methods=["GET"])
def listar():
    """
    Lista todas as tarefas. Aceita filtros opcionais via query string.

    O que é query string?
    É a parte da URL depois do '?'. Exemplo:
    /tarefas?status=pendente&prioridade=alta
    request.args.get("status") pega o valor "pendente" desse exemplo.
    """
    db = banco()

    # Montamos a query SQL dinamicamente dependendo dos filtros
    # Usamos "WHERE 1=1" como truque: sempre verdadeiro,
    # assim podemos ir adicionando "AND ..." sem se preocupar
    # se é o primeiro filtro ou não.
    query  = "SELECT * FROM tarefas WHERE 1=1"
    params = []  # lista de valores para substituir os '?' na query

    # Por que não colocamos o valor direto na string SQL?
    # Ex: f"WHERE status = '{status}'" é PERIGOSO — SQL Injection!
    # Se o usuário digitar ' OR '1'='1, quebra o banco.
    # Usando '?' e params, o SQLite escapa os valores automaticamente.

    status     = request.args.get("status")
    prioridade = request.args.get("prioridade")
    busca      = request.args.get("busca")

    if status:
        query += " AND status = ?"
        params.append(status)

    if prioridade:
        query += " AND prioridade = ?"
        params.append(prioridade)

    if busca:
        # LIKE com % é a busca por texto parcial do SQL
        # '%python%' encontra qualquer texto que contenha "python"
        query += " AND (titulo LIKE ? OR descricao LIKE ?)"
        params.extend([f"%{busca}%", f"%{busca}%"])

    query += " ORDER BY criada_em DESC"

    linhas  = db.execute(query, params).fetchall()
    tarefas = [dict(linha) for linha in linhas]  # converte Row em dict

    return jsonify({"tarefas": tarefas, "total": len(tarefas)})


# ── POST /tarefas → cria uma nova ───────────────────────────
@app.route("/tarefas", methods=["POST"])
def criar():
    """
    Cria uma nova tarefa com os dados enviados no corpo da requisição.

    O corpo da requisição vem em JSON. request.get_json() faz o parse
    (converte a string JSON para um dicionário Python).
    silent=True evita erro se o corpo não for JSON válido.
    """
    dados = request.get_json(silent=True)

    if not dados:
        return erro("Envie um JSON no corpo da requisição.", 400)

    titulo = dados.get("titulo", "").strip()
    if not titulo:
        return erro("O campo 'titulo' é obrigatório.", 400)

    prioridade = dados.get("prioridade", "media")
    if prioridade not in ("baixa", "media", "alta"):
        return erro("prioridade deve ser 'baixa', 'media' ou 'alta'.", 400)

    ts = agora()
    db = banco()

    # INSERT adiciona uma nova linha na tabela
    # cursor.lastrowid retorna o ID gerado automaticamente (AUTOINCREMENT)
    cursor = db.execute(
        """INSERT INTO tarefas (titulo, descricao, prioridade, status, criada_em, atualizada)
           VALUES (?, ?, ?, 'pendente', ?, ?)""",
        (titulo, dados.get("descricao", ""), prioridade, ts, ts)
    )
    db.commit()

    nova = dict(db.execute("SELECT * FROM tarefas WHERE id = ?", (cursor.lastrowid,)).fetchone())

    # 201 Created é o status correto para criação de recursos
    return jsonify({"mensagem": "Tarefa criada!", "tarefa": nova}), 201


# ── GET /tarefas/<id> → busca uma ───────────────────────────
@app.route("/tarefas/<int:id>", methods=["GET"])
def buscar(id):
    """
    Busca uma tarefa pelo ID.

    <int:id> na rota diz ao Flask para capturar esse segmento
    da URL como um inteiro e passar para a função como parâmetro.
    Ex: GET /tarefas/5 → id = 5
    """
    linha = banco().execute("SELECT * FROM tarefas WHERE id = ?", (id,)).fetchone()

    if linha is None:
        return erro(f"Tarefa {id} não encontrada.", 404)

    return jsonify(dict(linha))


# ── PATCH /tarefas/<id> → atualiza campos ───────────────────
@app.route("/tarefas/<int:id>", methods=["PATCH"])
def atualizar(id):
    """
    Atualiza apenas os campos enviados na requisição.

    Diferença entre PUT e PATCH:
      PUT   → você manda TUDO, substitui o registro inteiro
      PATCH → você manda só o que quer mudar, o resto fica igual

    Ex: PATCH com {"status": "concluida"} só muda o status.
    """
    db    = banco()
    linha = db.execute("SELECT * FROM tarefas WHERE id = ?", (id,)).fetchone()

    if linha is None:
        return erro(f"Tarefa {id} não encontrada.", 404)

    dados = request.get_json(silent=True)
    if not dados:
        return erro("Envie um JSON no corpo da requisição.", 400)

    # Campos que podem ser atualizados
    permitidos = ("titulo", "descricao", "prioridade", "status")

    # Monta o SET do SQL dinamicamente — só com os campos enviados
    partes  = []   # ex: ["titulo = ?", "status = ?"]
    valores = []   # valores correspondentes

    for campo in permitidos:
        if campo in dados:
            partes.append(f"{campo} = ?")
            valores.append(dados[campo])

    if not partes:
        return erro("Nenhum campo válido para atualizar.", 400)

    partes.append("atualizada = ?")
    valores.append(agora())
    valores.append(id)

    db.execute(f"UPDATE tarefas SET {', '.join(partes)} WHERE id = ?", valores)
    db.commit()

    atualizada = dict(db.execute("SELECT * FROM tarefas WHERE id = ?", (id,)).fetchone())
    return jsonify({"mensagem": "Tarefa atualizada!", "tarefa": atualizada})


# ── DELETE /tarefas/<id> → apaga ────────────────────────────
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def apagar(id):
    """Apaga uma tarefa pelo ID."""
    db    = banco()
    linha = db.execute("SELECT * FROM tarefas WHERE id = ?", (id,)).fetchone()

    if linha is None:
        return erro(f"Tarefa {id} não encontrada.", 404)

    db.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    db.commit()

    return jsonify({"mensagem": f"Tarefa {id} apagada."})


# ── GET /tarefas/resumo → estatísticas ──────────────────────
@app.route("/tarefas/resumo", methods=["GET"])
def resumo():
    """
    Retorna estatísticas gerais das tarefas.

    CASE WHEN é o "if/else" do SQL:
      SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END)
      → conta 1 para cada linha com status pendente, 0 para o resto
      → a soma é a contagem de tarefas pendentes
    """
    linha = banco().execute("""
        SELECT
            COUNT(*)                                                      AS total,
            SUM(CASE WHEN status = 'pendente'     THEN 1 ELSE 0 END)     AS pendentes,
            SUM(CASE WHEN status = 'em_andamento' THEN 1 ELSE 0 END)     AS em_andamento,
            SUM(CASE WHEN status = 'concluida'    THEN 1 ELSE 0 END)     AS concluidas,
            SUM(CASE WHEN prioridade = 'alta'     THEN 1 ELSE 0 END)     AS alta_prioridade
        FROM tarefas
    """).fetchone()

    total     = linha["total"] or 0
    concluidas = linha["concluidas"] or 0

    return jsonify({
        "total":           total,
        "pendentes":       linha["pendentes"],
        "em_andamento":    linha["em_andamento"],
        "concluidas":      concluidas,
        "alta_prioridade": linha["alta_prioridade"],
        # Taxa de conclusão: porcentagem de tarefas já finalizadas
        "taxa_conclusao":  round(concluidas / total * 100, 1) if total > 0 else 0,
    })


# ── Tratamento de erros globais ──────────────────────────────
@app.errorhandler(404)
def nao_encontrado(e):
    return erro("Rota não encontrada.", 404)

@app.errorhandler(405)
def metodo_invalido(e):
    return erro("Método HTTP não permitido para esta rota.", 405)


# ─────────────────────────────────────────────────────────────
#  ENTRADA DO PROGRAMA
#
#  if __name__ == "__main__" → este bloco só roda quando você
#  executa o arquivo diretamente (python api.py).
#  Se outro arquivo importar este, o bloco é ignorado.
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    criar_tabela()
    print("\n  🚀 API rodando em http://127.0.0.1:5000")
    print("\n  Rotas disponíveis:")
    print("    GET    /tarefas")
    print("    POST   /tarefas")
    print("    GET    /tarefas/<id>")
    print("    PATCH  /tarefas/<id>")
    print("    DELETE /tarefas/<id>")
    print("    GET    /tarefas/resumo\n")

    # debug=True → reinicia o servidor automaticamente quando você
    # salva o arquivo. Ótimo para desenvolvimento, nunca use em produção.
    app.run(debug=True)
