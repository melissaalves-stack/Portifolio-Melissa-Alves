
/* Reset básico e ajustes globais */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Sora", sans-serif;
  background-color: #fefefe;
  color: #222;
  line-height: 1.6;
}

.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 1rem;
}

/* Header fixo com logo e navegação */
header {
  background-color: #111;
  padding: 0.82rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.logo {
  font-size: 1.75rem;
  font-weight: 800;
  color: #fff;
}

.logo .realce {
  color: #00fff7;
}

/* Navegação padrão (desktop) */
.navbar {
  display: flex;
  gap: 1.5rem;
}

.navbar a {
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  position: relative;
  transition: color 0.3s ease;
}

.navbar a::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0%;
  height: 2px;
  background-color: #00fff7;
  transition: width 0.3s ease;
}

.navbar a:hover::after {
  width: 100%;
}

.navbar a:hover {
  color: #00fff7;
}

/* Ícone do menu mobile */
.menu-icon {
  display: none;
  font-size: 1.8rem;
  color: #fff;
  cursor: pointer;
}

/* Esconde checkbox padrão */
#menu-toggle {
  display: none;
}

/* Navegação responsiva (mobile) */
@media (max-width: 768px) {
  .menu-icon {
    display: block;
  }

  .navbar {
    display: none;
    width: 100%;
    flex-direction: column;
    background-color: #111;
    margin-top: 1rem;
    border-top: 1px solid #333;
    padding-top: 1rem;
  }

  #menu-toggle:checked ~ .navbar {
    display: flex;
  }

  .navbar a {
    padding: 0.5rem 1rem;
    border-bottom: 1px solid #222;
  }
}

/* Hero - destaque inicial com imagem e texto */
.hero {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #f1f1f1 0%, #eaeaea 100%);
  padding: 5rem 2rem;
  height: 80vh;
}

.hero-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.hero-img {
  flex: 1;
  text-align: center;
  animation: float 3s ease-in-out infinite;
}

.profile-img {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  border: 5px solid #00fff7;
  box-shadow: 0 0 25px #ff00c888;
  object-fit: cover;
}

.hero-text {
  flex: 2;
  max-width: 500px;
}

.hero-text h2 {
  font-family: "Bitcount", system-ui;
  font-weight: 500;
  font-size: 3rem;
  color: #00fff7;
}

.hero-text h2,
.hero-text p {
  text-align: left;
}

.hero-text p {
  margin: 1rem 0 2rem;
}

/* Botão principal reutilizável */
.btn-primary {
  background-color: #111;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.3s ease;
}

.btn-primary:hover {
  background-color: #00fff7;
}

/* Hero responsivo */
@media (max-width: 768px) {
  .hero-grid {
    flex-direction: column;
    text-align: center;
  }

  .hero-text h2,
  .hero-text p {
    text-align: center;
  }

  .hero-text {
    align-items: center;
  }
}

/* Seções gerais */
.section {
  padding: 3rem 2rem;
}

.section-title {
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #444;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.section-text {
  font-size: 1.05rem;
  line-height: 1.8;
  color: #333;
  margin-bottom: 1.2rem;
}

/* Grid de skills (cards) */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  justify-items: center;
}

.skill-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  text-align: center;
  padding: 1rem;
  border-radius: 8px;
  width: 6rem;
  height: 6rem;
  background-color: #f8f8f8;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.skill-card:hover {
  transform: translateY(-5px);
}

.skill-card i {
  font-size: 40px;
}

.skill-card span {
  font-weight: 600;
  font-size: 0.95rem;
  color: #333;
}

/* Tags de skills alternativa (não usada por padrão) */
.skills-list-icons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
}

.skill-tag {
  background-color: #111;
  color: #fff;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
}

.skill-tag i {
  font-size: 1.1rem;
}

/* Botão base genérico */
.btn {
  display: inline-block;
  margin-top: 1rem;
  background-color: #222;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
}

/* Seção de projetos */
.projetos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.projeto-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.projeto-card:hover {
  transform: translateY(-5px);
}

.projeto-card img {
  width: 100%;
  height: auto;
  display: block;
}

.projeto-card h3 {
  margin: 1rem;
  font-size: 1.25rem;
}

.projeto-card p {
  margin: 0 1rem 1rem;
  font-size: 0.95rem;
  color: #444;
}

.projeto-card .btns {
  display: flex;
  gap: 1rem;
  margin: 1rem;
  flex-wrap: wrap;
}

.projeto-card .btns a {
  background-color: #222;
  color: #fff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: bold;
  font-size: 0.9rem;
}

.projeto-card .btns a:hover {
  background-color: #00fff7;
}

/* Card de contato com links sociais */
.contato-card {
  background: linear-gradient(135deg, #fdfdfd, #f3f3f3);
  border: 2px solid #eee;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  max-width: 700px;
  margin: 0 auto;
}

.contato-card h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.contato-card p {
  font-size: 1.1rem;
  color: #444;
  margin-bottom: 2rem;
}

.btn-social {
  background-color: #111;
  color: #fff;
  padding: 0.75rem 1.25rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.3s ease;
}

.btn-social:hover {
  background-color: #00fff7;
  color: #fff;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-social i {
  font-size: 1.1rem;
}

/* Footer com créditos */
footer {
  text-align: center;
  padding: 2rem 1rem;
  font-size: 0.9rem;
  color: #666;
  background-color: #111;
}

footer a {
  color: #f9f9f9;
  text-decoration: none;
  font-weight: 500;
}

footer a:hover {
  text-decoration: underline;
}
