import json, os, re

# Carregar playlist de inglês limpa
with open('/mnt/c/Users/joao1/Desktop/Roteiro/english_playlist.json', 'r', encoding='utf-8') as f:
    english_playlist = json.load(f)

# ---------------------------------------------------------------------------
# 1. Dados de IA (6 Fases Técnicas - 173 Tópicos)
# ---------------------------------------------------------------------------
from build_ia_data import get_enriched_ia_phases
ia_phases = get_enriched_ia_phases()

# ---------------------------------------------------------------------------
# 2. Dados de Matemática (5 Módulos - 43 Tópicos 100% em Português PT-BR)
# ---------------------------------------------------------------------------
from build_math_data import get_enriched_mat_phases
mat_phases = get_enriched_mat_phases()

# ---------------------------------------------------------------------------
# 3. Dados de Inglês EnglishBay (6 Módulos - 73 Vídeo-Aulas)
# ---------------------------------------------------------------------------
ing_phases = [
    {
        "t": "Módulo 1 · Fundamentos Básicos & Apresentação",
        "d": "2 a 3 semanas (1 aula/dia)",
        "tip": "💡 <b>Dica de Estudo:</b> Repita as frases em voz alta junto com o professor. Anote no seu Caderno de Anotações (📝) o vocabulário novo e as estruturas essenciais de cada aula!",
        "p": "Gravar um áudio de 1 minuto em inglês apresentando seu nome, idade, ocupação e o que você gosta de fazer.",
        "r": "Canal EnglishBay no YouTube · Caderno de Anotações integrado · Prática diária de 25-30 min",
        "g": [
            ["Apresentação & Primeiro Contato", english_playlist[:4]],
            ["Estrutura, Números & Adjetivos", english_playlist[4:7]],
            ["Gostos, Hobbies & Conversação Inicial", english_playlist[7:10]],
            ["Família, Gramática & 25 Verbos Essenciais", english_playlist[10:13]]
        ]
    },
    {
        "t": "Módulo 2 · Rotina Diária, Horas & Preposições",
        "d": "2 a 3 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Domine as preposições IN, ON, AT praticando com os horários e locais da sua rotina real de desenvolvedor.",
        "p": "Escrever um parágrafo descrevendo sua rotina matinal e noturna em inglês usando preposições e horários.",
        "r": "Canal EnglishBay no YouTube · Tabela de preposições no Caderno de Anotações",
        "g": [
            ["Família, Artigos & Rotina", english_playlist[13:16]],
            ["Pronomes & Preposições (IN, ON, AT)", english_playlist[16:19]],
            ["Frequência, Datas & Ações em Andamento", english_playlist[19:22]],
            ["Horas, Verbo Haver & 25 Adjetivos", english_playlist[22:25]]
        ]
    },
    {
        "t": "Módulo 3 · Verbos Modais, Futuro & Pronomes",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Modais como Can, Should e Must aparecem em quase todas as documentações técnicas e reuniões de trabalho.",
        "p": "Listar 5 coisas que você DEVE (must) fazer na sua transição de carreira e 5 coisas que você PODE (can) construir com IA.",
        "r": "Canal EnglishBay no YouTube · Exercícios práticos com textos e áudios",
        "g": [
            ["Capacidade (Can) & Pronomes Oblíquos", english_playlist[25:27]],
            ["Conselhos (Should), Pronomes Reflexivos & Dever (Must)", english_playlist[27:30]],
            ["Perguntas Confusas, Futuro (Will) & Advérbios", english_playlist[30:33]],
            ["Futuro (Going to), Do vs Make & Possibilidades", english_playlist[33:37]]
        ]
    },
    {
        "t": "Módulo 4 · Passado, Hábitos & Comparativos",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Memorize os 25 verbos irregulares mais comuns criando frases sobre seu dia anterior de trabalho e código.",
        "p": "Escrever sobre como era sua vida profissional há 5 anos (usando Used To e Simple Past).",
        "r": "Canal EnglishBay no YouTube · Tabela de verbos irregulares no Caderno de Anotações",
        "g": [
            ["Cortesia (Would like), Comparativos & Desejos", english_playlist[37:40]],
            ["Superlativos, Passado do To Be & Igualdade", english_playlist[40:43]],
            ["Passado Simples & 25 Verbos Irregulares", english_playlist[43:46]],
            ["Poder no Passado (Could), Pronomes & Hábitos (Used to)", english_playlist[46:49]]
        ]
    },
    {
        "t": "Módulo 5 · Estruturas Intermediárias & Conversação",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> Pratique criar hipóteses com Second Conditional (\"If I had more time, I would study more IA\").",
        "p": "Simular uma entrevista técnica respondendo perguntas indiretas e falando sobre hábitos passados vs atuais.",
        "r": "Canal EnglishBay no YouTube · Roteiro de conversação no Caderno de Anotações",
        "g": [
            ["Duração de Tempo & Perguntas sem Auxiliares", english_playlist[49:51]],
            ["Hipóteses (E se...), Auxiliares & Condicionais", english_playlist[51:54]],
            ["Prefixos, Past Continuous & Sufixos", english_playlist[54:57]],
            ["Ofertas, Perguntas Indiretas, Hábitos & Quantificadores", english_playlist[57:61]]
        ]
    },
    {
        "t": "Módulo 6 · Fluência Avançada, Tempos Perfeitos & Voz Passiva",
        "d": "2 semanas",
        "tip": "💡 <b>Dica de Estudo:</b> O Present Perfect é essencial para artigos científicos e documentações (\"We have trained the model on 1B tokens\").",
        "p": "Ler a introdução do paper 'Attention is All You Need' e identificar verbos na voz passiva e no present perfect.",
        "r": "Canal EnglishBay no YouTube · Leituras de documentações técnicas em inglês",
        "g": [
            ["Present Perfect & Infinitivo vs Gerúndio", english_playlist[61:63]],
            ["Ever/Never, Verbos com Infinitivo & Present Perfect Continuous", english_playlist[63:66]],
            ["Verbos com Gerúndio, Past Perfect & Voz Passiva", english_playlist[66:69]],
            ["Third Conditional, Reported Speech, Desejos & Tag Questions", english_playlist[69:73]]
        ]
    }
]

print("Datasets prontos. Gerando páginas...")

# ---------------------------------------------------------------------------
# Estilos CSS Compartilhados
# ---------------------------------------------------------------------------
BASE_SHARED_CSS = """
:root{
  --c1:#06141B;--c2:#11212D;--c3:#253745;--c4:#4A5C6A;--c5:#9BA8AB;--c6:#CCD0CF;
  --bg:#06141B;--card:#11212D;--tx:#CCD0CF;--mu:#9BA8AB;--bd:#253745;--ac:#9BA8AB;--ac-hover:#CCD0CF;
  --z:#e5484d;--r:#e8a100;--e:#2fa36b;
  box-sizing:border-box;
  color-scheme:dark;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#06141B;--card:#11212D;--tx:#CCD0CF;--mu:#9BA8AB;--bd:#253745;--ac:#9BA8AB;--ac-hover:#CCD0CF;
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#06141B;--card:#11212D;--tx:#CCD0CF;--mu:#9BA8AB;--bd:#253745;--ac:#9BA8AB;--ac-hover:#CCD0CF;
  color-scheme:dark;
}
:root[data-theme="light"]{
  --bg:#edf1f2;--card:#ffffff;--tx:#06141B;--mu:#4A5C6A;--bd:#CCD0CF;--ac:#253745;--ac-hover:#11212D;
  color-scheme:light;
}
html{scroll-padding-top:70px;scroll-behavior:smooth}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}

/* Topbar Sticky de Navegação */
.top-nav{
  position:sticky;
  top:0;
  z-index:100;
  background:rgba(17,33,45,.92);
  backdrop-filter:blur(10px);
  -webkit-backdrop-filter:blur(10px);
  border-bottom:1px solid var(--bd);
  transition:background .2s;
}
:root[data-theme="light"] .top-nav{background:rgba(255,255,255,.92)}

.top-nav-inner{
  max-width:1440px;
  margin:0 auto;
  padding:0 22px;
  height:58px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
}
.nav-brand{
  display:flex;
  align-items:center;
  gap:8px;
  font-weight:800;
  font-size:1.05rem;
  color:var(--tx);
  text-decoration:none;
}
.nav-brand span{
  background:linear-gradient(135deg,#CCD0CF,#9BA8AB);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}
.nav-links{
  display:flex;
  align-items:center;
  gap:6px;
  overflow-x:auto;
}
.nav-links::-webkit-scrollbar{display:none}
.nav-link{
  font-size:.84rem;
  font-weight:600;
  padding:7px 12px;
  border-radius:8px;
  color:var(--mu);
  text-decoration:none;
  display:inline-flex;
  align-items:center;
  gap:6px;
  white-space:nowrap;
  transition:.15s;
}
.nav-link:hover{color:var(--tx);background:var(--bg)}
.nav-link.active{color:#CCD0CF;background:rgba(155,168,171,.15);border:1px solid rgba(155,168,171,.25);font-weight:700}

.nav-right{display:flex;align-items:center;gap:8px}
.nav-status-pill{
  font-size:.72rem;
  font-weight:600;
  padding:3px 8px;
  border-radius:99px;
  background:var(--bd);
  color:var(--mu);
}
.badge-pg{background:#0064a5;color:#fff}
.badge-sq{background:#003b57;color:#fff}
.nav-theme-btn{
  font:inherit;
  border:1px solid var(--bd);
  background:var(--card);
  color:var(--tx);
  padding:5px 9px;
  border-radius:8px;
  cursor:pointer;
  font-size:.9rem;
}

/* Layout com Sidebar */
.layout{display:flex;min-height:calc(100vh - 58px)}
.sidebar{
  width:320px;
  flex-shrink:0;
  background:var(--card);
  border-right:1px solid var(--bd);
  position:sticky;
  top:58px;
  height:calc(100vh - 58px);
  overflow-y:auto;
  padding:16px 14px;
  display:flex;
  flex-direction:column;
  gap:12px;
  z-index:90;
  transition:transform .25s cubic-bezier(0.16, 1, 0.3, 1),width .25s ease;
}
.sidebar::-webkit-scrollbar{width:5px}
.sidebar::-webkit-scrollbar-thumb{background:var(--bd);border-radius:10px}

.sb-header{display:flex;align-items:center;justify-content:space-between;padding-bottom:10px;border-bottom:1px solid var(--bd)}
.sb-header-title{font-weight:750;font-size:.92rem;color:var(--tx);display:flex;align-items:center;gap:6px}
.sb-shortcuts{display:grid;grid-template-columns:1fr;gap:4px}
.sb-quick-btn{font:inherit;font-size:.78rem;padding:6px 10px;border-radius:8px;border:1px solid transparent;background:var(--bg);color:var(--tx);cursor:pointer;text-align:left;display:flex;align-items:center;gap:6px;transition:.15s}
.sb-quick-btn:hover{border-color:var(--ac);color:var(--ac)}

.sb-tree{display:flex;flex-direction:column;gap:6px;margin-top:6px}
details.sb-phase{border-radius:8px;background:transparent}
details.sb-phase summary{list-style:none;cursor:pointer;padding:7px 9px;border-radius:8px;display:flex;align-items:center;justify-content:space-between;gap:6px;font-size:.82rem;font-weight:650;color:var(--tx);transition:.15s}
details.sb-phase summary::-webkit-details-marker{display:none}
details.sb-phase summary:hover{background:var(--bg)}
details.sb-phase.active-phase summary{background:rgba(74,92,106,.25);color:var(--tx)}
.sb-phase-title{display:flex;align-items:center;gap:6px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sb-badge-count{font-size:.7rem;padding:1px 6px;border-radius:99px;background:var(--bd);color:var(--mu);font-weight:600;flex-shrink:0}

.sb-sub-list{display:flex;flex-direction:column;gap:2px;padding:4px 0 6px 14px;margin-left:8px;border-left:1px solid var(--bd)}
.sb-sub-btn{
  font:inherit;
  font-size:.76rem;
  padding:5px 8px;
  border-radius:6px;
  border:none;
  background:transparent;
  color:var(--mu);
  text-align:left;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:6px;
  transition:.15s;
}
.sb-sub-btn:hover{background:var(--bg);color:var(--tx)}
.sb-sub-btn.active-group{color:#CCD0CF;font-weight:600;background:rgba(74,92,106,.2)}

/* Botão Mobile da Sidebar */
.sb-toggle-btn{
  position:fixed;
  bottom:20px;
  right:20px;
  z-index:95;
  background:linear-gradient(135deg,#253745,#4A5C6A);
  color:#CCD0CF;
  border:1px solid rgba(155,168,171,.3);
  border-radius:99px;
  padding:10px 18px;
  font:inherit;
  font-size:.85rem;
  font-weight:650;
  display:none;
  align-items:center;
  gap:8px;
  cursor:pointer;
  box-shadow:0 4px 18px rgba(6,20,27,.6);
}
.sb-backdrop{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);backdrop-filter:blur(3px);z-index:85}
.sb-backdrop.active{display:block}

@media(max-width:1040px){
  .sidebar{position:fixed;left:0;top:58px;bottom:0;transform:translateX(-100%);box-shadow:6px 0 28px rgba(0,0,0,.25)}
  .sidebar.open{transform:translateX(0)}
  .sb-toggle-btn{display:flex}
}

/* Área de Conteúdo */
.content-wrapper{flex:1;min-width:0;display:flex;flex-direction:column}
main{max-width:1260px;width:100%;margin:0 auto;padding:26px 24px 90px}
.hero-head{margin-bottom:20px}
.hero-head h1{font-size:1.75rem;margin:0 0 6px;font-weight:800;letter-spacing:-.02em}
.hero-head .sub{color:var(--mu);margin:0;font-size:.95rem}

/* Animação de Scroll */
@keyframes highlightHeading {
  0% { background: transparent; }
  25% { background: rgba(74, 92, 106, 0.35); color: var(--tx); padding-left: 8px; border-radius: 6px; }
  75% { background: rgba(74, 92, 106, 0.35); color: var(--tx); padding-left: 8px; border-radius: 6px; }
  100% { background: transparent; padding-left: 0; }
}
.target-highlight {
  animation: highlightHeading 1.8s ease-in-out;
  transition: all .2s ease;
}

/* Rastreador de Metas / Gamificação */
.tracker-box{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:16px;
  padding:20px 22px;
  margin-bottom:22px;
  box-shadow:0 6px 20px rgba(0,0,0,.03);
}
.tracker-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
.tracker-title{font-size:1.02rem;font-weight:750;color:var(--tx);display:flex;align-items:center;gap:8px}
.tracker-presets{display:flex;flex-wrap:wrap;gap:6px}
.trk-btn{font:inherit;font-size:.78rem;padding:5px 12px;border-radius:99px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer;transition:.15s}
.trk-btn:hover{border-color:var(--ac);color:var(--ac)}
.trk-btn.active{background:var(--ac);color:#06141B;border-color:var(--ac);font-weight:700}

.level-banner{background:var(--bg);border:1px solid var(--bd);border-radius:12px;padding:12px 16px;margin-bottom:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px}
.level-info{display:flex;align-items:center;gap:10px}
.level-icon{font-size:1.6rem}
.level-name{font-weight:750;font-size:.92rem;color:var(--tx)}
.level-desc{font-size:.78rem;color:var(--mu);margin-top:1px}
.level-xp-wrap{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex:1 1 200px}
.level-xp-text{font-size:.78rem;font-weight:600;color:var(--ac)}
.level-xp-bar{width:100%;max-width:220px;height:6px;background:var(--bd);border-radius:99px;overflow:hidden}
.level-xp-fill{height:100%;background:linear-gradient(90deg,#4A5C6A,#9BA8AB);border-radius:99px;transition:width .4s ease}

.pace-status-card{padding:12px 16px;border-radius:10px;margin-bottom:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;font-size:.88rem;font-weight:600}
.pace-ahead{background:rgba(47,163,107,.12);border:1px solid rgba(47,163,107,.3);color:var(--e)}
.pace-ontrack{background:rgba(74,92,106,.2);border:1px solid rgba(155,168,171,.35);color:#CCD0CF}
.pace-behind{background:rgba(229,72,77,.12);border:1px solid rgba(229,72,77,.3);color:var(--z)}

.next-step-box{background:rgba(37,55,69,.35);border:1px dashed rgba(155,168,171,.4);border-radius:12px;padding:12px 16px;margin-bottom:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px}
.next-step-info{display:flex;flex-direction:column;gap:2px}
.next-step-tag{font-size:.72rem;font-weight:700;letter-spacing:.05em;color:var(--ac);text-transform:uppercase}
.next-step-title{font-size:.88rem;font-weight:650;color:var(--tx)}
.next-step-btn{font:inherit;font-size:.82rem;font-weight:650;padding:8px 16px;border-radius:99px;border:1px solid rgba(155,168,171,.3);background:linear-gradient(135deg,#253745,#4A5C6A);color:#CCD0CF;cursor:pointer;display:flex;align-items:center;gap:6px;box-shadow:0 3px 12px rgba(6,20,27,.5);transition:.2s}
.next-step-btn:hover{transform:translateY(-1px);box-shadow:0 5px 16px rgba(6,20,27,.6);color:#fff}

.pace-stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin-bottom:14px}
.pace-stat-card{background:var(--bg);border:1px solid var(--bd);border-radius:10px;padding:10px 14px;display:flex;flex-direction:column;gap:3px}
.pace-stat-num{font-size:1.15rem;font-weight:750;color:var(--tx)}
.pace-stat-sub{font-size:.74rem;color:var(--mu)}

/* Barra Global de Progresso */
.progress-card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px 18px;margin-bottom:18px}
.progress-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:.86rem;font-weight:650}
.prog-bar{width:100%;height:8px;background:var(--bd);border-radius:99px;overflow:hidden;display:flex}
.p-z{background:var(--z);transition:width .3s}
.p-r{background:var(--r);transition:width .3s}
.p-e{background:var(--e);transition:width .3s}

/* Filtros e Busca */
.filter-row{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-bottom:18px}
.filters{display:flex;flex-wrap:wrap;gap:6px}
.fil-btn{font:inherit;font-size:.78rem;padding:5px 12px;border-radius:99px;border:1px solid var(--bd);background:var(--card);color:var(--tx);cursor:pointer;transition:.15s}
.fil-btn:hover{border-color:var(--ac)}
.fil-btn.active{background:var(--ac);color:#06141B;border-color:var(--ac);font-weight:700}
.search-input{font:inherit;font-size:.82rem;padding:6px 12px;border-radius:99px;border:1px solid var(--bd);background:var(--card);color:var(--tx);min-width:220px}
.search-input:focus{outline:none;border-color:var(--ac)}

/* Cards das Fases */
.phase-card{background:var(--card);border:1px solid var(--bd);border-radius:14px;margin-bottom:16px;overflow:hidden}
.phase-head{padding:14px 18px;background:var(--bg);border-bottom:1px solid var(--bd);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;cursor:pointer}
.phase-title-text{font-size:1.02rem;font-weight:750;color:var(--tx);display:flex;align-items:center;gap:8px}
.phase-dur{font-size:.74rem;padding:3px 10px;border-radius:99px;background:var(--bd);color:var(--mu);font-weight:600}
.phase-body{padding:18px}
.phase-callout{padding:10px 14px;border-radius:8px;font-size:.82rem;margin-bottom:12px}
.callout-tip{background:rgba(37,55,69,.35);border-left:3px solid var(--ac);color:var(--tx)}
.callout-proj{background:rgba(47,163,107,.08);border-left:3px solid var(--e);color:var(--tx)}
.callout-res{background:var(--bg);border:1px solid var(--bd);color:var(--mu);font-size:.8rem}

.group-section{margin-top:16px}
.group-title{font-size:.88rem;font-weight:750;color:var(--ac);text-transform:uppercase;letter-spacing:.04em;margin:0 0 8px;padding-bottom:4px;border-bottom:1px solid var(--bd);display:flex;align-items:center;gap:6px}

/* Linha de Tópico / Aula */
.topic-row{
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:8px 14px;
  padding:10px 14px;
  border-radius:10px;
  margin-bottom:6px;
  background:var(--bg);
  border:1px solid transparent;
  transition:.15s;
}
.topic-row:hover{border-color:var(--bd)}
.topic-row.status-e{background:rgba(47,163,107,.06);border-color:rgba(47,163,107,.2)}
.topic-row.status-r{background:rgba(232,161,0,.06);border-color:rgba(232,161,0,.25)}
.topic-row.status-z{background:var(--bg)}

.topic-left{
  display:flex;
  align-items:center;
  gap:10px;
  flex:1 1 280px;
  min-width:0;
}
.topic-title-text{
  font-size:.88rem;
  font-weight:550;
  color:var(--tx);
  line-height:1.45;
}
.topic-actions{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  gap:6px;
  flex-shrink:0;
  flex-wrap:wrap;
  margin-left:auto;
}

/* Botões de Ação do Tópico */
.status-btn{
  font:inherit;
  font-size:.76rem;
  font-weight:650;
  padding:4px 10px;
  border-radius:99px;
  border:1px solid transparent;
  cursor:pointer;
  transition:.15s;
  display:inline-flex;
  align-items:center;
  gap:4px;
  white-space:nowrap;
}
.status-btn-z{background:rgba(229,72,77,.1);color:var(--z);border-color:rgba(229,72,77,.25)}
.status-btn-r{background:rgba(232,161,0,.12);color:var(--r);border-color:rgba(232,161,0,.35)}
.status-btn-e{background:rgba(47,163,107,.12);color:var(--e);border-color:rgba(47,163,107,.3)}

.note-btn{
  font:inherit;
  font-size:.76rem;
  padding:4px 8px;
  border-radius:6px;
  border:1px solid var(--bd);
  background:var(--card);
  color:var(--mu);
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:4px;
  transition:.15s;
  white-space:nowrap;
}
.note-btn:hover{color:var(--tx);border-color:var(--ac)}
.note-btn.has-notes{color:#CCD0CF;border-color:var(--ac);background:rgba(74,92,106,.25);font-weight:600}

.yt-btn{
  font:inherit;
  font-size:.74rem;
  font-weight:650;
  padding:4px 9px;
  border-radius:6px;
  border:none;
  background:#cc0000;
  color:#fff;
  text-decoration:none;
  display:inline-flex;
  align-items:center;
  gap:4px;
  box-shadow:0 2px 6px rgba(204,0,0,.25);
  transition:.15s;
}
.yt-btn:hover{background:#e60000;transform:translateY(-1px)}

.doc-btn{
  font:inherit;
  font-size:.74rem;
  font-weight:650;
  padding:4px 9px;
  border-radius:6px;
  border:1px solid rgba(79,70,229,.3);
  background:rgba(79,70,229,.08);
  color:var(--ac);
  text-decoration:none;
  display:inline-flex;
  align-items:center;
  gap:4px;
  transition:.15s;
  white-space:nowrap;
}
.doc-btn:hover{background:var(--ac);color:#fff;transform:translateY(-1px)}

/* =========================================================================
   MODAL DE ANOTAÇÕES (MARKDOWN, TABELAS, CÓDIGO)
   ========================================================================= */
.note-modal-overlay{
  position:fixed;
  inset:0;
  background:rgba(0,0,0,.72);
  backdrop-filter:blur(6px);
  -webkit-backdrop-filter:blur(6px);
  z-index:999;
  display:none; /* Invisível por padrão */
  align-items:center;
  justify-content:center;
  padding:16px;
  animation:noteFadeIn .2s ease;
}
.note-modal-overlay.active{
  display:flex !important;
}
.note-modal-overlay[hidden]{
  display:none !important;
}
@keyframes noteFadeIn{from{opacity:0;transform:scale(.98)}to{opacity:1;transform:scale(1)}}
.note-modal-box{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:16px;
  width:100%;
  max-width:1080px;
  height:90vh;
  max-height:860px;
  display:flex;
  flex-direction:column;
  box-shadow:0 24px 60px rgba(0,0,0,.45);
  overflow:hidden;
}
.note-modal-header{
  padding:14px 20px;
  border-bottom:1px solid var(--bd);
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  background:var(--card);
}
.note-header-left{display:flex;flex-direction:column;gap:2px}
.note-breadcrumb{font-size:.72rem;font-weight:600;color:var(--mu);text-transform:uppercase;letter-spacing:.04em}
.note-topic-title{font-size:1.05rem;font-weight:750;color:var(--tx);margin:0}
.note-header-right{display:flex;align-items:center;gap:10px}
.note-status-wrap{display:flex;align-items:center;gap:6px;font-size:.78rem;color:var(--mu)}
.note-status-pill{font:inherit;font-size:.76rem;font-weight:650;padding:4px 10px;border-radius:99px;border:1px solid var(--bd);background:var(--bg);color:var(--tx);cursor:pointer}
.note-date-wrap{display:flex;align-items:center;gap:6px;font-size:.78rem;color:var(--mu)}
.note-date-wrap input{font:inherit;font-size:.76rem;padding:3px 8px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--tx)}
.note-close-btn{font:inherit;font-size:1.1rem;border:none;background:transparent;color:var(--mu);cursor:pointer;padding:4px 8px;border-radius:6px}
.note-close-btn:hover{background:var(--bg);color:var(--tx)}

.note-toolbar{
  padding:8px 16px;
  background:var(--bg);
  border-bottom:1px solid var(--bd);
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:8px;
}
.toolbar-group{display:flex;align-items:center;gap:4px;flex-wrap:wrap}
.tb-btn{font:inherit;font-size:.76rem;padding:5px 8px;border-radius:6px;border:1px solid var(--bd);background:var(--card);color:var(--tx);cursor:pointer;display:inline-flex;align-items:center;gap:4px}
.tb-btn:hover{border-color:var(--ac);color:var(--ac)}
.tb-sep{width:1px;height:18px;background:var(--bd);margin:0 2px}
.tb-select{font:inherit;font-size:.76rem;padding:4px 8px;border-radius:6px;border:1px solid var(--bd);background:var(--card);color:var(--tx)}
.toolbar-modes{display:flex;align-items:center;gap:3px}
.tb-mode-btn{font:inherit;font-size:.74rem;padding:4px 8px;border-radius:6px;border:1px solid transparent;background:transparent;color:var(--mu);cursor:pointer}
.tb-mode-btn.active{background:var(--card);border-color:var(--bd);color:var(--tx);font-weight:600}

.note-workspace{display:flex;flex:1;min-height:0;overflow:hidden}
.note-editor-pane{flex:1;display:flex;flex-direction:column;border-right:1px solid var(--bd)}
.note-editor-pane textarea{width:100%;height:100%;resize:none;border:none;outline:none;padding:16px 20px;font:14px/1.65 ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;background:transparent;color:var(--tx)}
.note-preview-pane{flex:1;overflow-y:auto;padding:18px 22px;background:var(--card)}
.preview-header{font-size:.74rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--mu);margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid var(--bd)}
.preview-body{font-size:.92rem;line-height:1.65;color:var(--tx)}

.mode-editor .note-preview-pane{display:none}
.mode-editor .note-editor-pane{border-right:none}
.mode-preview .note-editor-pane{display:none}

.note-modal-footer{
  padding:10px 18px;
  background:var(--card);
  border-top:1px solid var(--bd);
  display:flex;
  flex-wrap:wrap;
  align-items:center;
  justify-content:space-between;
  gap:10px;
}
.footer-stats{font-size:.76rem;color:var(--mu)}
.footer-sync{font-size:.76rem;color:var(--e);font-weight:600}
.footer-actions{display:flex;align-items:center;gap:8px}
.note-clear-btn{font:inherit;font-size:.78rem;padding:5px 10px;border-radius:6px;border:1px solid var(--bd);background:var(--bg);color:var(--mu);cursor:pointer}
.note-save-btn{font:inherit;font-size:.8rem;font-weight:650;padding:6px 14px;border-radius:8px;border:none;background:var(--ac);color:#fff;cursor:pointer}

/* Formatação do Preview Markdown */
.note-table-wrap{overflow-x:auto;margin:12px 0}
.note-table{width:100%;border-collapse:collapse;font-size:.85rem}
.note-table th,.note-table td{border:1px solid var(--bd);padding:8px 12px;text-align:left}
.note-table th{background:var(--bg);font-weight:700}
.note-code-block{background:var(--bg);border:1px solid var(--bd);border-radius:8px;margin:12px 0;overflow:hidden}
.code-header{display:flex;justify-content:space-between;align-items:center;padding:5px 12px;border-bottom:1px solid var(--bd);background:rgba(0,0,0,.03);font-size:.72rem;color:var(--mu)}
.copy-code-btn{font:inherit;font-size:.7rem;border:none;background:transparent;color:var(--ac);cursor:pointer}
.note-code-block pre{margin:0;padding:12px 14px;font:13px/1.55 ui-monospace,SFMono-Regular,monospace;overflow-x:auto}
.note-checklist{list-style:none;padding-left:0;margin:10px 0}
.note-todo{display:flex;align-items:center;gap:8px;margin:4px 0}
.note-todo.done{text-decoration:line-through;color:var(--mu)}
.note-quote{border-left:4px solid var(--ac);background:rgba(79,70,229,.07);padding:8px 12px;margin:10px 0;border-radius:0 6px 6px 0}
.empty-notes-hint{color:var(--mu);font-style:italic;padding:30px 10px;text-align:center}


"""

from studio_css import STUDIO_CSS
SHARED_CSS = BASE_SHARED_CSS + "\n" + STUDIO_CSS

from auth_aws_sync import AUTH_AWS_SYNC_CSS, AWS_SYNC_MODAL_HTML, CHANGE_CREDENTIALS_MODAL_HTML, FORGOT_PASSWORD_MODAL_HTML, AUTH_AWS_SYNC_JS
from projects_generator import generate_projects_page
from hub_journey import JOURNEY_CSS, JOURNEY_HTML, JOURNEY_JS_A, JOURNEY_JS_B

print("SHARED_CSS pronto.")

from listing_generator import generate_listing_page as _gen_listing_page

def generate_listing_page(track_id, page_title, page_sub, track_icon, phases, out_path, is_english=False, shared_css=None):
    if shared_css is None:
        shared_css = SHARED_CSS
    return _gen_listing_page(
        track_id=track_id,
        page_title=page_title,
        page_sub=page_sub,
        track_icon=track_icon,
        phases=phases,
        out_path=out_path,
        shared_css=shared_css,
        is_english=is_english
    )

print("Listing page generator pronto (conectado ao listing_generator modular).")

def generate_hub_page(out_path):
    hub_css = SHARED_CSS + "\n" + AUTH_AWS_SYNC_CSS + """
/* =========================================================================
   PORTAL DE LOGIN & ACESSO RESTRITO
   ========================================================================= */
.portal-login-wrap {
  max-width: 520px;
  margin: 50px auto 80px;
  padding: 0 16px;
}
.portal-card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 24px;
  padding: 38px 42px;
  box-shadow: 0 20px 60px rgba(6,20,27,.6), 0 0 40px rgba(37,55,69,.25);
  text-align: center;
  position: relative;
  overflow: hidden;
}
.portal-badge {
  display: inline-block;
  background: rgba(74,92,106,.25);
  border: 1px solid rgba(155,168,171,.3);
  color: #CCD0CF;
  font-size: .8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .05em;
  padding: 6px 14px;
  border-radius: 99px;
  margin-bottom: 14px;
}
.portal-title {
  font-size: 2.1rem;
  font-weight: 850;
  margin: 0 0 10px;
  color: var(--tx);
  letter-spacing: -.02em;
}
.portal-subtitle {
  font-size: 1rem;
  color: var(--mu);
  max-width: 560px;
  margin: 0 auto 28px;
  line-height: 1.55;
}
.portal-form {
  max-width: 440px;
  margin: 0 auto;
  text-align: left;
}
.portal-input-group {
  margin-bottom: 18px;
}
.portal-label {
  display: block;
  font-size: .82rem;
  font-weight: 750;
  color: var(--tx);
  margin-bottom: 6px;
}
.portal-input {
  width: 100%;
  padding: 13px 16px;
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 12px;
  color: var(--tx);
  font-size: .95rem;
  box-sizing: border-box;
  transition: all .2s;
}
.portal-input:focus {
  outline: none;
  border-color: #9BA8AB;
  box-shadow: 0 0 0 3px rgba(155,168,171,.2);
}
.portal-remember-row {
  margin-bottom: 22px;
}
.portal-submit-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #253745, #4A5C6A);
  color: #CCD0CF;
  border: 1px solid rgba(155,168,171,.35);
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(6,20,27,.4);
  transition: all .2s;
}
.portal-submit-btn:hover {
  filter: brightness(1.15);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(6,20,27,.6);
  color: #fff;
}
.portal-error-msg {
  background: rgba(239,68,68,.12);
  border: 1px solid rgba(239,68,68,.3);
  color: #ef4444;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: .84rem;
  margin-bottom: 16px;
  text-align: center;
}

/* Hub Cards e Seções Específicas */
.hub-main{max-width:1260px;margin:0 auto;padding:32px 24px 100px}
.hub-hero{text-align:center;margin-bottom:34px}
.hub-hero h1{font-size:2.2rem;font-weight:850;letter-spacing:-.03em;margin:0 0 10px;background:linear-gradient(135deg,#CCD0CF 40%,#9BA8AB);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hub-hero p{font-size:1.08rem;color:var(--mu);max-width:760px;margin:0 auto}

/* Card de Esclarecimento sobre Metas & Inglês */
.clarification-card{
  background:linear-gradient(135deg,rgba(37,55,69,.4),rgba(74,92,106,.2));
  border:1px solid var(--bd);
  border-radius:18px;
  padding:24px 28px;
  margin-bottom:32px;
  box-shadow:0 8px 24px rgba(6,20,27,.3);
}
.clarification-head{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.clarification-badge{background:#253745;color:#CCD0CF;border:1px solid rgba(155,168,171,.3);font-size:.76rem;font-weight:750;padding:4px 10px;border-radius:99px;text-transform:uppercase;letter-spacing:.04em}
.clarification-title{font-size:1.25rem;font-weight:800;color:var(--tx)}
.clarification-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:16px}
.clarification-col{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px 18px}
.clarification-col h4{margin:0 0 8px;font-size:.95rem;font-weight:750;color:var(--tx);display:flex;align-items:center;gap:6px}
.clarification-col p{margin:0;font-size:.86rem;line-height:1.55;color:var(--mu)}
.clarification-col b{color:var(--tx)}

/* =========================================================================
   COCKPIT NEURAL DE TELEMETRIA 360°, VELOCÍMETRO SVG & SIMULADOR PREDITIVO
   ========================================================================= */
.speedometer-sect {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 22px;
  padding: 26px 28px;
  margin-bottom: 36px;
  box-shadow: 0 14px 40px rgba(6,20,27,.4);
  position: relative;
  overflow: hidden;
}

.speed-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--bd);
  margin-bottom: 16px;
}

.speed-title-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.speed-title-icon {
  width: 44px;
  height: 44px;
  border-radius: 13px;
  background: linear-gradient(135deg, rgba(37,55,69,.5), rgba(74,92,106,.3));
  border: 1px solid var(--bd);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  flex-shrink: 0;
}

.speed-title {
  font-size: 1.18rem;
  font-weight: 850;
  color: var(--tx);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  letter-spacing: -.01em;
}

.speed-subtitle {
  font-size: .8rem;
  color: var(--mu);
  margin-top: 2px;
  font-weight: 500;
}

.speed-presets-wrap {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  background: var(--bg);
  padding: 5px 7px;
  border-radius: 99px;
  border: 1px solid var(--bd);
}

.speed-preset-btn {
  font: inherit;
  font-size: .78rem;
  font-weight: 700;
  padding: 6px 13px;
  border-radius: 99px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--mu);
  cursor: pointer;
  transition: all .18s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.speed-preset-btn:hover {
  color: var(--tx);
}

.speed-preset-btn.active {
  background: linear-gradient(135deg, var(--ac), #7c3aed);
  border-color: rgba(255,255,255,.15);
  color: #fff;
  box-shadow: 0 3px 12px rgba(79,70,229,.35);
}

/* Barra de Controles Secundária: Modos de Visão + Data de Início + Modo Demo */
.cockpit-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.cockpit-view-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  background: var(--bg);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid var(--bd);
}

.cockpit-tab-btn {
  font: inherit;
  font-size: .76rem;
  font-weight: 750;
  padding: 6px 12px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: var(--mu);
  cursor: pointer;
  transition: all .18s ease;
}

.cockpit-tab-btn:hover {
  color: var(--tx);
}

.cockpit-tab-btn.active {
  background: var(--card);
  color: var(--ac);
  box-shadow: 0 2px 8px rgba(0,0,0,.08);
  border: 1px solid rgba(155,168,171,.35);
}

.speed-date-inputs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  font-size: .8rem;
}

.speed-date-inputs label {
  color: var(--mu);
  font-weight: 650;
  display: flex;
  align-items: center;
  gap: 5px;
}

.speed-date-input {
  font: inherit;
  font-size: .78rem;
  font-weight: 650;
  padding: 5px 10px;
  border-radius: 8px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
  outline: none;
}

.speed-date-input:focus {
  border-color: var(--ac);
}

.speed-reset-btn {
  font: inherit;
  font-size: .75rem;
  font-weight: 700;
  padding: 5px 11px;
  border-radius: 8px;
  border: 1px solid var(--bd);
  background: var(--bg);
  color: var(--tx);
  cursor: pointer;
  transition: .15s;
}

.speed-reset-btn:hover {
  border-color: var(--ac);
  color: var(--ac);
}

.speed-demo-btn {
  font: inherit;
  font-size: .75rem;
  font-weight: 750;
  padding: 5px 12px;
  border-radius: 8px;
  border: 1px solid rgba(6,182,212,.4);
  background: rgba(6,182,212,.1);
  color: #06b6d4;
  cursor: pointer;
  transition: .18s;
}

.speed-demo-btn:hover, .speed-demo-btn.active {
  background: #06b6d4;
  color: #fff;
  box-shadow: 0 3px 12px rgba(6,182,212,.3);
}

/* Painel Expansível de Simulação de Dados (Modo Test-Drive) */
.cockpit-demo-drawer {
  display: none;
  background: linear-gradient(135deg, rgba(6,182,212,.08), rgba(79,70,229,.08));
  border: 1px dashed rgba(6,182,212,.45);
  border-radius: 14px;
  padding: 14px 18px;
  margin-bottom: 18px;
}

.cockpit-demo-drawer.open {
  display: block;
}

.cockpit-demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin-top: 10px;
}

.cockpit-demo-ctrl label {
  display: flex;
  justify-content: space-between;
  font-size: .76rem;
  font-weight: 750;
  color: var(--tx);
  margin-bottom: 4px;
}

.cockpit-demo-ctrl input[type="range"] {
  width: 100%;
  accent-color: var(--ac);
  cursor: pointer;
}

/* MÓDULO 1: GRADE PRINCIPAL DE TELEMETRIA (TACÔMETRO + ANÉIS + KPIs) */
.cockpit-main-grid {
  display: grid;
  grid-template-columns: 1.25fr 1.15fr 0.9fr;
  gap: 16px;
  margin-bottom: 18px;
}

@media (max-width: 1080px) {
  .cockpit-main-grid {
    grid-template-columns: 1fr 1fr;
  }
  .cockpit-kpi-col {
    grid-column: span 2;
    display: grid !important;
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 720px) {
  .cockpit-main-grid {
    grid-template-columns: 1fr;
  }
  .cockpit-kpi-col {
    grid-column: span 1;
    grid-template-columns: 1fr !important;
  }
}

.cockpit-panel {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.cockpit-panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}

.cockpit-panel-title {
  font-size: .8rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .04em;
  color: var(--mu);
  display: flex;
  align-items: center;
  gap: 6px;
}

.speed-gauge-multiplier {
  font-size: .75rem;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 99px;
  background: rgba(79,70,229,.14);
  color: var(--ac);
  border: 1px solid rgba(79,70,229,.3);
  white-space: nowrap;
}

/* Tacômetro SVG */
.tachometer-svg-wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 4px 0 6px;
}

.tachometer-needle {
  transition: transform .65s cubic-bezier(.34,1.56,.64,1);
  transform-origin: 140px 140px;
}

.tachometer-readout {
  text-align: center;
  margin-top: -12px;
}

.tachometer-big-val {
  font-size: 1.65rem;
  font-weight: 900;
  color: var(--tx);
  line-height: 1.1;
}

.tachometer-sub-val {
  font-size: .76rem;
  font-weight: 650;
  color: var(--mu);
  margin-top: 2px;
}

.tachometer-mini-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--bd);
}

.tachometer-mini-box {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 10px;
  padding: 8px 10px;
  text-align: center;
}

.tachometer-mini-lbl {
  font-size: .68rem;
  font-weight: 750;
  text-transform: uppercase;
  color: var(--mu);
}

.tachometer-mini-num {
  font-size: .92rem;
  font-weight: 850;
  color: var(--tx);
  margin-top: 2px;
}

/* Anéis Concêntricos Multi-Trilha */
.rings-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin: 8px 0;
}

@media (max-width: 480px) {
  .rings-layout {
    flex-direction: column;
  }
}

.rings-svg-box {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ring-progress-circle {
  transition: stroke-dashoffset .65s cubic-bezier(.22,1,.36,1);
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
}

.rings-center-label {
  position: absolute;
  text-align: center;
  pointer-events: none;
}

.rings-center-num {
  font-size: 1.25rem;
  font-weight: 900;
  color: var(--tx);
  line-height: 1;
}

.rings-center-sub {
  font-size: .66rem;
  font-weight: 700;
  color: var(--mu);
}

.rings-legend-list {
  display: flex;
  flex-direction: column;
  gap: 7px;
  flex: 1;
  width: 100%;
}

.rings-legend-item {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 10px;
  padding: 7px 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: .76rem;
  text-decoration: none;
  color: var(--tx);
  transition: transform .15s, border-color .15s;
}

.rings-legend-item:hover {
  transform: translateX(3px);
  border-color: var(--ac);
}

/* Coluna de KPIs Preditivos */
.cockpit-kpi-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.speed-metric-box {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 14px;
  padding: 13px 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 3px;
  flex: 1;
}

.speed-metric-lbl {
  font-size: .72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .04em;
  color: var(--mu);
  display: flex;
  align-items: center;
  gap: 5px;
}

.speed-metric-val {
  font-size: 1.32rem;
  font-weight: 900;
  color: var(--tx);
  line-height: 1.2;
}

.speed-metric-sub {
  font-size: .75rem;
  font-weight: 650;
  color: var(--mu);
}

/* Card de Diagnóstico Dinâmico ao Vivo */
.speed-diagnosis-card {
  padding: 12px 16px;
  border-radius: 12px;
  margin-bottom: 18px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  font-size: .88rem;
  font-weight: 600;
  line-height: 1.5;
  transition: all .25s ease;
}

.speed-diagnosis-card.pace-ahead {
  background: rgba(47,163,107,.12);
  border: 1px solid rgba(47,163,107,.35);
  color: var(--e);
}

.speed-diagnosis-card.pace-ontrack {
  background: rgba(79,70,229,.1);
  border: 1px solid rgba(79,70,229,.3);
  color: var(--ac);
}

.speed-diagnosis-card.pace-behind {
  background: rgba(229,72,77,.12);
  border: 1px solid rgba(229,72,77,.35);
  color: var(--z);
}

.speed-diag-badge {
  font-size: .76rem;
  font-weight: 850;
  padding: 4px 12px;
  border-radius: 99px;
  background: var(--card);
  border: 1px solid currentColor;
  white-space: nowrap;
  letter-spacing: .02em;
}

/* MÓDULO 2: GRÁFICO BURN-UP DE PROJEÇÃO + SIMULADOR "E SE?" */
.cockpit-chart-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 16px;
  margin-bottom: 18px;
}

@media (max-width: 920px) {
  .cockpit-chart-grid {
    grid-template-columns: 1fr;
  }
}

.burnup-svg {
  width: 100%;
  height: 165px;
  overflow: visible;
  margin-top: 6px;
}

.comp-bars-mini {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--bd);
}

@media (max-width: 560px) {
  .comp-bars-mini {
    grid-template-columns: 1fr;
  }
}

.comp-bar-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: .76rem;
  font-weight: 750;
  color: var(--tx);
}

.comp-bar-track {
  height: 8px;
  background: var(--bd);
  border-radius: 99px;
  overflow: hidden;
  margin-top: 5px;
}

.comp-bar-fill-real {
  height: 100%;
  background: linear-gradient(90deg, #10b981, #06b6d4);
  border-radius: 99px;
  transition: width .4s ease;
}

.comp-bar-fill-target {
  height: 100%;
  background: linear-gradient(90deg, #4A5C6A, #9BA8AB);
  border-radius: 99px;
  transition: width .4s ease;
}

/* Simulador Preditivo "E Se?" */
.whatif-panel {
  background: linear-gradient(155deg, rgba(79,70,229,.09), rgba(6,182,212,.05));
  border: 1px solid rgba(79,70,229,.28);
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.whatif-slider-box {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 12px 14px;
  margin: 10px 0;
}

.whatif-slider-box input[type="range"] {
  width: 100%;
  accent-color: #06b6d4;
  cursor: pointer;
  margin: 6px 0 4px;
}

.whatif-results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.whatif-res-card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 11px;
  padding: 10px 12px;
}

.whatif-res-lbl {
  font-size: .68rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--mu);
}

.whatif-res-val {
  font-size: 1.05rem;
  font-weight: 900;
  color: var(--tx);
  margin-top: 2px;
}

.whatif-res-sub {
  font-size: .72rem;
  font-weight: 700;
  color: #06b6d4;
  margin-top: 1px;
}

/* MÓDULO 3: ESCADA DE PATENTES XP & RADAR DAS 4 PÁGINAS */
.ranks-ladder-card {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 16px;
  padding: 16px 18px;
  margin-bottom: 16px;
}

.ranks-ladder-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
  gap: 10px;
  margin-top: 12px;
}

.rank-step-card {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 10px;
  opacity: .55;
  transition: all .25s ease;
}

.rank-step-card.unlocked {
  opacity: 1;
  border-color: rgba(47,163,107,.45);
  background: rgba(47,163,107,.07);
}

.rank-step-card.current-rank {
  opacity: 1;
  border-color: var(--ac);
  background: linear-gradient(135deg, rgba(79,70,229,.16), rgba(139,92,246,.1));
  box-shadow: 0 4px 16px rgba(79,70,229,.18);
  transform: translateY(-2px);
}

.rank-step-icon {
  font-size: 1.45rem;
  flex-shrink: 0;
}

.rank-step-name {
  font-size: .82rem;
  font-weight: 800;
  color: var(--tx);
}

.rank-step-req {
  font-size: .7rem;
  font-weight: 700;
  color: var(--mu);
}

.rank-step-card.unlocked .rank-step-req {
  color: var(--e);
}

.rank-step-card.current-rank .rank-step-req {
  color: var(--ac);
}

/* Mini Radar das 4 Páginas no Hub */
.hub-radar-card {
  background: var(--bg);
  border: 1px solid var(--bd);
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 16px;
}

.hub-radar-title {
  font-size: .86rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .04em;
  color: var(--mu);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.hub-radar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
}

.hub-radar-item {
  background: var(--card);
  border: 1px solid var(--bd);
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: border-color .2s, transform .2s;
}

.hub-radar-item:hover {
  border-color: var(--ac);
  transform: translateY(-2px);
}

.hub-radar-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.hub-radar-name {
  font-size: .86rem;
  font-weight: 750;
  color: var(--tx);
  display: flex;
  align-items: center;
  gap: 6px;
}

.hub-radar-count {
  font-size: .78rem;
  font-weight: 700;
  color: var(--mu);
}

.hub-radar-bar {
  height: 6px;
  background: var(--bd);
  border-radius: 99px;
  overflow: hidden;
}

.hub-radar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width .4s ease;
}

.hub-radar-link {
  align-self: flex-end;
  font-size: .76rem;
  font-weight: 700;
  color: var(--ac);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.hub-radar-link:hover {
  text-decoration: underline;
}

/* Próximo Passo Sugerido */
.hub-next-box {
  background: linear-gradient(135deg,rgba(37,55,69,.4),rgba(74,92,106,.2));
  border: 1px dashed rgba(155,168,171,.4);
  border-radius: 14px;
  padding: 14px 18px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.hub-next-tag {
  font-size: .7rem;
  font-weight: 750;
  letter-spacing: .05em;
  color: var(--ac);
  text-transform: uppercase;
}

.hub-next-title {
  font-size: .88rem;
  font-weight: 700;
  color: var(--tx);
  margin-top: 2px;
}

.hub-next-action-btn {
  font: inherit;
  font-size: .82rem;
  font-weight: 750;
  padding: 8px 18px;
  border-radius: 99px;
  border: 1px solid rgba(155,168,171,.3);
  background: linear-gradient(135deg, #253745, #4A5C6A);
  color: #CCD0CF;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 3px 12px rgba(6,20,27,.4);
  transition: .2s;
}

.hub-next-action-btn:hover {
  background: linear-gradient(135deg, #4A5C6A, #253745);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 5px 16px rgba(6,20,27,.6);
}

@keyframes hubPulseAnim {
  0% { box-shadow: 0 0 0 0 rgba(155,168,171,.4); }
  70% { box-shadow: 0 0 0 14px rgba(155,168,171,0); }
  100% { box-shadow: 0 0 0 0 rgba(155,168,171,0); }
}
.pulse-update {
  animation: hubPulseAnim .7s ease-out;
}

/* Grade dos 3 Cards Principais de Trilha */
.track-cards-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px;margin-bottom:40px}
.track-card{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:18px;
  padding:26px 24px;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  box-shadow:0 6px 22px rgba(0,0,0,.03);
  transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease;
  position:relative;
  overflow:hidden;
}
.track-card:hover{
  transform:translateY(-4px);
  box-shadow:0 12px 32px rgba(6,20,27,.5);
  border-color:#9BA8AB;
}
.track-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:14px}
.track-card-icon{font-size:2.2rem}
.track-badge-count{font-size:.76rem;font-weight:700;padding:4px 10px;border-radius:99px;background:var(--bg);color:var(--ac);border:1px solid var(--bd)}
.track-card-title{font-size:1.25rem;font-weight:800;color:var(--tx);margin:0 0 8px}
.track-card-desc{font-size:.88rem;color:var(--mu);line-height:1.55;margin:0 0 18px;flex:1}

.track-progress-wrap{margin-bottom:20px;padding-top:14px;border-top:1px solid var(--bd)}
.track-progress-info{display:flex;justify-content:space-between;font-size:.82rem;font-weight:650;color:var(--tx);margin-bottom:6px}
.track-progress-bar{height:7px;background:var(--bd);border-radius:99px;overflow:hidden}
.track-progress-fill{height:100%;border-radius:99px;transition:width .4s}

.track-access-btn{
  font:inherit;
  font-size:.92rem;
  font-weight:750;
  padding:12px 20px;
  border-radius:12px;
  border:1px solid rgba(155,168,171,.35);
  background:linear-gradient(135deg, #253745, #4A5C6A);
  color:#CCD0CF;
  text-decoration:none;
  text-align:center;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  box-shadow:0 4px 14px rgba(6,20,27,.4);
  transition:.2s;
}
.track-access-btn:hover{
  background:linear-gradient(135deg, #4A5C6A, #253745);
  color:#fff;
  border-color:#CCD0CF;
  transform:scale(1.01);
}

/* Contexto Global de Mercado */
.market-box{
  background:var(--card);
  border:1px solid var(--bd);
  border-radius:18px;
  padding:26px 28px;
  box-shadow:0 4px 18px rgba(0,0,0,.02);
}
.market-title{font-size:1.2rem;font-weight:800;color:var(--tx);margin:0 0 10px;display:flex;align-items:center;gap:8px}
.market-desc{font-size:.92rem;line-height:1.65;color:var(--mu);margin-bottom:18px}
.market-stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
.market-stat{background:var(--bg);border:1px solid var(--bd);border-radius:12px;padding:14px 16px}
.market-stat-num{font-size:1.4rem;font-weight:850;color:var(--ac);display:block;margin-bottom:3px}
.market-stat-lbl{font-size:.82rem;color:var(--tx);font-weight:600}
"""

    html_template = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hub Central - Roteiro de Estudo do zero à IA</title>
<style>
__HUB_CSS__
</style>
</head>
<body>

<!-- TOPBAR FIXA -->
<header class="top-nav">
  <div class="top-nav-inner">
    <a href="index.html" class="nav-brand">🚀 <span>Roteiro IA</span></a>
    <nav class="nav-links" id="hub-nav-links">
      <a href="index.html" class="nav-link active">🏠 Hub Central</a>
      <a href="ia.html" class="nav-link">🤖 IA & Código</a>
      <a href="matematica.html" class="nav-link">📐 Matemática</a>
      <a href="ingles.html" class="nav-link">🇺🇸 Inglês EnglishBay</a>
      <a href="projetos.html" class="nav-link">🛠️ Projetos & Portfólio</a>
    </nav>
    <div class="nav-right">
      <div class="nav-user-dropdown-wrap" id="nav-user-wrap">
        <button class="nav-user-pill" onclick="toggleUserDropdown(event)" id="nav-auth-user" title="Menu da Conta">
          👤 <span>João Naziozeno</span> <span style="font-size:.7rem;margin-left:2px">▾</span>
        </button>
        <div class="nav-user-dropdown" id="nav-user-dropdown" hidden style="display:none">
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
      <span id="nav-db-status" class="nav-status-pill" style="display:none">💾 Local</span>
      <button class="nav-theme-btn" onclick="toggleTheme()" title="Alternar tema claro/escuro">🌓</button>
    </div>
  </div>
</header>

<main class="hub-main">
  <!-- ESTADO 1: TELA DE LOGIN / PORTAL DE ACESSO (QUANDO DESCONECTADO) -->
  <div id="hub-login-view" style="display:none">
    <div class="portal-login-wrap">
      <div class="portal-card">
        <div class="portal-badge">🔒 Área Restrita do Estudante</div>
        <h2 class="portal-title">Portal de Acesso · Roteiro de IA</h2>
        <p class="portal-subtitle">Faça login para desbloquear suas trilhas de estudo.</p>
        
        <form id="portal-login-form" onsubmit="handlePortalLogin(event)" class="portal-form">
          <div class="portal-input-group">
            <label class="portal-label">E-mail Cadastrado</label>
            <input type="email" id="login-input-email" class="portal-input" value="joao@roteiro.ia" required placeholder="seu-email@dominio.com">
          </div>

          <div class="portal-input-group">
            <label class="portal-label">Senha</label>
            <input type="password" id="login-input-pass" class="portal-input" required placeholder="Digite sua senha">
          </div>

          <div class="portal-remember-row" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
            <label style="display:flex;align-items:center;gap:7px;cursor:pointer;font-size:.82rem;color:var(--mu);user-select:none">
              <input type="checkbox" id="login-remember-me" checked>
              <span>Lembrar meu acesso</span>
            </label>
            <a href="javascript:void(0)" onclick="openForgotPasswordModal()" class="forgot-pass-link" title="Recuperar senha com código via E-mail (SES) ou WhatsApp">Esqueci minha senha</a>
          </div>

          <div id="login-error-msg" class="portal-error-msg" style="display:none"></div>

          <button type="submit" class="portal-submit-btn">
            🚀 Entrar no Ecossistema de IA ➔
          </button>
        </form>
      </div>
    </div>
  </div>

  <!-- ESTADO 2: CONTEÚDO AUTENTICADO DO HUB (QUANDO CONECTADO) -->
  <div id="hub-authenticated-view" style="display:none">
    <!-- HERO HEAD -->
    <section class="hub-hero">
      <h1>Hub Central de Aprendizado</h1>
      <p>Do zero absoluto até o desenvolvimento e engenharia de Inteligência Artificial moderna. Escolha uma das 4 páginas estruturadas abaixo para gerenciar seus estudos, anotações e progresso.</p>
    </section>

  <!-- =======================================================================
       COCKPIT NEURAL DE TELEMETRIA 360°, VELOCÍMETRO SVG & SIMULADOR PREDITIVO
       ======================================================================= -->
  __JOURNEY_HTML__

  <!-- OS 4 CARDS GRANDES DE REDIRECIONAMENTO -->
  <div style="font-size:1.15rem;font-weight:800;color:var(--tx);margin-bottom:16px;display:flex;align-items:center;gap:8px">
    🎯 Suas 4 Páginas de Aprendizado & Portfólio:
  </div>

  <section class="track-cards-grid">
    <!-- CARD 1: IA & PROGRAMAÇÃO -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">🤖</div>
          <span class="track-badge-count">173 Tópicos · 6 Fases</span>
        </div>
        <h3 class="track-card-title">Inteligência Artificial & Código</h3>
        <p class="track-card-desc">
          Do zero ao domínio técnico completo: Python essencial, Git, consumo de APIs, Pandas, Scikit-learn, PyTorch, Redes Neurais, Transformers, LLMs, Agentes e MLOps.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em IA:</span>
            <span id="card-ia-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-ia-fill" style="width:0%;background:var(--ac)"></div>
          </div>
        </div>
        <a href="ia.html" class="track-access-btn">Acessar Trilha de IA & Programação ➔</a>
      </div>
    </div>

    <!-- CARD 2: MATEMÁTICA PARA IA -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">📐</div>
          <span class="track-badge-count">43 Tópicos · 5 Módulos</span>
        </div>
        <h3 class="track-card-title">Matemática Essencial para IA</h3>
        <p class="track-card-desc">
          Apenas a matemática que você realmente usa: Álgebra Linear com tensores, Cálculo com gradientes e Backpropagation, Probabilidade Bayesiana e Geometria de Embeddings.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em Matemática:</span>
            <span id="card-mat-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-mat-fill" style="width:0%;background:#e8a100"></div>
          </div>
        </div>
        <a href="matematica.html" class="track-access-btn" style="background:#e8a100">Acessar Trilha de Matemática ➔</a>
      </div>
    </div>

    <!-- CARD 3: INGLÊS ENGLISHBAY -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">🇺🇸</div>
          <span class="track-badge-count">73 Aulas · 6 Módulos</span>
        </div>
        <h3 class="track-card-title">Curso de Inglês EnglishBay</h3>
        <p class="track-card-desc">
          Sequência completa e organizada da playlist oficial do YouTube: da apresentação pessoal e estruturas básicas até tempos perfeitos, verbos modais e voz passiva.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em Inglês:</span>
            <span id="card-ing-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-ing-fill" style="width:0%;background:#2fa36b"></div>
          </div>
        </div>
        <a href="ingles.html" class="track-access-btn" style="background:#2fa36b">Acessar Trilha de Inglês ➔</a>
      </div>
    </div>

    <!-- CARD 4: LABORATÓRIO DE PROJETOS & PORTFÓLIO -->
    <div class="track-card">
      <div>
        <div class="track-card-top">
          <div class="track-card-icon">🛠️</div>
          <span class="track-badge-count">6 Projetos · Práticos</span>
        </div>
        <h3 class="track-card-title">Laboratório de Projetos & Portfólio</h3>
        <p class="track-card-desc">
          Construa aplicações reais de IA para o seu currículo: CLI com APIs, Pipeline ETL com PostgreSQL, API de Machine Learning com FastAPI, Classificador CNN com PyTorch, Chatbot RAG com LangChain e Deploy em nuvem com Docker e AWS.
        </p>
      </div>

      <div>
        <div class="track-progress-wrap">
          <div class="track-progress-info">
            <span>Progresso em Projetos:</span>
            <span id="card-proj-pct">0%</span>
          </div>
          <div class="track-progress-bar">
            <div class="track-progress-fill" id="card-proj-fill" style="width:0%;background:#ec4899"></div>
          </div>
        </div>
        <a href="projetos.html" class="track-access-btn" style="background:linear-gradient(135deg,#ec4899,#8b5cf6)">Acessar Laboratório de Projetos ➔</a>
      </div>
    </div>
  </section>

  <!-- CONTEXTO GLOBAL DE MERCADO -->
  <section class="market-box">
    <div class="market-title">🗺️ O Cenário Global do Talento em IA</div>
    <div class="market-desc">
      Dados do <b>Stanford AI Index</b> e do <b>Global AI Talent Tracker</b> (Carnegie/Paulson Institute) mostram que existem hoje cerca de 150.000 a 200.000 pessoas no mundo trabalhando diretamente no desenvolvimento de ponta em IA. Quando incluímos quem cria integrações e aplicações com APIs e modelos abertos, o número salta para a casa dos milhões (mais de 5,6 milhões de repositórios ativos no GitHub e Hugging Face).
      <br><br>
      Quem domina a tríade <b>Código Python + Matemática Aplicada + Inglês Técnico</b> se posiciona imediatamente no percentil mais valorizado do mercado mundial de tecnologia.
    </div>

    <div class="market-stats-grid">
      <div class="market-stat">
        <span class="market-stat-num">34,2% a 59%</span>
        <span class="market-stat-lbl">Talentos de elite empregados nos EUA (OpenAI, Google, Anthropic, Meta)</span>
      </div>
      <div class="market-stat">
        <span class="market-stat-num">40,6%</span>
        <span class="market-stat-lbl">Origem de pesquisadores seniores na China (formação matemática de ponta)</span>
      </div>
      <div class="market-stat">
        <span class="market-stat-num">5,6 Milhões</span>
        <span class="market-stat-lbl">Projetos de IA ativos no ecossistema global do GitHub & Hugging Face</span>
      </div>
      <div class="market-stat">
        <span class="market-stat-num">289 Tópicos</span>
        <span class="market-stat-lbl">Currículo completo deste roteiro cobrindo as 3 habilidades essenciais</span>
      </div>
    </div>
  </section>
  </div> <!-- /#hub-authenticated-view -->
</main>

__AWS_SYNC_MODAL__
__CHANGE_CREDENTIALS_MODAL__
__FORGOT_PASSWORD_MODAL__

<script>
__AUTH_AWS_SYNC_JS__

function checkHubAuth() {
  const user = getLoggedInUser();
  const loginView = document.getElementById("hub-login-view");
  const authView = document.getElementById("hub-authenticated-view");
  const navUserWrap = document.getElementById("nav-user-wrap");
  const navLinks = document.getElementById("hub-nav-links");
  const dbStatus = document.getElementById("nav-db-status");

  if (user && user.authenticated) {
    if (loginView) loginView.style.display = "none";
    if (authView) authView.style.display = "block";
    if (navUserWrap) navUserWrap.style.display = "inline-block";
    if (navLinks) navLinks.style.display = "flex";
    if (dbStatus) dbStatus.style.display = "inline-flex";
    
    const heroH1 = document.querySelector(".hub-hero h1");
    if (heroH1) heroH1.innerHTML = `Painel do Estudante: Rumo à IA 🚀`;
    const heroP = document.querySelector(".hub-hero p");
    if (heroP) heroP.innerHTML = `Bem-vindo de volta, <b>${user.name || "João"}</b>! Suas anotações estão sincronizadas e protegidas na nuvem AWS. Escolha uma das 4 páginas abaixo:`;

    calcAndPaint();
  } else {
    if (loginView) loginView.style.display = "block";
    if (authView) authView.style.display = "none";
    if (navUserWrap) navUserWrap.style.display = "none";
    if (navLinks) navLinks.style.display = "none";
    if (dbStatus) dbStatus.style.display = "none";
  }
}

async function handlePortalLogin(e) {
  e.preventDefault();
  const email = document.getElementById("login-input-email").value.trim();
  const pass = document.getElementById("login-input-pass").value.trim();
  const remember = document.getElementById("login-remember-me").checked;
  const errorEl = document.getElementById("login-error-msg");

  // Validação criptográfica com HASH SHA-256 e Salt
  const isValid = await validateLoginPassword(pass);

  if (isValid) {
    let userName = "João Naziozeno";
    const existing = getLoggedInUser();
    if (existing && existing.name) userName = existing.name;

    const userObj = {
      authenticated: true,
      name: userName,
      email: email || "joao@roteiro.ia",
      loginTime: Date.now(),
      provider: "aws-cognito-ready"
    };

    if (remember) {
      localStorage.setItem("roteiro_auth_user", JSON.stringify(userObj));
    } else {
      sessionStorage.setItem("roteiro_auth_user", JSON.stringify(userObj));
    }

    if (errorEl) errorEl.style.display = "none";

    const redirectUrl = sessionStorage.getItem("roteiro_redirect_after_login");
    if (redirectUrl) {
      sessionStorage.removeItem("roteiro_redirect_after_login");
      window.location.href = redirectUrl;
      return;
    }

    checkHubAuth();
    updateNavAuthUI();
  } else {
    if (errorEl) {
      errorEl.textContent = "Senha incorreta. Verifique suas credenciais e tente novamente.";
      errorEl.style.display = "block";
    }
  }
}

const KEY = "roteiro-ia-v1";
const PACE_KEY = "roteiro-hub-pace";
const START_KEY = "roteiro-start-date";

let PR = {};
let API_BASE = "http://localhost:8000";

const HUB_PRESETS = {
  sprint: { name: "⚡ Ultra Otimista", months: 4, days: 120, label: "Meta de 4 meses (Sprint intensivo)" },
  optimistic: { name: "🚀 Otimista Acelerado", months: 6, days: 180, label: "Meta de 6 meses (Ritmo acelerado)" },
  standard: { name: "🎯 Equilibrado Sustentável", months: 14, days: 420, label: "Meta de 14 meses (Sustentável)" }
};

let currentPace = "optimistic";
let currentStartDate = "";
let isDemoMode = false;
let lastRemainingTopics = 289;

__JOURNEY_JS_A__

function loadData(){
  try{
    const raw = localStorage.getItem(KEY);
    if(raw) PR = JSON.parse(raw);
  }catch(e){}
}

async function initSync(){
  loadData();
  loadPaceSettings();
  calcAndPaint();

  try{
    let res = await fetch(API_BASE + "/api/status", { cache: "no-store" }).catch(()=>null);
    if(!res && !window.location.origin.startsWith("http")){
      res = await fetch("http://localhost:8080/api/status", { cache: "no-store" }).catch(()=>null);
      if(res) API_BASE = "http://localhost:8080";
    }

    if(res && res.ok){
      const data = await res.json();
      const dbBadge = document.getElementById("nav-db-status");
      if(dbBadge){
        if(data.db_type === "postgres"){
          dbBadge.className = "nav-status-pill badge-pg";
          dbBadge.textContent = "🐘 PostgreSQL";
        } else {
          dbBadge.className = "nav-status-pill badge-sq";
          dbBadge.textContent = "💾 SQLite";
        }
      }

      const progRes = await fetch(API_BASE + "/api/progress?user_id=1");
      if(progRes.ok){
        const dbData = await progRes.json();
        for(const k in dbData){
          PR[k] = Object.assign({s:"z", n:"", d:""}, dbData[k]);
        }
        try{ localStorage.setItem(KEY, JSON.stringify(PR)); }catch(e){}
        calcAndPaint();
      }
    }
  }catch(e){}
}

__JOURNEY_JS_B__

function toggleTheme(){
  const html = document.documentElement;
  const isDark = html.getAttribute("data-theme") === "dark" || (!html.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
  const next = isDark ? "light" : "dark";
  html.setAttribute("data-theme", next);
  try{ localStorage.setItem("roteiro-theme", next); }catch(e){}
}

try{
  const savedTheme = localStorage.getItem("roteiro-theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);
}catch(e){}

window.addEventListener("DOMContentLoaded", () => {
  initSync();
  checkHubAuth();
});
</script>
</body>
</html>
"""

    html = (html_template
        .replace("__HUB_CSS__", hub_css + JOURNEY_CSS)
        .replace("__JOURNEY_HTML__", JOURNEY_HTML)
        .replace("__JOURNEY_JS_A__", JOURNEY_JS_A)
        .replace("__JOURNEY_JS_B__", JOURNEY_JS_B)
        .replace("__AWS_SYNC_MODAL__", AWS_SYNC_MODAL_HTML)
        .replace("__CHANGE_CREDENTIALS_MODAL__", CHANGE_CREDENTIALS_MODAL_HTML)
        .replace("__FORGOT_PASSWORD_MODAL__", FORGOT_PASSWORD_MODAL_HTML)
        .replace("__AUTH_AWS_SYNC_JS__", AUTH_AWS_SYNC_JS)
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Gerado: {out_path} (Hub Central)")

# ---------------------------------------------------------------------------
# Executar a Geração de Todos os Arquivos do Ecossistema
# ---------------------------------------------------------------------------
out_ia = "/mnt/c/Users/joao1/Desktop/Roteiro/ia.html"
out_mat = "/mnt/c/Users/joao1/Desktop/Roteiro/matematica.html"
out_ing = "/mnt/c/Users/joao1/Desktop/Roteiro/ingles.html"
out_proj = "/mnt/c/Users/joao1/Desktop/Roteiro/projetos.html"
out_hub = "/mnt/c/Users/joao1/Desktop/Roteiro/index.html"
out_mirror = "/mnt/c/Users/joao1/Desktop/Roteiro/Roteiro de Estudo_ do zero à IA.html"

generate_listing_page(
    track_id="ia",
    page_title="Inteligência Artificial & Programação Python",
    page_sub="Do zero aos fundamentos de Python, Engenharia de Dados, Scikit-learn, PyTorch, Transformers, LLMs, Agentes e MLOps",
    track_icon="🤖",
    phases=ia_phases,
    out_path=out_ia,
    is_english=False
)

generate_listing_page(
    track_id="mat",
    page_title="Matemática Essencial para IA",
    page_sub="Álgebra Linear, Tensores, Cálculo Diferencial, Gradientes, Backpropagation, Probabilidade Bayesiana e Matemática dos Transformers",
    track_icon="📐",
    phases=mat_phases,
    out_path=out_mat,
    is_english=False
)

generate_listing_page(
    track_id="ing",
    page_title="Curso de Inglês EnglishBay (Playlist Oficial)",
    page_sub="Sequência completa de 73 vídeo-aulas da playlist oficial com links diretos para o YouTube, anotações de vocabulário e exercícios",
    track_icon="🇺🇸",
    phases=ing_phases,
    out_path=out_ing,
    is_english=True
)

generate_projects_page(out_proj, SHARED_CSS)

generate_hub_page(out_hub)
generate_hub_page(out_mirror)

print("\n🚀 Todos os arquivos do ecossistema gerados com sucesso!")
