# ✅ API de Tarefas

API REST completa para gerenciar tarefas, feita com Flask e SQLite. Sem banco de dados externo — tudo em um arquivo `.db` local.

## Como rodar

```bash
pip install flask
python api.py
```

## Endpoints

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | `/tarefas` | Lista todas as tarefas |
| GET | `/tarefas?status=pendente` | Filtra por status |
| GET | `/tarefas?busca=python` | Busca por palavra |
| POST | `/tarefas` | Cria uma tarefa |
| GET | `/tarefas/<id>` | Busca uma tarefa |
| PATCH | `/tarefas/<id>` | Atualiza campos |
| DELETE | `/tarefas/<id>` | Apaga uma tarefa |
| GET | `/tarefas/resumo` | Estatísticas |

## Exemplos com curl

```bash
# Criar uma tarefa
curl -X POST http://localhost:5000/tarefas \
     -H "Content-Type: application/json" \
     -d '{"titulo": "Estudar Flask", "prioridade": "alta"}'

# Marcar como concluída
curl -X PATCH http://localhost:5000/tarefas/1 \
     -H "Content-Type: application/json" \
     -d '{"status": "concluida"}'

# Estatísticas
curl http://localhost:5000/tarefas/resumo
```

## Tecnologias
- **Flask** — servidor web e roteamento HTTP
- **SQLite** — banco de dados em arquivo (embutido no Python)
