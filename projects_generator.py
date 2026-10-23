# -*- coding: utf-8 -*-
"""
Gerador da Página: Laboratório de Projetos & Portfólio de IA (projetos.html)
A 4ª página do ecossistema: Portfólio de elite com os 6 projetos essenciais da trilha,
gestão interativa de status, links de repositórios/demos, anotações de engenharia
e exportador para LinkedIn / README.
"""

from auth_aws_sync import AUTH_GUARD_HEAD_SCRIPT, AUTH_AWS_SYNC_CSS, AWS_SYNC_MODAL_HTML, CHANGE_CREDENTIALS_MODAL_HTML, AUTH_AWS_SYNC_JS

PROJECTS_CSS = """
/* =========================================================================
   ESTILOS ESPECÍFICOS DO LABORATÓRIO DE PROJETOS & PORTFÓLIO
   ========================================================================= */
.proj-main {
  max-width: 1260px;
  margin: 0 auto;
  padding: 32px 24px 100px;
}
.proj-hero {
  text-align: center;
  margin-bottom: 30px;
}
.proj-hero h1 {
  font-size: 2.2rem;
  font-weight: 850;
  letter-spacing: -.03em;
  margin: 0 0 10px;
  background: linear-gradient(135deg, var(--tx) 30%, #ec4899);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.proj-hero p {
  font-size: 1.05rem;
  color: var(--mu);
  max-width: 780px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Barra de Métricas do Portfólio */
.proj-metrics-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 16px;
  margin-bottom: 28px;
}
.proj-metric-card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 4px 18px rgba(0,0,0,.03);
}
.proj-metric-lbl {
  font-size: .78rem;
  font-weight: 750;
  text-transform: uppercase;
  color: var(--mu);
  letter-spacing: .03em;
  margin-bottom: 6px;
  display: block;
}
.proj-metric-val {
  font-size: 1.4rem;
  font-weight: 850;
  color: var(--tx);
  display: flex;
  align-items: baseline;
  gap: 6px;
}

/* Barra de Filtros e Ações */
.proj-actions-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 16px;
  padding: 14px 18px;
  margin-bottom: 26px;
}
.proj-filters-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.proj-filter-btn {
  background: var(--bg);
  border: 1px solid var(--bd);
  color: var(--mu);
  font-size: .82rem;
  font-weight: 700;
  padding: 7px 14px;
  border-radius: 99px;
  cursor: pointer;
  transition: all .2s;
}
.proj-filter-btn:hover, .proj-filter-btn.active {
  background: var(--ac);
  border-color: var(--ac);
  color: #fff;
}
.proj-btn-add {
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  border: none;
  font-weight: 800;
  font-size: .84rem;
  padding: 9px 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all .2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.proj-btn-add:hover {
  filter: brightness(1.1);
  transform: translateY(-1px);
}
.proj-btn-export {
  background: var(--bg);
  border: 1px solid var(--bd);
  color: var(--tx);
  font-weight: 750;
  font-size: .84rem;
  padding: 9px 15px;
  border-radius: 10px;
  cursor: pointer;
  transition: all .2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.proj-btn-export:hover {
  background: var(--card);
  border-color: var(--ac);
  color: var(--ac);
}

/* Grid de Projetos */
.proj-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 22px;
}
.proj-card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 18px;
  padding: 22px;
  box-shadow: 0 6px 24px rgba(0,0,0,.03);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform .2s, border-color .2s;
  position: relative;
}
.proj-card:hover {
  transform: translateY(-3px);
  border-color: rgba(79,70,229,.4);
  box-shadow: 0 12px 32px rgba(79,70,229,.08);
}
.proj-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}
.proj-phase-badge {
  font-size: .74rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .04em;
  padding: 4px 10px;
  border-radius: 99px;
  background: rgba(79,70,229,.12);
  color: var(--ac);
  border: 1px solid rgba(79,70,229,.25);
}
.proj-status-select {
  font-size: .78rem;
  font-weight: 750;
  padding: 4px 10px;
  border-radius: 99px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
  cursor: pointer;
  outline: none;
}
.proj-status-select.status-done {
  background: rgba(16,185,129,.12);
  border-color: rgba(16,185,129,.35);
  color: #10b981;
}
.proj-status-select.status-wip {
  background: rgba(245,158,11,.12);
  border-color: rgba(245,158,11,.35);
  color: #f59e0b;
}
.proj-status-select.status-planned {
  background: rgba(100,116,139,.12);
  border-color: rgba(100,116,139,.35);
  color: var(--mu);
}
.proj-title {
  font-size: 1.18rem;
  font-weight: 800;
  margin: 0 0 8px;
  color: var(--tx);
  line-height: 1.35;
}
.proj-desc {
  font-size: .88rem;
  color: var(--mu);
  line-height: 1.55;
  margin-bottom: 16px;
}
.proj-stack-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 18px;
}
.proj-tag {
  background: var(--bg);
  border: 1px solid var(--bd);
  color: var(--tx);
  font-size: .73rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
}
.proj-card-footer {
  border-top: 1px solid var(--bd);
  padding-top: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.proj-footer-links {
  display: flex;
  gap: 8px;
}
.proj-link-btn {
  background: var(--bg);
  border: 1px solid var(--bd);
  color: var(--tx);
  font-size: .78rem;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 8px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all .2s;
}
.proj-link-btn:hover {
  background: var(--card);
  border-color: var(--ac);
  color: var(--ac);
}
.proj-notes-btn {
  background: rgba(79,70,229,.1);
  border: 1px solid rgba(79,70,229,.25);
  color: var(--ac);
  font-size: .78rem;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: all .2s;
}
.proj-notes-btn:hover {
  background: var(--ac);
  color: #fff;
}
"""

def generate_projects_page(out_path, shared_css):
    full_css = shared_css + "\n" + AUTH_AWS_SYNC_CSS + "\n" + PROJECTS_CSS

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Laboratório de Projetos & Portfólio de IA</title>
{AUTH_GUARD_HEAD_SCRIPT}
<style>
{full_css}
</style>
</head>
<body>

<!-- TOPBAR FIXA -->
<header class="top-nav">
  <div class="top-nav-inner">
    <a href="index.html" class="nav-brand">🚀 <span>Roteiro IA</span></a>
    <nav class="nav-links">
      <a href="index.html" class="nav-link">🏠 Hub Central</a>
      <a href="ia.html" class="nav-link">🤖 IA & Código</a>
      <a href="matematica.html" class="nav-link">📐 Matemática</a>
      <a href="ingles.html" class="nav-link">🇺🇸 Inglês EnglishBay</a>
      <a href="projetos.html" class="nav-link active">🛠️ Projetos & Portfólio</a>
    </nav>
    <div class="nav-right">
      <div class="nav-user-dropdown-wrap" id="nav-user-wrap">
        <button class="nav-user-pill" onclick="toggleUserDropdown(event)" id="nav-auth-user" title="Menu da Conta">
          👤 <span>João Naziozeno</span> <span style="font-size:.7rem;margin-left:2px">▾</span>
        </button>
        <div class="nav-user-dropdown" id="nav-user-dropdown" hidden>
          <div class="dropdown-user-header">
            <div class="dropdown-user-name" id="dropdown-user-name">João Naziozeno</div>
            <div class="dropdown-user-email" id="dropdown-user-email">joao@roteiro.ia</div>
          </div>
          <button class="dropdown-item" onclick="openAwsSyncModal()">
            <span>☁️</span>
            <span>Sincronização AWS</span>
          </button>
          <button class="dropdown-item" onclick="openChangeCredentialsModal()">
            <span>🔑</span>
            <span>Alterar Usuário & Senha</span>
          </button>
          <div class="dropdown-divider"></div>
          <button class="dropdown-item danger" onclick="handleUserLogout()">
            <span>🔒</span>
            <span>Sair da Conta</span>
          </button>
        </div>
      </div>
      <button class="nav-theme-btn" onclick="toggleTheme()" title="Alternar tema claro/escuro">🌓</button>
    </div>
  </div>
</header>

<main class="proj-main">
  <!-- HERO -->
  <section class="proj-hero">
    <h1>Laboratório de Projetos & Portfólio de IA</h1>
    <p>
      O código que você escreve é o seu maior currículo. Acompanhe a construção dos <b>6 projetos práticos essenciais da trilha</b>, documente seus repositórios, APIs, testes e gere um portfólio pronto para impressionar recrutadores.
    </p>
  </section>

  <!-- BARRA DE MÉTRICAS -->
  <section class="proj-metrics-bar">
    <div class="proj-metric-card">
      <span class="proj-metric-lbl">Total de Projetos</span>
      <div class="proj-metric-val" id="metric-total-proj">6 <span style="font-size:.85rem;color:var(--mu);font-weight:600">estruturados</span></div>
    </div>
    <div class="proj-metric-card">
      <span class="proj-metric-lbl">Projetos Concluídos</span>
      <div class="proj-metric-val" style="color:#10b981" id="metric-done-proj">0 <span style="font-size:.85rem;color:var(--mu);font-weight:600">projetos</span></div>
    </div>
    <div class="proj-metric-card">
      <span class="proj-metric-lbl">Em Desenvolvimento</span>
      <div class="proj-metric-val" style="color:#f59e0b" id="metric-wip-proj">1 <span style="font-size:.85rem;color:var(--mu);font-weight:600">projeto</span></div>
    </div>
    <div class="proj-metric-card">
      <span class="proj-metric-lbl">Taxa de Conclusão</span>
      <div class="proj-metric-val" style="color:var(--ac)" id="metric-pct-proj">0%</div>
    </div>
  </section>

  <!-- BARRA DE FILTROS & AÇÕES -->
  <section class="proj-actions-bar">
    <div class="proj-filters-group">
      <button class="proj-filter-btn active" onclick="setProjectFilter('all', this)">Todos (6)</button>
      <button class="proj-filter-btn" onclick="setProjectFilter('fase1', this)">Fase 1 (Python)</button>
      <button class="proj-filter-btn" onclick="setProjectFilter('fase2', this)">Fase 2 (Dados)</button>
      <button class="proj-filter-btn" onclick="setProjectFilter('fase3', this)">Fase 3 (ML)</button>
      <button class="proj-filter-btn" onclick="setProjectFilter('fase4', this)">Fase 4 (PyTorch)</button>
      <button class="proj-filter-btn" onclick="setProjectFilter('fase5', this)">Fase 5 (LLMs/RAG)</button>
      <button class="proj-filter-btn" onclick="setProjectFilter('fase6', this)">Fase 6 (MLOps/AWS)</button>
    </div>

    <div style="display:flex;gap:10px;align-items:center">
      <button class="proj-btn-export" onclick="openExportPortfolioModal()">
        📋 Exportar para LinkedIn / README
      </button>
      <button class="proj-btn-add" onclick="openAddProjectModal()">
        + Adicionar Projeto Próprio
      </button>
    </div>
  </section>

  <!-- GRID DE PROJETOS -->
  <section class="proj-grid" id="portfolio-projects-grid">
    <!-- Renderizado dinamicamente via JS -->
  </section>
</main>

{AWS_SYNC_MODAL_HTML}
{CHANGE_CREDENTIALS_MODAL_HTML}

<!-- MODAL: ANOTAÇÕES & LIÇÕES APRENDIDAS DO PROJETO -->
<div id="modal-project-notes" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:650px;width:95%">
    <div class="modal-sub-header">
      <h3 class="modal-sub-title" id="proj-notes-modal-title">Anotações do Projeto</h3>
      <button class="modal-close-icon" onclick="closeProjectNotesModal()">✕</button>
    </div>
    <p style="font-size:.85rem;color:var(--mu);margin-bottom:12px">
      Documente a arquitetura, desafios enfrentados, soluções adotadas e métricas alcançadas.
    </p>
    <textarea id="proj-notes-textarea" style="width:100%;height:220px;padding:12px;background:var(--bg);border:1px solid var(--bd);border-radius:10px;color:var(--tx);font-family:monospace;font-size:.88rem;resize:vertical;box-sizing:border-box" placeholder="Escreva aqui os insights e detalhes técnicos..."></textarea>
    <div style="display:flex;justify-content:flex-end;gap:10px;margin-top:14px">
      <button class="aws-btn-sec" onclick="closeProjectNotesModal()">Cancelar</button>
      <button class="aws-btn-primary" onclick="saveProjectNotes()">💾 Salvar Anotações</button>
    </div>
  </div>
</div>

<!-- MODAL: EDITAR LINKS DO PROJETO -->
<div id="modal-edit-links" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:550px;width:95%">
    <div class="modal-sub-header">
      <h3 class="modal-sub-title" id="edit-links-title">Editar Links do Projeto</h3>
      <button class="modal-close-icon" onclick="closeEditLinksModal()">✕</button>
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;margin:16px 0">
      <div>
        <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Link do Repositório GitHub</label>
        <input type="url" id="input-edit-github" class="aws-cfg-input" placeholder="https://github.com/JoaoNaziozeno/seu-projeto">
      </div>
      <div>
        <label style="font-size:.78rem;font-weight:700;color:var(--mu);display:block;margin-bottom:4px">Link da Demonstração ao Vivo / Deploy</label>
        <input type="url" id="input-edit-demo" class="aws-cfg-input" placeholder="https://seunome.amplifyapp.com ou link Streamlit/HuggingFace">
      </div>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:10px">
      <button class="aws-btn-sec" onclick="closeEditLinksModal()">Cancelar</button>
      <button class="aws-btn-primary" onclick="saveProjectLinks()">💾 Salvar Links</button>
    </div>
  </div>
</div>

<!-- MODAL: EXPORTAR PORTFÓLIO EM MARKDOWN (LINKEDIN/README) -->
<div id="modal-export-portfolio" class="modal-sub-overlay" hidden>
  <div class="modal-sub-box" style="max-width:700px;width:95%">
    <div class="modal-sub-header">
      <div style="display:flex;align-items:center;gap:8px">
        <span>📋</span>
        <h3 class="modal-sub-title">Exportar Portfólio (Markdown / LinkedIn)</h3>
      </div>
      <button class="modal-close-icon" onclick="closeExportPortfolioModal()">✕</button>
    </div>
    <p style="font-size:.85rem;color:var(--mu);margin-bottom:12px">
      Copie o texto estruturado abaixo para colar diretamente no seu README de perfil do GitHub ou no LinkedIn:
    </p>
    <textarea id="portfolio-export-textarea" readonly style="width:100%;height:260px;padding:12px;background:var(--bg);border:1px solid var(--bd);border-radius:10px;color:var(--tx);font-family:monospace;font-size:.84rem;resize:vertical;box-sizing:border-box"></textarea>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px">
      <span style="font-size:.8rem;color:var(--mu)" id="copy-portfolio-status">Clique em Copiar</span>
      <button class="aws-btn-primary" onclick="copyPortfolioText()">📄 Copiar Texto Completo</button>
    </div>
  </div>
</div>

<script>
{AUTH_AWS_SYNC_JS}

// =========================================================================
// BANCO DE DADOS LOCAL E REPOSITÓRIO DE PROJETOS DE IA
// =========================================================================
const PORTFOLIO_STORAGE_KEY = "roteiro_portfolio_projects";

const DEFAULT_PROJECTS = [
  {{
    id: "proj-1",
    phaseKey: "fase1",
    phaseLabel: "Fase 1 · Python Puro & APIs",
    title: "CLI de Previsão do Tempo & Cotações com APIs",
    desc: "Aplicação terminal em Python que consome APIs públicas REST (OpenWeather & CoinGecko), trata exceções, manipula dados JSON estruturados e exibe dashboards no terminal.",
    stack: ["Python 3", "Requests", "JSON", "Argparse", "CLI"],
    status: "wip",
    githubUrl: "https://github.com/JoaoNaziozeno/Roteiro",
    demoUrl: "",
    notes: "Primeiro projeto em Python focado em requisições HTTP, headers, timeouts e tratamento robusto de erros."
  }},
  {{
    id: "proj-2",
    phaseKey: "fase2",
    phaseLabel: "Fase 2 · Dados & SQL",
    title: "Pipeline ETL & Análise Exploratória com PostgreSQL",
    desc: "Ingestão e saneamento de grandes volumes de dados (Kaggle), transformação em DataFrames Pandas, persistência em PostgreSQL e geração de gráficos de correlação.",
    stack: ["Pandas", "NumPy", "PostgreSQL", "SQL", "Seaborn"],
    status: "planned",
    githubUrl: "",
    demoUrl: "",
    notes: ""
  }},
  {{
    id: "proj-3",
    phaseKey: "fase3",
    phaseLabel: "Fase 3 · Machine Learning",
    title: "Microsserviço de ML Preditivo com FastAPI & Scikit-Learn",
    desc: "Modelo supervisionado de classificação/regressão com validação cruzada, métricas ROC-AUC e deploy de API REST assíncrona documentada com Swagger.",
    stack: ["Scikit-Learn", "FastAPI", "Uvicorn", "Joblib", "Pydantic"],
    status: "planned",
    githubUrl: "",
    demoUrl: "",
    notes: ""
  }},
  {{
    id: "proj-4",
    phaseKey: "fase4",
    phaseLabel: "Fase 4 · Visão & Deep Learning",
    title: "Classificador Neural de Imagens com PyTorch (CNN)",
    desc: "Implementação de Rede Neural Convolucional com PyTorch, Transfer Learning (ResNet-50), data augmentation e otimização por gradiente descendente em GPU.",
    stack: ["PyTorch", "Torchvision", "CUDA", "CNN", "Matplotlib"],
    status: "planned",
    githubUrl: "",
    demoUrl: "",
    notes: ""
  }},
  {{
    id: "proj-5",
    phaseKey: "fase5",
    phaseLabel: "Fase 5 · LLMs & Agentes",
    title: "Chatbot com Busca Semântica em PDFs (RAG) & LangChain",
    desc: "Assistente inteligente com embeddings vetoriais, banco pgvector/ChromaDB e raciocínio de contexto com LLM (OpenAI/Claude) para consulta a documentos técnicos.",
    stack: ["LangChain", "LlamaIndex", "ChromaDB", "pgvector", "LLMs"],
    status: "planned",
    githubUrl: "",
    demoUrl: "",
    notes: ""
  }},
  {{
    id: "proj-6",
    phaseKey: "fase6",
    phaseLabel: "Fase 6 · MLOps & Nuvem AWS",
    title: "Pipeline de Deploy de IA em Nuvem AWS com Docker & CI/CD",
    desc: "Containerização completa com Docker, automação de testes com GitHub Actions e deploy de alta disponibilidade na AWS (EC2/ECS) com monitoramento.",
    stack: ["Docker", "GitHub Actions", "AWS EC2", "AWS S3", "FastAPI"],
    status: "planned",
    githubUrl: "",
    demoUrl: "",
    notes: ""
  }}
];

let projectsData = [];
let currentFilter = "all";
let activeEditProjId = null;

function loadProjects() {{
  try {{
    const saved = localStorage.getItem(PORTFOLIO_STORAGE_KEY);
    if (saved) {{
      projectsData = JSON.parse(saved);
    }} else {{
      projectsData = JSON.parse(JSON.stringify(DEFAULT_PROJECTS));
      saveProjects();
    }}
  }} catch(e) {{
    projectsData = JSON.parse(JSON.stringify(DEFAULT_PROJECTS));
  }}
  renderProjects();
  updateMetrics();
}}

function saveProjects() {{
  try {{
    localStorage.setItem(PORTFOLIO_STORAGE_KEY, JSON.stringify(projectsData));
  }} catch(e) {{}}
}}

function renderProjects() {{
  const grid = document.getElementById("portfolio-projects-grid");
  if (!grid) return;

  const filtered = projectsData.filter(p => {{
    if (currentFilter === "all") return true;
    return p.phaseKey === currentFilter;
  }});

  grid.innerHTML = filtered.map(p => {{
    const statusClass = p.status === "done" ? "status-done" : (p.status === "wip" ? "status-wip" : "status-planned");
    const ghLink = p.githubUrl ? `<a href="${{p.githubUrl}}" target="_blank" rel="noopener" class="proj-link-btn">💻 GitHub</a>` : `<button class="proj-link-btn" onclick="openEditLinksModal('${{p.id}}')">+ Add GitHub</button>`;
    const demoLink = p.demoUrl ? `<a href="${{p.demoUrl}}" target="_blank" rel="noopener" class="proj-link-btn" style="color:#10b981">🌐 Demo</a>` : `<button class="proj-link-btn" onclick="openEditLinksModal('${{p.id}}')">+ Add Demo</button>`;

    return `
      <div class="proj-card">
        <div>
          <div class="proj-card-top">
            <span class="proj-phase-badge">${{p.phaseLabel}}</span>
            <select class="proj-status-select ${{statusClass}}" onchange="onProjectStatusChange('${{p.id}}', this.value)">
              <option value="planned" ${{p.status === "planned" ? "selected" : ""}}>⚪ Planejado</option>
              <option value="wip" ${{p.status === "wip" ? "selected" : ""}}>🟡 Em Andamento</option>
              <option value="done" ${{p.status === "done" ? "selected" : ""}}>🟢 Concluído</option>
            </select>
          </div>
          <h3 class="proj-title">${{p.title}}</h3>
          <p class="proj-desc">${{p.desc}}</p>
          <div class="proj-stack-tags">
            ${{p.stack.map(s => `<span class="proj-tag">${{s}}</span>`).join("")}}
          </div>
        </div>

        <div class="proj-card-footer">
          <div class="proj-footer-links">
            ${{ghLink}}
            ${{demoLink}}
          </div>
          <button class="proj-notes-btn" onclick="openProjectNotesModal('${{p.id}}')" title="Ver e editar anotações de engenharia">
            📝 Anotações
          </button>
        </div>
      </div>
    `;
  }}).join("");
}}

function updateMetrics() {{
  const total = projectsData.length;
  const done = projectsData.filter(p => p.status === "done").length;
  const wip = projectsData.filter(p => p.status === "wip").length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  document.getElementById("metric-total-proj").innerHTML = `${{total}} <span style="font-size:.85rem;color:var(--mu);font-weight:600">projetos</span>`;
  document.getElementById("metric-done-proj").innerHTML = `${{done}} <span style="font-size:.85rem;color:var(--mu);font-weight:600">projetos</span>`;
  document.getElementById("metric-wip-proj").innerHTML = `${{wip}} <span style="font-size:.85rem;color:var(--mu);font-weight:600">em andamento</span>`;
  document.getElementById("metric-pct-proj").textContent = pct + "%";
}}

function setProjectFilter(filterKey, btnEl) {{
  currentFilter = filterKey;
  document.querySelectorAll(".proj-filter-btn").forEach(b => b.classList.remove("active"));
  if (btnEl) btnEl.classList.add("active");
  renderProjects();
}}

function onProjectStatusChange(projId, newStatus) {{
  const p = projectsData.find(x => x.id === projId);
  if (p) {{
    p.status = newStatus;
    saveProjects();
    updateMetrics();
    renderProjects();
    if (typeof showToast === "function") showToast("Status do projeto atualizado!");
  }}
}}

function openProjectNotesModal(projId) {{
  activeEditProjId = projId;
  const p = projectsData.find(x => x.id === projId);
  if (!p) return;
  document.getElementById("proj-notes-modal-title").textContent = "📝 " + p.title;
  document.getElementById("proj-notes-textarea").value = p.notes || "";
  const modal = document.getElementById("modal-project-notes");
  modal.hidden = false;
  modal.style.display = "flex";
}}

function closeProjectNotesModal() {{
  const modal = document.getElementById("modal-project-notes");
  modal.hidden = true;
  modal.style.display = "none";
}}

function saveProjectNotes() {{
  if (!activeEditProjId) return;
  const p = projectsData.find(x => x.id === activeEditProjId);
  if (p) {{
    p.notes = document.getElementById("proj-notes-textarea").value;
    saveProjects();
    closeProjectNotesModal();
    if (typeof showToast === "function") showToast("Anotações salvas com sucesso!");
  }}
}}

function openEditLinksModal(projId) {{
  activeEditProjId = projId;
  const p = projectsData.find(x => x.id === projId);
  if (!p) return;
  document.getElementById("edit-links-title").textContent = "🔗 Links: " + p.title;
  document.getElementById("input-edit-github").value = p.githubUrl || "";
  document.getElementById("input-edit-demo").value = p.demoUrl || "";
  const modal = document.getElementById("modal-edit-links");
  modal.hidden = false;
  modal.style.display = "flex";
}}

function closeEditLinksModal() {{
  const modal = document.getElementById("modal-edit-links");
  modal.hidden = true;
  modal.style.display = "none";
}}

function saveProjectLinks() {{
  if (!activeEditProjId) return;
  const p = projectsData.find(x => x.id === activeEditProjId);
  if (p) {{
    p.githubUrl = document.getElementById("input-edit-github").value.trim();
    p.demoUrl = document.getElementById("input-edit-demo").value.trim();
    saveProjects();
    closeEditLinksModal();
    renderProjects();
    if (typeof showToast === "function") showToast("Links atualizados!");
  }}
}}

function openExportPortfolioModal() {{
  const modal = document.getElementById("modal-export-portfolio");
  let md = "# 🚀 Portfólio de Engenharia de Inteligência Artificial\\n\\n";
  md += "**Desenvolvedor:** João Naziozeno\\n";
  md += "**Roteiro de Formação:** Do Zero ao Desenvolvimento de IA\\n\\n";
  md += "## 🛠️ Projetos Práticos Desenvolvidos\\n\\n";

  projectsData.forEach((p, idx) => {{
    const stEmoji = p.status === "done" ? "✅ Concluído" : (p.status === "wip" ? "⏳ Em Desenvolvimento" : "📌 Planejado");
    md += `### ${{idx + 1}}. ${{p.title}} (${{stEmoji}})\\n`;
    md += `* **Fase:** ${{p.phaseLabel}}\\n`;
    md += `* **Descrição:** ${{p.desc}}\\n`;
    md += `* **Stack Tecnológica:** ${{p.stack.join(", ")}}\\n`;
    if (p.githubUrl) md += `* **Código-Fonte (GitHub):** [${{p.githubUrl}}](${{p.githubUrl}})\\n`;
    if (p.demoUrl) md += `* **Demonstração:** [${{p.demoUrl}}](${{p.demoUrl}})\\n`;
    if (p.notes) md += `* **Arquitetura & Detalhes:** ${{p.notes}}\\n`;
    md += "\\n---\\n\\n";
  }});

  document.getElementById("portfolio-export-textarea").value = md;
  document.getElementById("copy-portfolio-status").textContent = "Clique em Copiar";
  modal.hidden = false;
  modal.style.display = "flex";
}}

function closeExportPortfolioModal() {{
  const modal = document.getElementById("modal-export-portfolio");
  modal.hidden = true;
  modal.style.display = "none";
}}

function copyPortfolioText() {{
  const ta = document.getElementById("portfolio-export-textarea");
  ta.select();
  navigator.clipboard.writeText(ta.value).then(() => {{
    document.getElementById("copy-portfolio-status").textContent = "✅ Copiado para a área de transferência!";
    if (typeof showToast === "function") showToast("Portfólio copiado!");
  }}).catch(() => {{
    alert("Texto selecionado, use Ctrl+C para copiar.");
  }});
}}

function openAddProjectModal() {{
  const title = prompt("Digite o título do novo projeto:");
  if (!title) return;
  const desc = prompt("Descrição resumida do que o projeto faz:") || "";
  const stackRaw = prompt("Tecnologias usadas (separadas por vírgula):", "Python, FastAPI") || "Python";
  const stack = stackRaw.split(",").map(s => s.trim()).filter(Boolean);

  const newProj = {{
    id: "proj-custom-" + Date.now(),
    phaseKey: "fase1",
    phaseLabel: "Projeto Personalizado",
    title: title,
    desc: desc,
    stack: stack,
    status: "wip",
    githubUrl: "",
    demoUrl: "",
    notes: ""
  }};

  projectsData.unshift(newProj);
  saveProjects();
  renderProjects();
  updateMetrics();
  if (typeof showToast === "function") showToast("Novo projeto adicionado!");
}}

function toggleTheme() {{
  const html = document.documentElement;
  const isDark = html.getAttribute("data-theme") === "dark" || (!html.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
  const next = isDark ? "light" : "dark";
  html.setAttribute("data-theme", next);
  try {{ localStorage.setItem("roteiro-theme", next); }} catch(e) {{}}
}}

try {{
  const savedTheme = localStorage.getItem("roteiro-theme");
  if (savedTheme) document.documentElement.setAttribute("data-theme", savedTheme);
}} catch(e) {{}}

window.addEventListener("DOMContentLoaded", () => {{
  loadProjects();
}});
</script>
</body>
</html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Gerado: {out_path} (Laboratório de Projetos & Portfólio)")
