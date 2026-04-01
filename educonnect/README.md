# 🧠 EduConnect – Plataforma de Educação Online

## 📘 Descrição do Projeto

O **EduConnect** é uma plataforma de ensino online desenvolvida como parte da **Atividade Prática – Ciclo Completo de Desenvolvimento de Software**.  
O sistema conecta **alunos, professores e gestores**, permitindo **criar cursos, assistir aulas em vídeo, realizar atividades avaliativas e emitir certificados digitais em PDF**.

---

## 🚀 Funcionalidades Principais

### 👩‍🎓 Aluno

- ✅ Cadastro e autenticação com senha criptografada
- ✅ Visualização de cursos disponíveis
- ✅ Matrícula e desmatrícula em cursos
- ✅ Acesso a aulas em vídeo (MP4, MOV, AVI, MKV, WEBM)
- ✅ Realização de atividades com questões de múltipla escolha
- ✅ Visualização de nota automática após submissão
- ✅ Download de certificados em PDF

### 👩‍🏫 Professor

- ✅ Cadastro e autenticação
- ✅ Gerenciamento de cursos atribuídos pelo gestor
- ✅ Criação de aulas com upload de vídeos
- ✅ Criação de atividades avaliativas
- ✅ Criação de questões de múltipla escolha (A-E)
- ✅ Visualização de submissões dos alunos
- ✅ Acompanhamento de desempenho (acertos/erros por questão)

### 🧑‍💼 Gestor

- ✅ Cadastro e autenticação
- ✅ Criação de novos cursos
- ✅ Edição de cursos (título, descrição)
- ✅ Atribuição de professores aos cursos
- ✅ Visualização de alunos matriculados
- ✅ Matricular alunos manualmente em cursos

---

## ⚙️ Arquitetura e Tecnologias

| Camada                 | Tecnologias                                               |
| ---------------------- | --------------------------------------------------------- |
| **Backend**            | Python 3.x, Flask, Flask-SQLAlchemy, Flask-Login          |
| **Frontend**           | HTML5, CSS3, JavaScript (HTMX para interações AJAX)       |
| **Banco de Dados**     | SQLite (desenvolvimento)                                  |
| **Autenticação**       | Flask-Login + Werkzeug (hash de senhas com pbkdf2:sha256) |
| **Upload de Arquivos** | Werkzeug secure_filename                                  |
| **Geração de PDF**     | FPDF                                                      |
| **Controle de Versão** | Git + GitHub                                              |

---

## 📁 Estrutura do Projeto

```
Educonnect/
│
├── app.py                      # Aplicação Flask principal
├── database.db                 # Banco de dados SQLite (gerado automaticamente)
│
├── instance/                   # Pasta para configurações locais
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   └── style.css          # Estilos CSS
│   ├── img/                   # Imagens
│   └── js/
│       └── app.js             # Scripts JavaScript
│
├── templates/                  # Templates HTML (Jinja2)
│   ├── index.html
│   ├── login.html
│   ├── cadastro.html
│   ├── aluno_dashboard.html
│   ├── cursos_aluno.html
│   ├── aulas_aluno.html
│   ├── atividades_aluno.html
│   ├── aluno_responder_atividade.html
│   ├── certificados_aluno.html
│   ├── professor_dashboard.html
│   ├── cursos_professores.html
│   ├── editar_curso_professor.html
│   ├── atividades_professor.html
│   ├── professor_ver_submissao.html
│   ├── gestor_dashboard.html
│   ├── cursos_gestor.html
│   ├── criar_curso.html
│   ├── editar_curso.html
│   └── ver_alunos.html
│
├── uploads/                    # Vídeos de aulas enviados pelos professores
│
└── README.md                   # Este arquivo
```

---

### Fluxo de Uso Completo

#### Como Gestor:

1. Cadastre-se com role "gestor"
2. No dashboard, clique em **"Meus Cursos"**
3. Crie um novo curso com título e descrição
4. Edite o curso e atribua um professor
5. Visualize alunos matriculados e matricule manualmente se necessário

#### Como Professor:

1. Cadastre-se com role "professor"
2. Aguarde um gestor atribuir você a um curso
3. Acesse **"Meus Cursos"** e edite seu curso
4. Adicione aulas com upload de vídeo
5. Crie atividades e adicione questões de múltipla escolha
6. Visualize submissões dos alunos e acompanhe o desempenho

#### Como Aluno:

1. Cadastre-se com role "aluno"
2. Na página de cursos, matricule-se em cursos disponíveis
3. Acesse as aulas em vídeo do curso
4. Responda as atividades disponíveis
5. Visualize sua nota imediatamente após submissão
6. Baixe certificados em PDF dos cursos concluídos


## 🔐 Segurança Implementada

- ✅ **Senhas criptografadas** com Werkzeug (pbkdf2:sha256)
- ✅ **Proteção de rotas** com `@login_required`
- ✅ **Validação de permissões** por role (aluno/professor/gestor)
- ✅ **Sanitização de uploads** com `secure_filename`
- ✅ **Constraint de unicidade** para evitar submissões duplicadas
- ✅ **Secret key** para sessões Flask (alterar em produção)

---

## 📊 Modelos de Dados

### User

- id, email (único), password_hash, nome, role
- Relacionamentos: cursos_criados, cursos_matriculados

### Curso

- id, titulo, descricao, data_criacao, professor_id, gestor_id
- Relacionamentos: gestor, professor, alunos, aulas, atividades

### Aula

- id, titulo, descricao, video_filename, curso_id

### Atividade

- id, titulo, tipo, descricao, data_entrega, curso_id
- Relacionamentos: questoes, submissoes

### Questao

- id, enunciado, alternativa_a/b/c/d/e, resposta_correta, atividade_id

### Submissao

- id, atividade_id, aluno_id, enviada_em, nota
- Relacionamentos: respostas, atividade, aluno

### Resposta

- id, submissao_id, questao_id, alternativa, correta

### Certificado

- id, titulo, curso_id

---

## 🚀 Próximas Melhorias

- [ ] Adicionar paginação para listas longas
- [ ] Implementar busca e filtros de cursos
- [ ] Sistema de notificações (novos cursos, prazos)
- [ ] Dashboard com gráficos de desempenho
- [ ] Suporte a diferentes tipos de atividades (dissertativas, upload de arquivos)
- [ ] API REST para integração mobile
- [ ] Deploy em produção (Heroku, AWS, Azure)
- [ ] Migração para PostgreSQL em produção

---

## 👨‍💻 Autores

**Equipe:** Guilherme Aredes • Melissa Hollanda • Diego Vianna • Francisco Toro • Julia Rocha • Mell Dias • Murilo Antonio  
**Disciplina:** Ciclo Completo de Desenvolvimento de Software  


