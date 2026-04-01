from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from sqlalchemy.exc import IntegrityError
from fpdf import FPDF
import io


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'mkv', 'webm'}

app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')

db = SQLAlchemy(app) # Inicializa a extensão SQLAlchemy, conectando-a ao 'app' Flask.
login_manager = LoginManager(app) # Inicializa o gerenciador de login.
login_manager.login_view = 'login' # Informa ao Flask-Login qual é a rota (função) de login.
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

matriculas = db.Table('matriculas',
    db.Column('aluno_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True),
    db.Column('data_matricula', db.DateTime, server_default=db.func.now())
)

class User(db.Model, UserMixin):
    __tablename__ = 'users' # Nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True) # Coluna de ID. 'primary_key=True' diz que é o identificador único.
    
    email = db.Column(db.String(150), unique=True, nullable=False) # 'unique=True' impede emails duplicados. 'nullable=False' torna obrigatório.
    password_hash = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    
    # Requisito 1: Separação de aluno, professor e gestor
    # Vamos usar uma string simples: 'aluno', 'professor', 'gestor'
    role = db.Column(db.String(50), nullable=False, default='aluno')

    # Relações (para o futuro)
    # 'db.relationship' conecta este modelo a outros.
    # 'back_populates' é como a outra classe (Curso) irá se referir a esta.
    cursos_criados = db.relationship(
        'Curso',
        foreign_keys='Curso.gestor_id',
        back_populates='gestor',
        lazy=True
    )

    cursos_matriculados = db.relationship(
        'Curso',
        secondary=matriculas,
        back_populates='alunos',
        lazy='dynamic'
    )


    # Métodos para senha (NUNCA salve a senha pura!)
    def set_password(self, password):
        # 'generate_password_hash' cria um "hash" seguro da senha, que não pode ser revertido.
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        # 'check_password_hash' compara o hash salvo com a senha que o usuário digitou.
        return check_password_hash(self.password_hash, password)
    
@login_manager.user_loader
def load_user(user_id):
    # 'db.session.get' é uma forma rápida de buscar um item pelo seu ID (chave primária).
    return db.session.get(User, int(user_id))

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())

    # 'db.ForeignKey' diz ao banco de dados que esta coluna referencia a coluna 'id' da tabela 'users'.
    professor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    alunos = db.relationship(
        'User',
        secondary=matriculas,
        back_populates='cursos_matriculados',
        lazy='dynamic'
    )

    # Chave Estrangeira: conecta o curso ao gestor
    gestor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Relação: Define como o Python acessa o gestor a partir do curso
    gestor = db.relationship(
        'User',
        foreign_keys=[gestor_id],
        back_populates='cursos_criados',
        lazy=True
    )
    professor = db.relationship('User', foreign_keys=[professor_id], lazy=True)

class Aula(db.Model):
    __tablename__ = 'aulas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text) # Adicionado para mais detalhes
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    
    # --- ADICIONE ESTA LINHA ---
    # Armazena apenas o nome do arquivo, não o caminho completo
    video_filename = db.Column(db.String(300)) 
    # -----------------------------

    curso = db.relationship('Curso', backref=db.backref('aulas', lazy='dynamic'))


class Atividade(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    tipo = db.Column(db.String(50)) # Ex: 'prova', 'trabalho'
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    data_entrega = db.Column(db.Date)
    descricao = db.Column(db.Text)

    curso = db.relationship('Curso', backref=db.backref('atividades', lazy='dynamic'))


class Questao(db.Model):
    __tablename__ = 'questoes'
    id = db.Column(db.Integer, primary_key=True)
    enunciado = db.Column(db.Text, nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    
    # Alternativas (A, B, C, D, E)
    alternativa_a = db.Column(db.String(500))
    alternativa_b = db.Column(db.String(500))
    alternativa_c = db.Column(db.String(500))
    alternativa_d = db.Column(db.String(500))
    alternativa_e = db.Column(db.String(500))
    
    # Qual é a correta? ('A', 'B', 'C', 'D' ou 'E')
    resposta_correta = db.Column(db.String(1), nullable=False)
    
    # Relacionamento com atividade
    atividade = db.relationship('Atividade', backref=db.backref('questoes', lazy='dynamic'))

class Submissao(db.Model):
    __tablename__ = 'submissoes'
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    enviada_em = db.Column(db.DateTime, default=datetime.utcnow)
    nota = db.Column(db.Integer)  # quantidade de acertos

    atividade = db.relationship('Atividade', backref=db.backref('submissoes', lazy='dynamic'))
    aluno = db.relationship('User')

    __table_args__ = (
        db.UniqueConstraint('atividade_id', 'aluno_id', name='uq_submissao_unica'),
    )

class Resposta(db.Model):
    __tablename__ = 'respostas'
    id = db.Column(db.Integer, primary_key=True)
    submissao_id = db.Column(db.Integer, db.ForeignKey('submissoes.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'), nullable=False)
    alternativa = db.Column(db.String(1), nullable=False)  # 'A'..'E'
    correta = db.Column(db.Boolean)

    submissao = db.relationship('Submissao', backref=db.backref('respostas', cascade='all, delete-orphan'))
    questao = db.relationship('Questao')

    __table_args__ = (
        db.UniqueConstraint('submissao_id', 'questao_id', name='uq_resposta_unica'),
    )


class Certificado(db.Model):
    __tablename__ = 'certificados'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))


@app.route('/')
def index():
    # 'render_template' procura um arquivo na pasta 'templates' e o exibe no navegador.
    return render_template('login.html')

# Rota de Cadastro (Requisito 1)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # 'request.method' verifica qual o tipo de requisição (GET ou POST).
    if request.method == 'POST':
        # 'request.form.get' pega os dados enviados pelo formulário (pelo atributo 'name').
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        role = request.form.get('role')

        # Verifica se o email já existe
        # 'User.query.filter_by(...)' faz uma busca no banco de dados.
        # '.first()' pega apenas o primeiro resultado (ou None se não achar).
        user_existente = User.query.filter_by(email=email).first()

        if user_existente:
            # 'flash' exibe uma mensagem rápida para o usuário (precisa configurar no HTML).
            flash('Este email já está cadastrado. Tente fazer login.', 'error')
            # 'redirect' envia o usuário para outra rota.
            # 'url_for' gera o link correto para a função 'login'.
            return redirect(url_for('login'))

        # Cria um novo usuário
        novo_usuario = User(nome=nome, email=email, role=role)
        novo_usuario.set_password(senha) # Usa o método que criamos para gerar o hash da senha

        try:
            # 'db.session.add' adiciona o objeto à "sessão" do banco de dados (prepara para salvar).
            db.session.add(novo_usuario)
            # 'db.session.commit' salva permanentemente todas as mudanças da sessão no banco.
            db.session.commit()
            
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            # 'db.session.rollback' desfaz as mudanças se der um erro.
            db.session.rollback()
            flash(f'Erro ao cadastrar: {e}', 'error')

    # Se o método for 'GET' (usuário apenas abriu a página), exibe o formulário.
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = User.query.filter_by(email=email).first()

        # Verifica se o usuário existe E se a senha está correta
        if user and user.check_password(senha):
            # 'login_user' é a função do Flask-Login que registra o usuário como "logado" na sessão.
            login_user(user)
            flash('Login feito com sucesso!', 'success')
            
            # Redireciona com base no 'role'
            if user.role == 'professor':
                return redirect(url_for('painel_professor'))
            elif user.role == 'gestor':
                return redirect(url_for('painel_gestor'))
            else:  # aluno
                return redirect(url_for('painel_aluno'))
        else:
            flash('Email ou senha inválidos.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required # '@login_required' protege a rota, só usuários logados podem acessá-la.
def logout():
    # 'logout_user' limpa a sessão do usuário.
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/painel/professor')
@login_required # 1. Garante que o usuário está logado
def painel_professor():
    # 'current_user' é um objeto especial do Flask-Login que representa o usuário logado.
    # 2. Garante que o usuário é um professor
    if current_user.role != 'professor':
        flash('Acesso negado. Esta área é restrita para professores.', 'error')
        return redirect(url_for('index'))

    Informacao = {
        'nome': current_user.nome,
        'email': current_user.email
    }

    # Se for professor, exibe o painel
    return render_template('professor_dashboard.html', informacao=Informacao)

@app.route('/cursos/professor/view')
@login_required
def cursos_professor():
    if current_user.role != 'professor':
        flash('Acesso negado. Esta área é restrita para professores.', 'error')
        return redirect(url_for('index'))

    cursos = Curso.query.filter_by(professor_id=current_user.id).all()
    return render_template('cursos_professores.html', cursos=cursos)

@app.route('/cursos/professor/editar/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def editar_curso_professor(curso_id):
    if current_user.role != 'professor':
        flash('Acesso negado. Esta área é restrita para professores.', 'error')
        return redirect(url_for('index'))

    curso = Curso.query.get_or_404(curso_id)
    if curso.professor_id != current_user.id:
            flash('Você não é o professor deste curso.', 'error')
            return redirect(url_for('cursos_professor'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        tipo = request.form.get('tipo')
        data_entrega_str = request.form.get('data_entrega')

        data_entrega = None
        if data_entrega_str:
            try:
                data_entrega = datetime.strptime(data_entrega_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Data de entrega inválida. Use o formato AAAA-MM-DD.', 'error')
                return redirect(url_for('atividades_curso_professor', curso_id=curso.id))

        nova_atividade = Atividade(
            titulo=titulo,
            descricao=descricao,
            tipo=tipo,
            data_entrega=data_entrega,
            curso_id=curso.id  # Vincula ao curso correto
        )
        db.session.add(nova_atividade)
        db.session.commit()
        flash('Atividade adicionada com sucesso!', 'success')
        return redirect(url_for('atividades_curso_professor', curso_id=curso.id))

    Atividades = curso.atividades.all()
    return render_template('editar_curso_professor.html', curso=curso, atividades=Atividades)

@app.route('/cursos/professor/atividades/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def atividades_curso_professor(curso_id):
    if current_user.role != 'professor':
        flash('Acesso negado. Esta área é restrita para professores.', 'error')
        return redirect(url_for('index'))

    curso = Curso.query.get_or_404(curso_id)

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        tipo = request.form.get('tipo')
        data_entrega = request.form.get('data_entrega')

        nova_atividade = Atividade(titulo=titulo, descricao=descricao, tipo=tipo, data_entrega=data_entrega, curso_id=curso.id)
        db.session.add(nova_atividade)
        db.session.commit()
        flash('Atividade adicionada com sucesso!', 'success')
        return redirect(url_for('editar_curso_professor', curso_id=curso.id))

    atividades = curso.atividades.all()
    return render_template('editar_curso_professor.html', curso=curso, atividades=atividades)

@app.route('/atividade/<int:atividade_id>/adicionar_questao', methods=['GET', 'POST'])
@login_required
def adicionar_questao(atividade_id):
    if current_user.role != 'professor':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    atividade = Atividade.query.get_or_404(atividade_id)
    curso = atividade.curso
    
    # Valida que o professor é responsável pelo curso
    if curso.professor_id != current_user.id:
        flash('Você não é o professor deste curso.', 'error')
        return redirect(url_for('cursos_professor'))
    
    if request.method == 'POST':
        enunciado = request.form.get('enunciado')
        alt_a = request.form.get('alternativa_a')
        alt_b = request.form.get('alternativa_b')
        alt_c = request.form.get('alternativa_c')
        alt_d = request.form.get('alternativa_d')
        alt_e = request.form.get('alternativa_e')
        resposta_correta = request.form.get('resposta_correta')
        
        if not enunciado or not resposta_correta:
            flash('Enunciado e resposta correta são obrigatórios.', 'error')
            return redirect(url_for('adicionar_questao', atividade_id=atividade_id))
        
        nova_questao = Questao(
            enunciado=enunciado,
            atividade_id=atividade.id,
            alternativa_a=alt_a,
            alternativa_b=alt_b,
            alternativa_c=alt_c,
            alternativa_d=alt_d,
            alternativa_e=alt_e,
            resposta_correta=resposta_correta.upper()
        )
        db.session.add(nova_questao)
        db.session.commit()
        flash('Questão adicionada com sucesso!', 'success')
        return redirect(url_for('gerenciar_questoes', atividade_id=atividade.id))

    return render_template('atividades_professor.html', atividade=atividade)

@app.route('/atividade/<int:atividade_id>/questoes')
@login_required
def gerenciar_questoes(atividade_id):
    if current_user.role != 'professor':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    atividade = Atividade.query.get_or_404(atividade_id)
    curso = atividade.curso
    
    if curso.professor_id != current_user.id:
        flash('Você não é o professor deste curso.', 'error')
        return redirect(url_for('cursos_professor'))
    
    questoes = atividade.questoes.all()
    
    # ADICIONE ESTA LINHA: busca as submissões desta atividade
    submissoes = atividade.submissoes.order_by(Submissao.enviada_em.desc()).all()
    
    return render_template('atividades_professor.html', atividade=atividade, questoes=questoes, submissoes=submissoes)

@app.route('/professor/atividade/<int:atividade_id>/submissoes')
@login_required
def professor_submissoes_atividade(atividade_id):
    if current_user.role != 'professor':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))

    atividade = Atividade.query.get_or_404(atividade_id)
    if atividade.curso.professor_id != current_user.id:
        flash('Você não é o professor deste curso.', 'error')
        return redirect(url_for('cursos_professor'))

    submissoes = atividade.submissoes.order_by(Submissao.enviada_em.desc()).all()
    return render_template('professor_submissoes_atividade.html', atividade=atividade, submissoes=submissoes)

@app.route('/professor/submissao/<int:submissao_id>')
@login_required
def professor_ver_submissao(submissao_id):
    if current_user.role != 'professor':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))

    submissao = Submissao.query.get_or_404(submissao_id)
    atividade = submissao.atividade
    if atividade.curso.professor_id != current_user.id:
        flash('Você não é o professor deste curso.', 'error')
        return redirect(url_for('cursos_professor'))

    # Respostas com comparação
    respostas = (
        db.session.query(Resposta, Questao)
        .join(Questao, Resposta.questao_id == Questao.id)
        .filter(Resposta.submissao_id == submissao.id)
        .all()
    )
    # CORRIJA AQUI: Estava 'professor_submissao_detalhe.html', mude para o nome correto
    return render_template('professor_ver_submissao.html', submissao=submissao, respostas=respostas)

@app.route('/certificados')
@login_required
def certificados_aluno():
    if current_user.role != 'aluno':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    # Para este MOCK, vamos listar todos os cursos matriculados
    # No futuro, você adicionaria lógica para ver quais foram concluídos
    cursos_concluidos = current_user.cursos_matriculados.all()
    
    return render_template('certificados_aluno.html', cursos=cursos_concluidos)

# ### NOVO ### - Rota para gerar o PDF
@app.route('/gerar_certificado/<int:curso_id>')
@login_required
def gerar_certificado(curso_id):
    if current_user.role != 'aluno':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))

    curso = Curso.query.get_or_404(curso_id)
    aluno = current_user

    # Verifica se o aluno está matriculado (em um sistema real, checaria a conclusão)
    if not aluno.cursos_matriculados.filter(Curso.id == curso_id).first():
        flash('Você não pode emitir um certificado para um curso que não está matriculado.', 'error')
        return redirect(url_for('certificados_aluno'))
    
    try:
        # --- Início da Geração do PDF ---
        pdf = FPDF(orientation='L', unit='mm', format='A4') # Paisagem
        pdf.add_page()
        
        # Define uma borda
        pdf.set_line_width(1)
        pdf.rect(5.0, 5.0, 287.0, 200.0)
        
        # Título
        pdf.set_font('Arial', 'B', 24)
        pdf.ln(20) # Pula linha
        pdf.cell(0, 20, 'CERTIFICADO DE CONCLUSÃO', ln=1, align='C')
        pdf.ln(20)
        
        # Corpo do Texto
        pdf.set_font('Arial', '', 16)
        # Use 'latin-1' para lidar com acentos
        pdf.multi_cell(0, 10, f'Certificamos que {aluno.nome.encode("latin-1", "replace").decode("latin-1")} concluiu com sucesso o curso:'.encode("latin-1", "replace").decode("latin-1"), align='C')
        pdf.ln(10)
        
        # Nome do Curso
        pdf.set_font('Arial', 'B', 20)
        pdf.multi_cell(0, 10, curso.titulo.encode("latin-1", "replace").decode("latin-1"), align='C')
        pdf.ln(20)
        
        # Data (mock)
        pdf.set_font('Arial', '', 12)
        data_hoje = datetime.now().strftime("%d de %B de %Y")
        pdf.cell(0, 10, f'Emitido em: {data_hoje}'.encode("latin-1", "replace").decode("latin-1"), ln=1, align='C')
        
        # Linha da Assinatura (mock)
        pdf.ln(30)
        pdf.cell(0, 10, '_________________________', ln=1, align='C')
        pdf.cell(0, 10, 'EduConnect - Gestor da Plataforma', ln=1, align='C')
        
        # --- Fim da Geração do PDF ---
        
        # Cria um buffer de memória para o PDF
        pdf_buffer = io.BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        # Cria a resposta do Flask
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        # 'inline' tenta abrir no navegador, 'attachment' força o download
        response.headers['Content-Disposition'] = f'inline; filename=certificado_{curso.id}.pdf'
        
        return response
    
        
    except Exception as e:
        flash(f'Erro ao gerar PDF: {e}', 'error')
        return redirect(url_for('certificados_aluno'))


    

@app.route('/cursos/aluno/view')
@login_required
def cursos_aluno():
    if current_user.role != 'aluno':
        flash('Acesso negado. Esta área é restrita para alunos.', 'error')
        return redirect(url_for('index'))

    cursos_matriculados = current_user.cursos_matriculados
    cursos_disponiveis = Curso.query.filter(Curso.id.notin_([c.id for c in cursos_matriculados])).all()

    return render_template('cursos_aluno.html', cursos_matriculados=cursos_matriculados, cursos_disponiveis=cursos_disponiveis)

@app.route('/aluno/atividades/<int:atividade_id>', methods=['GET', 'POST'])
@login_required
def aluno_responder_atividade(atividade_id):
    if current_user.role != 'aluno':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))

    atividade = Atividade.query.get_or_404(atividade_id)
    curso = atividade.curso

    submissao_existente = Submissao.query.filter_by(
        atividade_id=atividade.id, aluno_id=current_user.id
    ).first()

    if request.method == 'POST':
        if submissao_existente:
            # Requisição via modal (AJAX): retorna mensagem e 409
            return '''
                <div style="text-align:center;padding:24px;">
                  <h3>Você já enviou esta atividade.</h3>
                  <p>Apenas uma submissão é permitida.</p>
                </div>
            ''', 409
        # Monta o dicionário de respostas
        respostas_dict = {}
        for k, v in request.form.items():
            if k.startswith('respostas[') and k.endswith(']'):
                qid = int(k[10:-1])
                respostas_dict[qid] = v.strip().upper()

        if not respostas_dict:
            return '<div class="erro-container"><p>❌ Selecione ao menos uma alternativa.</p></div>', 400
        # Cria a submissão (sem apagar anterior)
        submissao = Submissao(atividade_id=atividade.id, aluno_id=current_user.id)
        db.session.add(submissao)
        db.session.flush()

        acertos = 0
        questoes_todas = atividade.questoes.all()
        for q in questoes_todas:
            marcada = respostas_dict.get(q.id)
            if not marcada:
                continue
            correta = (marcada == (q.resposta_correta or '').upper())
            if correta:
                acertos += 1
            db.session.add(Resposta(
                submissao_id=submissao.id,
                questao_id=q.id,
                alternativa=marcada,
                correta=correta
            ))

        submissao.nota = acertos

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return '''
                <div style="text-align:center;padding:24px;">
                  <h3>Você já enviou esta atividade.</h3>
                </div>
            ''', 409
        
        # Retorna mensagem de sucesso
        return f'''
        <div class="sucesso-container" style="text-align: center; padding: 40px;">
            <h2 style="color: #28a745;">✓ Respostas enviadas!</h2>
            <p style="font-size: 18px;">Você acertou <strong>{acertos}/{len(questoes_todas)}</strong> questões.</p>
            <p style="color: #666;">Fechando automaticamente...</p>
        </div>
        '''

    questoes = atividade.questoes.order_by(Questao.id.asc()).all()
    return render_template(
        'aluno_responder_atividade.html',
        atividade=atividade,
        questoes=questoes,
        ja_enviou=bool(submissao_existente)
    )


@app.route('/aluno/curso/<int:curso_id>/atividades', methods=['GET'])
@login_required
def atividades_aluno(curso_id):
    if current_user.role != 'aluno':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))
    
    curso = Curso.query.get_or_404(curso_id)
    
    # Verifica se o aluno está matriculado neste curso
    if not current_user.cursos_matriculados.filter(Curso.id == curso.id).first():
        flash('Você não está matriculado neste curso.', 'error')
        return redirect(url_for('cursos_aluno'))
    
    # Busca apenas as atividades deste curso
    atividades = Atividade.query.filter_by(curso_id=curso.id).all()
    
    return render_template('atividades_aluno.html', curso=curso, atividades=atividades)

@app.route('/aluno/curso/<int:curso_id>/aulas')
@login_required
def aulas_aluno(curso_id):
    if current_user.role != 'aluno':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))

    curso = Curso.query.get_or_404(curso_id)

    # Verifica se o aluno está matriculado
    if not current_user.cursos_matriculados.filter(Curso.id == curso.id).first():
        flash('Você não está matriculado neste curso.', 'error')
        return redirect(url_for('cursos_aluno'))

    aulas = curso.aulas.all()
    return render_template('aulas_aluno.html', curso=curso, aulas=aulas)


@app.route('/cursos/gestor/view')
@login_required
def cursos_gestor():
    if current_user.role != 'gestor':
        flash('Acesso negado. Esta área é restrita para gestores.', 'error')
        return redirect(url_for('index'))

    cursos = Curso.query.filter_by(gestor_id=current_user.id).all()
    return render_template('cursos_gestor.html', cursos=cursos)


@app.route('/curso/gestor/criar', methods=['GET', 'POST'])
@login_required
def criar_curso():
    if current_user.role != 'gestor':
        return redirect(url_for('index')) # Ou página de "acesso negado"

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')

        if titulo:
            # Cria o curso e associa ao professor logado (current_user)
            novo_curso = Curso(titulo=titulo, 
                               descricao=descricao,
                               gestor_id=current_user.id) # Linka o curso ao ID do gestor
            db.session.add(novo_curso)
            db.session.commit()
            flash('Curso criado com sucesso!', 'success')
            return redirect(url_for('cursos_gestor'))

    # Se for GET, apenas mostra a página com o formulário de criar curso
    return render_template('criar_curso.html')

@app.route('/curso/editar/<int:curso_id>', methods=['GET', 'POST'])
@login_required
def editar_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    professores = User.query.filter_by(role='professor').all()

    if request.method == 'POST':
        curso.titulo = request.form.get('titulo')
        curso.descricao = request.form.get('descricao')

        professor_id = request.form.get('professor_id')  # name do select
        if professor_id:
            try:
                prof_id_int = int(professor_id)
            except ValueError:
                flash('Professor inválido.', 'error')
                return render_template('editar_curso.html', curso=curso, professores=professores)

            professor = User.query.filter_by(id=prof_id_int, role='professor').first()
            if not professor:
                flash('Professor inválido.', 'error')
                return render_template('editar_curso.html', curso=curso, professores=professores)

            curso.professor_id = professor.id
        else:
            # Permite deixar o curso sem professor atribuído
            curso.professor_id = None

        db.session.commit()
        flash('Curso atualizado com sucesso!', 'success')
        return redirect(url_for('cursos_gestor'))

    return render_template('editar_curso.html', curso=curso)

@app.route('/curso/alunos/<int:curso_id>', methods=['GET'])
@login_required
def ver_alunos(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    if current_user.role != 'gestor' and current_user.role != 'professor':
        flash('Acesso negado. Esta área é restrita para gestores e professores.', 'error')
        return redirect(url_for('index'))

    alunos = curso.alunos.all()  # Supondo que você tenha uma relação definida no modelo Curso
    return render_template('ver_alunos.html', curso=curso, alunos=alunos)

#gestor matricular aluno
@app.route('/gestor/matricular/<int:curso_id>/<int:aluno_id>', methods=['POST'])
@login_required
def gestor_matricular_aluno(curso_id, aluno_id):
    if current_user.role != 'gestor':
        return "Acesso negado", 403
    
    curso = Curso.query.get_or_404(curso_id)
    aluno = User.query.filter_by(id=aluno_id, role='aluno').first_or_404()
    
    if aluno not in curso.alunos:
        curso.alunos.append(aluno)
        db.session.commit()
        flash(f'{aluno.nome} matriculado em {curso.titulo}!', 'success')
    else:
        flash('Aluno já matriculado.', 'info')
    
    return redirect(url_for('ver_alunos', curso_id=curso_id))


@app.route('/matricular/<int:curso_id>', methods=['POST'])
@login_required
def matricular_aluno(curso_id):
    if current_user.role != 'aluno':
        flash('Apenas alunos podem se matricular.', 'error')
        return redirect(url_for('index'))
    
    curso = Curso.query.get_or_404(curso_id)
    
    # Verifica se já está matriculado
    if current_user in curso.alunos:
        flash('Você já está matriculado neste curso.', 'info')
    else:
        curso.alunos.append(current_user)
        db.session.commit()
        flash(f'Matriculado em {curso.titulo} com sucesso!', 'success')
    
    return redirect(url_for('painel_aluno'))

@app.route('/desmatricular/<int:curso_id>', methods=['POST'])
@login_required
def desmatricular_aluno(curso_id):
    if current_user.role != 'aluno':
        return "Acesso negado", 403
    
    curso = Curso.query.get_or_404(curso_id)
    
    if current_user in curso.alunos:
        curso.alunos.remove(current_user)
        db.session.commit()
        flash(f'Desmatriculado de {curso.titulo}.', 'success')
    
    return redirect(url_for('painel_aluno'))

@app.route('/lancar_atividade', methods=['POST'])
@login_required
def lancar_atividade():
    if current_user.role != 'professor':
        return "Acesso negado", 403 # 403 é o código HTTP para "Proibido"

    # Lógica para pegar dados do form (request.form.get(...))
    # Criar um objeto Atividade()
    # Salvar no db.session
    # ...
    return redirect(url_for('painel_professor'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/curso/<int:curso_id>/adicionar_aula', methods=['POST'])
@login_required
def adicionar_aula(curso_id):
    if current_user.role != 'professor':
        flash('Acesso negado.', 'error')
        return redirect(url_for('index'))

    curso = Curso.query.get_or_404(curso_id)
    if curso.professor_id != current_user.id:
        flash('Você não tem permissão para adicionar aulas a este curso.', 'error')
        return redirect(url_for('cursos_professor'))

    titulo = request.form.get('titulo_aula')
    descricao = request.form.get('descricao_aula')
    video_file = request.files.get('video_aula')

    if not titulo or not video_file or video_file.filename == '':
        flash('Título e arquivo de vídeo são obrigatórios.', 'error')
        return redirect(url_for('editar_curso_professor', curso_id=curso.id))

    if video_file and allowed_file(video_file.filename):
        # Garante que o nome do arquivo é seguro
        filename = secure_filename(video_file.filename)
        
        # Salva o arquivo na pasta de uploads
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Cria a nova aula no banco de dados
        nova_aula = Aula(
            titulo=titulo,
            descricao=descricao,
            curso_id=curso.id,
            video_filename=filename # Salva o nome do arquivo
        )
        db.session.add(nova_aula)
        db.session.commit()
        flash('Aula adicionada com sucesso!', 'success')
    else:
        flash('Formato de vídeo inválido. Use mp4, mov, avi ou mkv.', 'error')

    return redirect(url_for('editar_curso_professor', curso_id=curso.id))

@app.route('/uploads/<path:filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/painel/aluno', methods=['GET', 'POST'])
@login_required # 1. Garante que o usuário está logado
def painel_aluno():
    # 'current_user' é um objeto especial do Flask-Login que representa o usuário logado.
    # 2. Garante que o usuário é um aluno
    if current_user.role != 'aluno':
        flash('Acesso negado. Esta área é restrita para alunos.', 'error')
        return redirect(url_for('index'))

    Informacao = {
        'nome': current_user.nome,
        'email': current_user.email
    }

    # Se for aluno, exibe o painel
    return render_template('aluno_dashboard.html', informacao=Informacao)


@app.route('/painel/gestor')
@login_required # 1. Garante que o usuário está logado
def painel_gestor():
    # 'current_user' é um objeto especial do Flask-Login que representa o usuário logado.
    # 2. Garante que o usuário é um gestor
    if current_user.role != 'gestor':
        flash('Acesso negado. Esta área é restrita para gestores.', 'error')
        return redirect(url_for('index'))


    Informacao = {
        'nome': current_user.nome,
        'email': current_user.email
    }
    # Se for gestor, exibe o painel
    return render_template('gestor_dashboard.html', informacao=Informacao)


# --- Inicialização ---
if __name__ == '__main__':
    # Cria as tabelas do banco de dados antes de rodar a app pela primeira vez
    with app.app_context():
        db.create_all() # db.create_all() lê todos os Modelos (classes) e cria as tabelas no 'database.db'.
    
    app.run(debug=True) # Inicia o servidor web. debug=True faz o servidor reiniciar automaticamente quando você salvar o arquivo.