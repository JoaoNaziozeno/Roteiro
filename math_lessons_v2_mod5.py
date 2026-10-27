# -*- coding: utf-8 -*-
"""
Aulas Visuais de Matemática v2 — Módulo 5: Transformers, Geometria Vetorial & Atenção.
Baseado em Vaswani et al. (Attention Is All You Need, 2017),
Su et al. (RoFormer: Rotary Position Embedding, 2021),
Zhang & Sennrich (RMSNorm, 2019) e Llama 3 Technical Report (Meta, 2024).
"""

# SVG: Scaled Dot-Product Attention Pipeline
SVG_ATTENTION = r'''<svg viewBox="0 0 540 240" class="lv2-svg" role="img" aria-label="Pipeline da Scaled Dot-Product Attention">
  <defs>
    <marker id="m5-arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#CCD0CF"/>
    </marker>
  </defs>
  <!-- Bloco Q e K -->
  <rect x="30" y="30" width="70" height="35" rx="6" fill="#11212D" stroke="#4A5C6A" stroke-width="1.5"/>
  <text x="65" y="52" class="sv-t" text-anchor="middle" style="font-weight:700">Query Q</text>

  <rect x="30" y="90" width="70" height="35" rx="6" fill="#11212D" stroke="#4A5C6A" stroke-width="1.5"/>
  <text x="65" y="112" class="sv-t" text-anchor="middle" style="font-weight:700">Key K</text>

  <!-- Multiplicação Mat-Mul Q @ K^T -->
  <line x1="100" y1="47" x2="150" y2="70" class="sv-a" marker-end="url(#m5-arr)"/>
  <line x1="100" y1="107" x2="150" y2="85" class="sv-a" marker-end="url(#m5-arr)"/>
  <rect x="155" y="60" width="80" height="36" rx="6" fill="#253745" stroke="#9BA8AB" stroke-width="1.5"/>
  <text x="195" y="82" class="sv-t" text-anchor="middle" style="font-weight:700">Q @ Kᵀ</text>

  <!-- Divisão por sqrt(d_k) -->
  <line x1="235" y1="78" x2="275" y2="78" class="sv-a" marker-end="url(#m5-arr)"/>
  <rect x="280" y="60" width="75" height="36" rx="6" fill="#11212D" stroke="#4A5C6A" stroke-width="1.5"/>
  <text x="317" y="82" class="sv-tm" text-anchor="middle" style="font-size:11px;font-weight:700">/ √d_k</text>

  <!-- Softmax -->
  <line x1="355" y1="78" x2="395" y2="78" class="sv-a" marker-end="url(#m5-arr)"/>
  <rect x="400" y="60" width="85" height="36" rx="6" fill="#253745" stroke="#CCD0CF" stroke-width="1.8"/>
  <text x="442" y="82" class="sv-t" text-anchor="middle" style="font-weight:700">Softmax</text>

  <!-- Value V e Mat-Mul Final -->
  <rect x="30" y="170" width="70" height="35" rx="6" fill="#11212D" stroke="#4A5C6A" stroke-width="1.5"/>
  <text x="65" y="192" class="sv-t" text-anchor="middle" style="font-weight:700">Value V</text>

  <line x1="442" y1="96" x2="442" y2="170" class="sv-a" marker-end="url(#m5-arr)"/>
  <line x1="100" y1="187" x2="395" y2="187" class="sv-a" marker-end="url(#m5-arr)"/>
  <rect x="400" y="170" width="105" height="38" rx="6" fill="#06141B" stroke="#CCD0CF" stroke-width="2"/>
  <text x="452" y="194" class="sv-t" text-anchor="middle" style="font-weight:800;font-size:12px">Saída (@ V)</text>
</svg>'''

# SVG: Rotação de RoPE no Plano Complexo
SVG_ROPE = r'''<svg viewBox="0 0 500 220" class="lv2-svg" role="img" aria-label="Rotação de RoPE no plano 2D">
  <!-- Círculo unitário -->
  <circle cx="220" cy="110" r="80" fill="none" stroke="#253745" stroke-width="1.5" stroke-dasharray="3 3"/>
  <!-- Eixos -->
  <line x1="110" y1="110" x2="330" y2="110" class="sv-ax"/>
  <line x1="220" y1="20" x2="220" y2="200" class="sv-ax"/>

  <!-- Vetor original x no tempo 0 -->
  <line x1="220" y1="110" x2="295" y2="80" class="sv-b" style="stroke-width:2.4"/>
  <circle cx="295" cy="80" r="4" class="sv-fillm"/>
  <text x="302" y="80" class="sv-tm" style="font-weight:700">x (Posição 0)</text>

  <!-- Vetor rotacionado por m * θ na posição m=3 -->
  <line x1="220" y1="110" x2="180" y2="40" class="sv-a" style="stroke-width:2.8"/>
  <circle cx="180" cy="40" r="5" class="sv-fill"/>
  <text x="145" y="35" class="sv-t" style="font-weight:700">R₃ x (Posição 3)</text>

  <!-- Arco de Rotação m*theta -->
  <path d="M 270 90 A 55 55 0 0 0 200 65" fill="none" stroke="#CCD0CF" stroke-width="1.8" stroke-dasharray="2 2"/>
  <text x="245" y="60" class="sv-t" style="font-size:11px;font-weight:700">Δθ = 3θ</text>

  <!-- Caixa explicativa à direita -->
  <rect x="350" y="50" width="135" height="110" rx="8" fill="#11212D" stroke="#253745"/>
  <text x="360" y="75" class="sv-t" style="font-size:11px;font-weight:700">Propriedade RoPE:</text>
  <text x="360" y="98" class="sv-tm" style="font-size:10px">⟨R_m q, R_n k⟩ =</text>
  <text x="360" y="118" class="sv-t" style="font-size:11px;font-weight:700">qᵀ R_{n-m} k</text>
  <text x="360" y="142" class="sv-tm" style="font-size:9.5px">Depende apenas da</text>
  <text x="360" y="154" class="sv-tm" style="font-size:9.5px">distância relativa (n - m)!</text>
</svg>'''

GUIDES_MOD5_V2 = {
    # =========================================================================
    # TÓPICO 38: Espaços vetoriais de alta dimensão e armazenamento de fatos em LLMs
    # =========================================================================
    "Espaços vetoriais de alta dimensão e armazenamento de fatos em LLMs": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Onde fica guardado que a <i>“capital da França é Paris”</i> dentro de um modelo como o GPT-4? Não existe uma tabela de banco de dados SQL e nem um dicionário Python em seus arquivos. Esse fato está gravado na geometria hiperdimensional de um <b>espaço vetorial de 4.096 dimensões</b>. Como a quase-ortogonalidade matemática permite que um modelo guarde bilhões de fatos sem que um sobrescreva o outro?""",
        "prerequisitos": [
            "Vetores, bases e produto escalar (Tópicos 1, 2 e 3)",
            "Matrizes como transformações lineares (Tópico 6)"
        ],
        "objetivos": [
            "compreender o fenômeno da Quase-Ortogonalidade em espaços de alta dimensão ($\mathbb{R}^{4096}$);",
            "entender o Lema de Johnson-Lindenstrauss sobre preservação de distâncias relativas;",
            "descobrir como as camadas Feed-Forward (MLP) dos Transformers operam como memórias associativas de chave-valor."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Mágica da Alta Dimensão",
                "titulo": "A Geometria Quase-Ortogonal",
                "corpo": r"""<p>No espaço bidimensional (2D), só conseguimos desenhar <b>2 vetores</b> mutuamente perpendiculares ($\theta = 90^\circ, \cos = 0$). No espaço tridimensional (3D), no máximo <b>3 vetores</b>.</p>
<p>Mas o que acontece quando pulamos para $d = 4.096$ dimensões (a dimensão de ativação de LLMs como o LLaMA)?</p>
<p>O volume da hiperesfera se concentra quase inteiramente em sua casca equatorial! Se você sortear vetores aleatórios em $\mathbb{R}^{4096}$, o produto escalar entre quaisquer dois vetores quase sempre será minúsculo ($|\cos \theta| < 0.03$). Eles são <b>quase-ortogonais</b>!</p>
<p>Isso significa que cabem <i>milhões de direções semânticas independentes</i> convivendo no mesmo espaço vetorial sem interferência destrutiva mútua.</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "Memória Associativa",
                "titulo": "Como as Camadas MLP Guardam Conhecimento Factóico",
                "corpo": r"""<p>Pesquisas recentes de interpretabilidade mecânica (Geva et al., 2021; Meng et al., ROME 2022) provaram que as camadas Feed-Forward dos Transformers funcionam como <b>tabelas hash de memória chave-valor contínuas</b>:</p>
$$\mathbf{y} = \text{GeLU}(\mathbf{x} W_{\text{in}} + \mathbf{b}_1) W_{\text{out}} + \mathbf{b}_2$$
<ul>
<li>A primeira matriz $W_{\text{in}}$ armazena vetores-chave (Keys): ela reconhece padrões conceituais como <i>“sujeito: Torre Eiffel, atributo: país”</i> via produto escalar alto.</li>
<li>A segunda matriz $W_{\text{out}}$ armazena vetores-valor (Values): quando o neurônio da chave dispara, ela injeta no fluxo residual a direção semântica do vetor de <i>“França”</i>!</li>
</ul>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: O Colapso dos Cossenos em Alta Dimensão",
                "codigo": r'''import numpy as np

# Comparando a ortogonalidade aleatória em 3D vs 4096D
np.random.seed(42)
N_pares = 2000

def calcular_cossenos_aleatorios(dim, n_pares):
    cossenos = []
    for _ in range(n_pares):
        u = np.random.randn(dim)
        v = np.random.randn(dim)
        cos = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        cossenos.append(cos)
    return np.array(cossenos)

cos_3d = calcular_cossenos_aleatorios(dim=3, n_pares=N_pares)
cos_4096d = calcular_cossenos_aleatorios(dim=4096, n_pares=N_pares)

print("Distribuição de Similaridade de Cosseno entre vetores aleatórios:")
print(f"Em 3D    -> Média: {np.mean(np.abs(cos_3d)):.3f} | Desvio: {np.std(cos_3d):.3f} (Muito espalhado: de -1 a +1!)")
print(f"Em 4096D -> Média: {np.mean(np.abs(cos_4096d)):.4f} | Desvio: {np.std(cos_4096d):.4f} (QUASE RIGOROSAMENTE ZERO!)")
print(f"99% dos vetores em 4096D têm |cos| < {np.percentile(np.abs(cos_4096d), 99):.4f}")
assert np.mean(np.abs(cos_4096d)) < 0.02, "Em 4096D os vetores devem ser quase perfeitamente ortogonais!"''',
                "experimentos": [
                    "Aumente a dimensão para <code>dim = 12288</code> (dimensão do GPT-4) e observe o cosseno colapsar ainda mais próximo de 0.000.",
                    "Perceba por que os modelos conseguem empilhar conhecimento de física quântica, gramática portuguesa e código Python no mesmo espaço vetorial sem misturá-los."
                ]
            }
        ],
        "resumo": [
            "Em alta dimensão ($d \ge 4096$), quase todos os vetores aleatórios são mutuamente quase-ortogonais.",
            "Essa quase-ortogonalidade permite armazenar milhões de associações semânticas sem interferência cruzada.",
            "Camadas MLP de Transformers funcionam como bancos de dados chave-valor projetando fatos via produto escalar."
        ],
        "proxima": r"Para manter esses vetores sob controle e estáveis ao longo de dezenas de camadas, como normalizar o espaço semântico? Vamos explorar a Normalização de Embeddings e a RMSNorm.",
        "referencias": [
            {"obra": "Meng et al. (2022). Locating and Editing Factual Associations in GPT (ROME)", "trecho": "Paper NeurIPS", "uso": "Prova de que associações conceituais são gravadas como vetores nos pesos das MLPs"},
            {"obra": "Geva et al. (2021). Transformer Feed-Forward Layers Are Key-Value Memories", "trecho": "Paper EMNLP", "uso": "Análise da correspondência entre neurônios de MLP e memórias associativas"}
        ]
    },

    # =========================================================================
    # TÓPICO 39: Normalização de embeddings e geometria do espaço semântico
    # =========================================================================
    "Normalização de embeddings e geometria do espaço semântico": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""O que acontece quando você pega um vetor de texto e divide pelo seu comprimento ($\mathbf{x} / \|\mathbf{x}\|$)? Ele aterrissa na superfície de uma <b>hiperesfera unitária de raio 1</b>. Nessa esfera, a magnitude numérica do vetor é apagada e resta puramente o seu <b>conteúdo angular semântico</b>. Por que o LLaMA 3, Mistral e Gemma aposentaram a LayerNorm clássica e adotaram a <b>RMSNorm</b>?""",
        "prerequisitos": [
            "Norma L2 Euclidiana (Tópico 4)",
            "Similaridade de Cosseno (Tópico 5)",
            "LayerNorm (Tópico 22)"
        ],
        "objetivos": [
            "compreender as propriedades geométricas de embeddings projetados na esfera unitária $\mathbb{S}^{d-1}$;",
            "provar a equivalência analítica entre Distância Euclidiana ao quadrado e Cosseno: $\|\mathbf{u} - \mathbf{v}\|^2 = 2 - 2\cos(\theta)$;",
            "dominar a fórmula e a vantagem computacional da RMSNorm (Root Mean Square Normalization)."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Esfera Semântica",
                "titulo": "Por que normalizar vetores para norma 1?",
                "corpo": r"""<p>Quando um modelo de embedding (como text-embedding-3 da OpenAI) gera um vetor para uma frase curta (<i>“bom dia”</i>) e para um artigo de 5 páginas, o texto longo conteria naturalmente números com magnitudes muito maiores se não houvesse normalização.</p>
<p>Ao projetar todo vetor na <b>hiperesfera unitária</b> ($\hat{\mathbf{x}} = \frac{\mathbf{x}}{\|\mathbf{x}\|_2}$), garantimos que:</p>
<ol>
<li>O comprimento de qualquer vetor é exatamente 1: $\|\hat{\mathbf{x}}\| = 1.0$.</li>
<li>O produto escalar entre dois vetores normalizados vira <b>exatamente a Similaridade de Cosseno</b>: $\hat{\mathbf{u}} \cdot \hat{\mathbf{v}} = \cos(\theta)$!</li>
<li>A distância Euclidiana ao quadrado fica rigidamente amarrada ao cosseno:
$$\|\hat{\mathbf{u}} - \hat{\mathbf{v}}\|^2 = \|\hat{\mathbf{u}}\|^2 + \|\hat{\mathbf{v}}\|^2 - 2(\hat{\mathbf{u}} \cdot \hat{\mathbf{v}}) = 1 + 1 - 2\cos(\theta) = 2 - 2\cos(\theta)$$</li>
</ol>
<p>Portanto, minimizar a distância no banco vetorial é matematicamente idêntico a maximizar a similaridade de cosseno!</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "A Evolução da Engenharia",
                "titulo": "Da LayerNorm para a RMSNorm nos Modelos Modernos",
                "corpo": r"""<p>A LayerNorm clássica subtraía a média $\mu$ e dividia pelo desvio padrão $\sigma$. Em 2019, Zhang & Sennrich investigaram: <i>“Será que subtrair a média é realmente necessário, ou a mágica da estabilização vem puramente de calibrar a escala de magnitude?”</i></p>
<p>Eles descobriram que subtrair a média não fazia falta nenhuma! Nasceu a <b>RMSNorm (Root Mean Square Normalization)</b>:</p>
$$\text{RMS}(\mathbf{x}) = \sqrt{\frac{1}{d} \sum_{i=1}^d x_i^2 + \epsilon}, \quad \bar{x}_i = \frac{x_i}{\text{RMS}(\mathbf{x})} \cdot \gamma_i$$
<p>Por não precisar calcular a média nem fazer duas passagens pelos dados na memória da GPU, a RMSNorm é <b>7% a 15% mais rápida</b> e economiza largura de banda preciosa em chips como a Nvidia H100. É por isso que é o padrão absoluto no LLaMA 3!</p>""",
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: RMSNorm vs LayerNorm",
                "codigo": r'''import numpy as np

# Vetor de ativações de um token de texto em dimensão d=8
x = np.array([3.2, -1.5, 0.4, 8.1, -4.0, 2.2, -0.8, 1.1])
d = len(x)

# 1. Implementação da LayerNorm Tradicional
media_ln = np.mean(x)
desvio_ln = np.std(x)
x_layernorm = (x - media_ln) / (desvio_ln + 1e-5)

# 2. Implementação da RMSNorm Moderna (LLaMA 3)
rms = np.sqrt(np.mean(x**2) + 1e-5)
x_rmsnorm = x / rms

print(f"Vetor original          : {x.round(2)}")
print(f"Norma original          : {np.linalg.norm(x):.3f}\n")
print(f"LayerNorm (média 0, std 1): {x_layernorm.round(3)}")
print(f"  -> Média pós-LayerNorm  : {np.mean(x_layernorm):.6f}")
print(f"RMSNorm (escala mantida) : {x_rmsnorm.round(3)}")
print(f"  -> RMS pós-RMSNorm      : {np.sqrt(np.mean(x_rmsnorm**2)):.6f} (rigorosamente 1.0!)")''',
                "experimentos": [
                    "Verifique a identidade geométrica: normalize dois vetores aleatórios com <code>u / norm(u)</code> e confira se <code>norm(u - v)**2</code> bate com <code>2 - 2 * dot(u, v)</code>.",
                    "Note que na RMSNorm os sinais e o centro natural das ativações não são deslocados artificialmente para zero, preservando a assimetria natural de ativações como ReLU e GeLU."
                ]
            }
        ],
        "resumo": [
            "Projetar embeddings na hiperesfera unitária converte produtos escalares em medidas puras de similaridade angular de cosseno.",
            "A distância euclidiana ao quadrado na esfera unitária é diretamente expressa por $2 - 2\cos(\theta)$.",
            "A RMSNorm calibra a escala pelo Root Mean Square sem subtrair a média, acelerando o treinamento de LLMs modernos."
        ],
        "proxima": r"Com os embeddings normalizados, como uma palavra se transforma em Query, Key e Value? Vamos dissecar as projeções lineares de pesos no Tópico 40.",
        "referencias": [
            {"obra": "Zhang & Sennrich (2019). Root Mean Square Layer Normalization", "trecho": "Paper NeurIPS", "uso": "Dedução teórica e validação empírica da RMSNorm"},
            {"obra": "Meta AI (2024). The Llama 3 Herd of Models", "trecho": "Technical Report", "uso": "Detalhes de arquitetura utilizando RMSNorm e embeddings normalizados"}
        ]
    },

    # =========================================================================
    # TÓPICO 40: Projeções lineares e matrizes de pesos Query, Key e Value
    # =========================================================================
    "Projeções lineares e matrizes de pesos Query, Key e Value (W_q, W_k, W_v)": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Em uma frase como <i>“O cozinheiro serviu o café quente porque <b>ele</b>...”</i>, quem é a palavra <i>“ele”</i>? Para responder, a palavra <i>“ele”</i> precisa desempenhar três papéis simultâneos: fazer uma pergunta (<b>Query</b>), responder às perguntas dos outros (<b>Key</b>) e fornecer conteúdo semântico (<b>Value</b>). Como três simples matrizes de pesos lineares ($W_Q, W_K, W_V$) dividem uma mesma palavra nessas três personas matemáticas?""",
        "prerequisitos": [
            "Multiplicação de matrizes e transposta (Tópicos 6 e 7)",
            "Embeddings de palavras (Tópico 1)"
        ],
        "objetivos": [
            "compreender a metáfora da biblioteca e dos papéis de busca: Query, Key e Value;",
            "entender as dimensões dos tensores e a projeção linear via multiplicação de matrizes;",
            "descobrir por que precisamos de projeções aprendidas em vez de usar os embeddings brutos."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Metáfora da Biblioteca de Busca",
                "titulo": "As Três Facetas de um Token",
                "corpo": r"""<p>Vaswani et al. (2017) se inspiraram nos sistemas clássicos de recuperação de informação de bancos de dados para criar a atenção dos Transformers:</p>
<ul>
<li><b>Query ($\mathbf{q}$ - Consulta):</b> É o que o token atual está <i>procurando</i>. No caso de <i>“ele”</i>, a Query pergunta: <i>“Cadê o substantivo masculino singular que veio antes de mim?”</i></li>
<li><b>Key ($\mathbf{k}$ - Chave / Rótulo):</b> É o catálogo descritivo do que o token <i>tem a oferecer</i>. A palavra <i>“cozinheiro”</i> oferece: <i>“Sou um substantivo masculino singular”</i>. A palavra <i>“quente”</i> oferece: <i>“Sou um adjetivo de temperatura”</i>.</li>
<li><b>Value ($\mathbf{v}$ - Conteúdo de Valor):</b> É o significado informacional real que será transmitido se a consulta bater com a chave. Se <i>“ele”</i> focar em <i>“cozinheiro”</i>, o Value extrai as características semânticas de cozinheiro para atualizar o contexto de <i>“ele”</i>.</li>
</ul>""",
            },
            {
                "tipo": "notacao",
                "titulo": "As Projeções Lineares Matriciais",
                "corpo": r"""<p>Seja $X \in \mathbb{R}^{T \times d}$ a matriz contendo os embeddings dos $T$ tokens da frase em dimensão $d$. O modelo aprende três matrizes de pesos:</p>
$$W_Q \in \mathbb{R}^{d \times d_k}, \quad W_K \in \mathbb{R}^{d \times d_k}, \quad W_V \in \mathbb{R}^{d \times d_v}$$
<p>As matrizes de Query, Key e Value são geradas por simples multiplicação matricial:</p>
$$Q = X W_Q, \quad K = X W_K, \quad V = X W_V$$""",
                "itens": [
                    {"simbolo": r"$Q \in \mathbb{R}^{T \times d_k}$", "leitura": "matriz de Queries", "significado": "Cada linha $i$ é a pergunta formulada pelo token $i$."},
                    {"simbolo": r"$K \in \mathbb{R}^{T \times d_k}$", "leitura": "matriz de Keys", "significado": "Cada linha $j$ é a chave de endereçamento do token $j$. Tem rigorosamente a mesma dimensão $d_k$ de $Q$ para permitir o produto escalar!"},
                    {"simbolo": r"$V \in \mathbb{R}^{T \times d_v}$", "leitura": "matriz de Values", "significado": "Cada linha $j$ é a informação substancial a ser repassada. Frequentemente $d_v = d_k$."},
                ],
            },
            {
                "tipo": "passos",
                "titulo": "Por que não usar o embedding original X diretamente?",
                "corpo": r"""<p>Por que Vaswani et al. não calcularam simplesmente $X X^\top$ em vez de projetar em $W_Q$ e $W_K$?</p>""",
                "passos": [
                    {
                        "faca": r"Analise a simetria de $X X^\top$: O produto escalar bruto é comutativo: $\mathbf{x}_i^\top \mathbf{x}_j = \mathbf{x}_j^\top \mathbf{x}_i$.",
                        "porque": "Sem matrizes de projeção, se a palavra A prestar atenção em B, a palavra B seria obrigada a prestar exatamente a mesma atenção em A!"
                    },
                    {
                        "faca": r"Observe a assimetria linguística real: Em <i>'bloqueou o cartão'</i>, o verbo <i>'bloqueou'</i> precisa olhar para o objeto <i>'cartão'</i>, mas <i>'cartão'</i> não precisa olhar para o verbo com o mesmo objetivo.",
                        "porque": "Relações gramaticais e semânticas são <b>direcionadas e assimétricas</b>."
                    },
                    {
                        "faca": r"Projeções separadas criam assimetria: Como $Q = X W_Q$ e $K = X W_K$, a pontuação de atenção é $\mathbf{q}_i^\top \mathbf{k}_j = \mathbf{x}_i^\top (W_Q W_K^\top) \mathbf{x}_j$.",
                        "porque": "Como $W_Q W_K^\top$ não é uma matriz simétrica, $\mathbf{q}_i^\top \mathbf{k}_j \neq \mathbf{q}_j^\top \mathbf{k}_i$! A assimetria permite atenção direcional perfeita."
                    }
                ],
                "conclusao": r"As matrizes $W_Q, W_K, W_V$ conferem total liberdade para o Transformer aprender gramática, sintaxe e relações causais de forma independente em cada camada."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Calculando Q, K e V a partir de Embeddings",
                "codigo": r'''import numpy as np

# 3 tokens da nossa cafeteria: ["café", "está", "quente"]
# Dimensão do embedding d = 4, dimensão de atenção d_k = 3
tokens = ["café", "está", "quente"]
T, d, d_k = 3, 4, 3

np.random.seed(42)
# Matriz de embeddings dos tokens X (3 x 4)
X = np.random.randn(T, d)

# Matrizes de projeção de pesos aprendidas pelo modelo
W_Q = np.random.randn(d, d_k)
W_K = np.random.randn(d, d_k)
W_V = np.random.randn(d, d_k)

# Projeções lineares matriciais
Q = X @ W_Q # (3 x 3)
K = X @ W_K # (3 x 3)
V = X @ W_V # (3 x 3)

print("Matrizes Projetadas:")
print("Shape de Q (Queries):", Q.shape)
print("Shape de K (Keys)   :", K.shape)
print("Shape de V (Values) :", V.shape)

# Mostrando a Query do primeiro token ('café')
print(f"\nQuery do token '{tokens[0]}' : {Q[0].round(3)}")
print(f"Key do token '{tokens[2]}' ('quente'): {K[2].round(3)}")
afinidade_cafe_quente = np.dot(Q[0], K[2])
print(f"Afinidade não normalizada (Q_café · K_quente): {afinidade_cafe_quente:.3f}")''',
                "experimentos": [
                    "Compare a afinidade $\mathbf{q}_0^\top \mathbf{k}_2$ com $\mathbf{q}_2^\top \mathbf{k}_0$ e comprove que a matriz de afinidade resultante é assimétrica.",
                    "Entenda como durante o treinamento (backpropagation) os gradientes ajustam diretamente as matrizes $W_Q, W_K, W_V$ para maximizar a assertividade dos tokens."
                ]
            }
        ],
        "resumo": [
            "Query é o que o token busca, Key é como ele se apresenta e Value é o conteúdo que ele entrega.",
            "As matrizes de projeção $W_Q, W_K, W_V$ transformam embeddings genéricos em representações especializadas de busca.",
            "A projeção linear quebra a simetria do produto escalar, permitindo atenção linguística direcional e assimétrica."
        ],
        "proxima": r"Com as matrizes Q, K e V prontas, como uni-las na fórmula mais famosa da IA contemporânea? No próximo tópico, dissecaremos a Scaled Dot-Product Attention.",
        "referencias": [
            {"obra": "Vaswani et al. (2017). Attention Is All You Need", "trecho": "Seção 3.2.1: Scaled Dot-Product Attention", "uso": "Definição formal das matrizes de projeção Q, K, V"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 2.6: Linear Mappings", "uso": "Fundamentação algébrica de transformações lineares entre espaços de dimensões distintas"}
        ]
    },

    # =========================================================================
    # TÓPICO 41: Fórmula de Scaled Dot-Product Attention
    # =========================================================================
    "Fórmula de Scaled Dot-Product Attention: softmax((Q @ K^T) / sqrt(d_k)) * V": {
        "v": 2,
        "duracao": 35,
        "gancho": r"""Esta é a fórmula mais poderosa da história da inteligência artificial moderna:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$$
Por que dividimos rigorosamente pela raiz da dimensão ($\sqrt{d_k}$)? O que acontece se removermos essa divisão? E como calcular essa matriz à mão, passo a passo, para dois tokens de texto?""",
        "prerequisitos": [
            "Matrizes Q, K, V (Tópico 40)",
            "Função Softmax e multiplicação de matrizes (Tópicos 7 e 35)",
            "Média e variância da soma de variáveis (Tópico 22)"
        ],
        "objetivos": [
            "dominar a anatomia completa da fórmula de Scaled Dot-Product Attention;",
            "provar matematicamente por que a variância do produto escalar cresce linearmente com $d_k$, justificando a divisão por $\sqrt{d_k}$;",
            "calcular manualmente a matriz de atenção de 2 tokens com passos aritméticos verificados."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Equação Soberana",
                "titulo": "A Anatomia dos Quatro Passos da Atenção",
                "corpo": r"""<p>A atenção pondera o quanto cada palavra deve absorver de informação de todas as outras palavras do texto. O cálculo ocorre em quatro etapas matriciais:</p>
<ol>
<li><b>Afinidade Bruta ($Q K^\top$):</b> Multiplica cada Query por todas as Keys via produto escalar, gerando uma matriz de pontuações $T \times T$.</li>
<li><b>Escalonamento ($/ \sqrt{d_k}$):</b> Divide as pontuações para controlar a variância e impedir que a Softmax sature.</li>
<li><b>Pesos de Probabilidade ($\text{Softmax}$):</b> Aplica a Softmax em cada linha independentemente, transformando pontuações brutas em pesos percentuais positivos que somam 100%.</li>
<li><b>Agregação Ponderada ($\times V$):</b> Multiplica os pesos de atenção pela matriz de Values, produzindo a nova representação enriquecida pelo contexto!</li>
</ol>""",
            },
            {
                "tipo": "visual",
                "titulo": "O Fluxo de Dados da Atenção",
                "corpo": r"""<p>Acompanhe o caminho percorrido pelos tensores dentro do mecanismo:</p>""",
                "svg": SVG_ATTENTION,
                "legenda": "Q multiplica K transposto, o resultado é escalado por √d_k, normalizado por Softmax e multiplica V para gerar a saída.",
            },
            {
                "tipo": "passos",
                "titulo": "A Prova Matemática: Por que dividir por √d_k?",
                "corpo": r"""<p>Esta é uma das perguntas mais frequentes em entrevistas técnicas de IA para pesquisadores:</p>""",
                "passos": [
                    {
                        "faca": r"Considere componentes independentes $q_i$ e $k_i$ com média zero e variância 1: $$\mathbb{E}[q_i] = 0, \quad \text{Var}(q_i) = 1, \quad \mathbb{E}[k_i] = 0, \quad \text{Var}(k_i) = 1$$",
                        "porque": "Essa é a distribuição padrão após camadas de normalização (LayerNorm / RMSNorm)."
                    },
                    {
                        "faca": r"Calcule a variância do produto individual $q_i k_i$: Como são independentes, $\text{Var}(q_i k_i) = \mathbb{E}[(q_i k_i)^2] - (\mathbb{E}[q_i k_i])^2 = \text{Var}(q_i)\text{Var}(k_i) = 1 \times 1 = 1$.",
                        "porque": "O produto de duas variáveis padrão independentes tem variância 1."
                    },
                    {
                        "faca": r"Calcule a variância da soma de $d_k$ termos: O produto escalar é $\mathbf{q}^\top \mathbf{k} = \sum_{i=1}^{d_k} q_i k_i$. A variância da soma é a soma das variâncias: $$\text{Var}\left( \sum_{i=1}^{d_k} q_i k_i \right) = \sum_{i=1}^{d_k} 1 = d_k$$",
                        "porque": "Se $d_k = 64$, a variância do produto escalar é $64$, e seu desvio padrão é $\sqrt{64} = 8$!"
                    },
                    {
                        "faca": r"Veja o perigo de números grandes na Softmax: Se as pontuações atingem valores como $+8$ ou $-8$, a Softmax satura com probabilidades extremas como $0.9999$ e $0.0001$.",
                        "porque": "Lembra do Módulo 2 (Tópico 15)? A derivada da Softmax satura e vai a zero ($\text{softmax}' \to 0$), <b>matando o gradiente</b> e paralisando o treino!"
                    },
                    {
                        "faca": r"Divida por $\sqrt{d_k}$: Pela propriedade de variância $\text{Var}(c X) = c^2 \text{Var}(X)$: $$\text{Var}\left( \frac{\mathbf{q}^\top \mathbf{k}}{\sqrt{d_k}} \right) = \left(\frac{1}{\sqrt{d_k}}\right)^2 \text{Var}(\mathbf{q}^\top \mathbf{k}) = \frac{1}{d_k} \times d_k = 1.0$$",
                        "porque": "A divisão por $\sqrt{d_k}$ traz a variância de volta para exatamente 1.0, mantendo a Softmax em sua zona ativa de gradientes saudáveis!"
                    }
                ],
                "conclusao": r"A divisão por $\sqrt{d_k}$ é uma solução estatística genial para o problema do gradiente evanescente na atenção."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Scaled Dot-Product Attention Completo",
                "codigo": r'''import numpy as np

# Função completa de Atenção
def scaled_dot_product_attention(Q, K, V):
    d_k = Q.shape[-1]
    
    # 1. Multiplicação Q @ K^T e escalonamento
    scores = (Q @ K.T) / np.sqrt(d_k)
    
    # 2. Softmax por linha
    exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    pesos_atencao = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
    
    # 3. Multiplicação pelos Values
    saida = pesos_atencao @ V
    return saida, pesos_atencao

# Simulação com 2 tokens: ["café", "quente"] com d_k = 4
Q_exemplo = np.array([
    [1.0, 0.0, 1.0, 0.0],  # Token 0: 'café'
    [0.0, 1.0, 0.0, 1.0]   # Token 1: 'quente'
])
K_exemplo = np.array([
    [1.0, 0.0, 1.0, 0.0],
    [0.0, 1.0, 1.0, 0.0]
])
V_exemplo = np.array([
    [10.0, 20.0], # Conteúdo do token 0
    [30.0, 40.0]  # Conteúdo do token 1
])

saida, pesos = scaled_dot_product_attention(Q_exemplo, K_exemplo, V_exemplo)

print("Matriz de Pesos de Atenção (Softmax):")
print(f"Token 'café'   -> [atenta em si: {pesos[0,0]*100:.1f}%, atenta em 'quente': {pesos[0,1]*100:.1f}%]")
print(f"Token 'quente' -> [atenta em 'café': {pesos[1,0]*100:.1f}%, atenta em si: {pesos[1,1]*100:.1f}%]")
print("\nSaída contextualizada final:")
print(saida.round(2))
assert np.isclose(np.sum(pesos[0]), 1.0), "Cada linha da matriz de atenção deve somar 100%!"''',
                "experimentos": [
                    "Remova o termo <code>/ np.sqrt(d_k)</code> e use <code>d_k = 128</code> com entradas normais. Observe como os pesos colapsam em 100% para um token e 0% para todos os outros, demonstrando a saturação da Softmax.",
                    "Aplique uma máscara causal triangular inferior para impedir que tokens presentes olhem para tokens futuros (como no treinamento do GPT)."
                ]
            }
        ],
        "resumo": [
            "A Scaled Dot-Product Attention calcula afinidade via produto escalar e sintetiza informações de valores contextuais.",
            "A divisão por $\sqrt{d_k}$ estabiliza a variância em 1.0, impedindo o desaparecimento de gradientes na Softmax.",
            "As saídas contextuais são médias ponderadas dos vetores de Value pelas afinidades probabilísticas."
        ],
        "proxima": r"Uma única cabeça de atenção só consegue focar em um padrão por vez. Para enriquecer o modelo, dividimos a atenção em múltiplas cabeças: Multi-Head Attention.",
        "referencias": [
            {"obra": "Vaswani et al. (2017). Attention Is All You Need", "trecho": "Seção 3.2.1: Scaled Dot-Product Attention", "uso": "Formulação original e justificativa empírica do escalonamento"},
            {"obra": "Deisenroth, Faisal & Ong. Mathematics for Machine Learning", "trecho": "Capítulo 6.4: Variance of Linear Combinations", "uso": "Prova matemática formal da variância do produto escalar de variáveis independentes"}
        ]
    },

    # =========================================================================
    # TÓPICO 42: Mecanismo Multi-Head Attention
    # =========================================================================
    "Mecanismo Multi-Head Attention: divisão de dimensões e concatenação": {
        "v": 2,
        "duracao": 30,
        "gancho": r"""Em uma frase como <i>“A atendente entregou o café ao cliente porque <b>ela</b> era gentil”</i>, a palavra <i>“ela”</i> precisa focar em <i>“atendente”</i> por razões gramaticais (gênero feminino), mas também precisa olhar para <i>“gentil”</i> por razões descritivas. Como uma única cabeça de atenção não consegue focar em dois lugares diferentes com a mesma intensidade, dividimos o modelo em <b>múltiplas cabeças de atenção independentes (Multi-Head Attention)</b> sem gastar um centavo a mais de computação!""",
        "prerequisitos": [
            "Scaled Dot-Product Attention (Tópico 41)",
            "Matrizes e concatenação de tensores (Tópicos 1 e 7)"
        ],
        "objetivos": [
            "compreender por que múltiplos focos de atenção simultâneos são indispensáveis para a linguagem natural;",
            "entender a matemática da divisão em $h$ cabeças com dimensão reduzida $d_k = d / h$;",
            "acompanhar a recombinação final via concatenação e matriz de projeção de saída $W_O$."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "Múltiplos Pontos de Vista",
                "titulo": "O Princípio do Multi-Head Attention",
                "corpo": r"""<p>Se tivéssemos apenas uma cabeça de atenção com dimensão total $d = 4096$, a média ponderada da Softmax forçaria todos os relacionamentos a se misturarem em uma única sopa semântica indistinta.</p>
<p>Vaswani et al. (2017) propuseram projetar as Queries, Keys e Values $h$ vezes com matrizes aprendidas diferentes, executar a atenção em cada uma em paralelo e concatenar os resultados:</p>
$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \text{head}_2, \dots, \text{head}_h) W_O$$
$$\text{onde } \text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$
<p>O segredo brilhante da arquitetura é que cada cabeça trabalha com dimensão reduzida:</p>
$$d_k = d / h$$
<p>Por exemplo, no GPT-3 com $d = 12.288$ e $h = 96$ cabeças, cada cabeça processa vetores de tamanho $d_k = 12.288 / 96 = 128$. O custo computacional total de processar 96 cabeças pequenas em paralelo na GPU é <b>rigorosamente idêntico</b> ao de processar uma única cabeça gigante!</p>""",
            },
            {
                "tipo": "tabela",
                "titulo": "O que cada cabeça costuma aprender na prática?",
                "cabecalho": ["Cabeça de Atenção", "Especialização Linguística Aprendida", "Exemplo Prático"],
                "linhas": [
                    ["Cabeça Sintática", "Conecta pronomes a substantivos antecedentes", "<i>'ela'</i> $\to$ <i>'atendente'</i>"],
                    ["Cabeça Causal / Adjetiva", "Conecta causas, emoções e qualificadores", "<i>'bloqueou'</i> $\to$ <i>'fraude'</i>"],
                    ["Cabeça Posicional Relativa", "Foca sistematicamente na palavra imediatamente anterior", "Token $t$ olha para $t-1$"],
                    ["Cabeça de Entidades", "Agrupa termos que formam um nome composto", "<i>'Torre'</i> $\to$ <i>'Eiffel'</i>"]
                ]
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: Multi-Head Attention com Reshape de Tensores",
                "codigo": r'''import numpy as np

# Configurações do Transformer
batch_size = 1
seq_len = 3      # 3 tokens
d_model = 8      # dimensão do modelo
num_heads = 2    # 2 cabeças de atenção
d_k = d_model // num_heads # 4 por cabeça

np.random.seed(42)
X = np.random.randn(batch_size, seq_len, d_model)

# Matrizes de projeção globais
W_Q = np.random.randn(d_model, d_model)
W_K = np.random.randn(d_model, d_model)
W_V = np.random.randn(d_model, d_model)
W_O = np.random.randn(d_model, d_model) # Projeção de saída final

# 1. Projeção linear global
Q = X @ W_Q # (1, 3, 8)
K = X @ W_K
V = X @ W_V

# 2. Reshape elegante para fatiar nas h cabeças: (batch, seq, heads, d_k) -> (batch, heads, seq, d_k)
Q_heads = Q.reshape(batch_size, seq_len, num_heads, d_k).swapaxes(1, 2)
K_heads = K.reshape(batch_size, seq_len, num_heads, d_k).swapaxes(1, 2)
V_heads = V.reshape(batch_size, seq_len, num_heads, d_k).swapaxes(1, 2)

print(f"Shape do tensor fatiado por cabeças: {Q_heads.shape}")
print(f"  -> {batch_size} batch, {num_heads} cabeças paralelas, {seq_len} tokens, dimensão {d_k} cada")

# 3. Scaled dot-product em paralelo para todas as cabeças
scores = (Q_heads @ K_heads.swapaxes(-1, -2)) / np.sqrt(d_k)
exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)
head_outputs = attn_weights @ V_heads # (1, 2, 3, 4)

# 4. Concatenação e projeção final W_O
concat = head_outputs.swapaxes(1, 2).reshape(batch_size, seq_len, d_model)
saida_mha = concat @ W_O

print(f"Shape após concatenação e projeção W_O: {saida_mha.shape} (retorna idêntico ao input!)")
assert saida_mha.shape == X.shape, "A saída do Multi-Head deve preservar a dimensão de entrada!"''',
                "experimentos": [
                    "Aumente para <code>num_heads = 4</code> (com <code>d_k = 2</code>) e veja como a mecânica de tensores do NumPy continua executando o paralelismo com perfeição.",
                    "Entenda como a matriz de saída $W_O$ mistura e consolida os aprendizados de todas as cabeças de volta na corrente residual principal."
                ]
            }
        ],
        "resumo": [
            "Multi-Head Attention divide o espaço de representação em múltiplos subespaços de atenção paralelos.",
            "Dividir $d$ em $h$ cabeças com $d_k = d/h$ mantém o custo computacional rigorosamente idêntico a uma única cabeça grande.",
            "A concatenação final projetada por $W_O$ unifica os múltiplos pontos de vista aprendidos de volta no fluxo residual."
        ],
        "proxima": r"O Transformer não tem noção de tempo ou ordem: ele enxerga um saco de palavras. Como ensinar ordem ao modelo usando rotação vetorial? Chegamos ao último tópico: Positional Encodings e RoPE.",
        "referencias": [
            {"obra": "Vaswani et al. (2017). Attention Is All You Need", "trecho": "Seção 3.2.2: Multi-Head Attention", "uso": "Arquitetura e fundamentação do mecanismo de múltiplas cabeças"},
            {"obra": "Clark et al. (2019). What Does BERT Look At? An Analysis of Attention", "trecho": "Paper ACL", "uso": "Comprovação empírica da especialização linguística de cabeças individuais"}
        ]
    },

    # =========================================================================
    # TÓPICO 43: Positional Encodings: funções sinusoidais e rotação vetorial (RoPE)
    # =========================================================================
    "Positional Encodings: funções sinusoidais e rotação vetorial (RoPE)": {
        "v": 2,
        "duracao": 35,
        "gancho": r"""Se você embaralhar todas as palavras de uma frase, o mecanismo de atenção original calculará rigorosamente as mesmas afinidades: ele é uma <b>bolsa de palavras atemporal</b> que não sabe quem veio antes de quem. Como ensinar a uma IA que <i>“o cão mordeu o homem”</i> é completamente diferente de <i>“o homem mordeu o cão”</i>? E por que a moderna <b>RoPE (Rotary Position Embedding)</b> usada no LLaMA 3 gira vetores no plano complexo em vez de somar ondas senoidais?""",
        "prerequisitos": [
            "Trigonometria (seno e cosseno)",
            "Matrizes de rotação 2D (Tópico 6)",
            "Produto escalar de vetores (Tópico 3)"
        ],
        "objetivos": [
            "compreender por que os Transformers precisam de codificação posicional explícita;",
            "analisar a abordagem sinusoidal original de Vaswani et al. ($X + PE$);",
            "dominar a inovação do RoPE (Rotary Position Embedding) e provar por que ela preserva a distância relativa $(m - n)$ no produto escalar."
        ],
        "blocos": [
            {
                "tipo": "texto",
                "rotulo": "A Amnésia Temporal do Transformer",
                "titulo": "Por que a Atenção é Cega à Ordem?",
                "corpo": r"""<p>Na fórmula da atenção $\text{softmax}\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$, o produto escalar mede apenas o alinhamento de direções entre vetores. Ele é <b>invariante à permutação</b>: se você trocar a ordem das palavras de entrada, a saída é simplesmente permutada na mesma ordem, sem que o modelo perceba que a semântica mudou!</p>
<p>Diferente das antigas RNNs (que liam palavra por palavra em sequência temporal), o Transformer lê todos os tokens de uma só vez em paralelo na GPU. Para saber quem veio primeiro, precisamos injetar a <b>posição $pos$</b> explicitamente na matemática.</p>""",
            },
            {
                "tipo": "texto",
                "rotulo": "A Abordagem Clássica vs. A Revolução Moderna",
                "titulo": "Das Senoides Aditivas ao RoPE Rotacional",
                "corpo": r"""<p>A evolução ocorreu em dois grandes saltos históricos:</p>
<ol>
<li><b>Sinusoidal Aditivo (Vaswani et al., 2017):</b> Cria ondas de seno e cosseno em frequências decrescentes e <b>soma diretamente</b> ao embedding: $\tilde{X} = X + PE$. Embora funcional, a soma polui o espaço semântico e tem dificuldade para extrapolar para textos mais longos do que os vistos no treino.</li>
<li><b>Rotary Position Embedding (RoPE - Su et al., 2021):</b> Em vez de somar, nós <b>rotacionamos</b> o vetor de Query e Key no plano bidimensional por um ângulo proporcional à sua posição $m$ no texto!</li>
</ol>""",
            },
            {
                "tipo": "visual",
                "titulo": "A Geometria Rotacional do RoPE",
                "corpo": r"""<p>Veja como o vetor gira no plano conforme o token avança na sequência:</p>""",
                "svg": SVG_ROPE,
                "legenda": "Cada par de coordenadas do vetor gira por um ângulo m·θ. O produto escalar resultante depende unicamente da distância relativa (n - m) entre as posições.",
            },
            {
                "tipo": "passos",
                "titulo": "A Mágica da Distância Relativa no RoPE",
                "corpo": r"""<p>Acompanhe a prova matemática de por que o produto escalar rotacionado preserva a distância relativa:</p>""",
                "passos": [
                    {
                        "faca": r"Escreva a matriz de rotação 2D na posição $m$: $$R_m = \begin{bmatrix} \cos(m\theta) & -\sin(m\theta) \\ \sin(m\theta) & \cos(m\theta) \end{bmatrix}$$",
                        "porque": "Matriz ortogonal clássica de rotação por um ângulo $m\theta$."
                    },
                    {
                        "faca": r"Rotacione a Query na posição $m$ e a Key na posição $n$: $$\tilde{\mathbf{q}}_m = R_m \mathbf{q}, \quad \tilde{\mathbf{k}}_n = R_n \mathbf{k}$$",
                        "porque": "Cada vetor recebe uma rotação proporcional à sua própria coordenada temporal absoluta."
                    },
                    {
                        "faca": r"Calcule o produto escalar entre a Query e a Key rotacionadas: $$\langle \tilde{\mathbf{q}}_m, \tilde{\mathbf{k}}_n \rangle = (R_m \mathbf{q})^\top (R_n \mathbf{k}) = \mathbf{q}^\top (R_m^\top R_n) \mathbf{k}$$",
                        "porque": "Propriedade da transposta do produto: $(A B)^\top = B^\top A^\top$."
                    },
                    {
                        "faca": r"Use a propriedade de grupo das rotações: A transposta de uma rotação é a rotação inversa ($R_m^\top = R_{-m}$). Girar $-m$ e depois $+n$ é girar exatamente $(n - m)$: $$R_m^\top R_n = R_{-m} R_n = R_{n - m}$$",
                        "porque": "Pelas identidades trigonométricas de subtração de arcos $\cos(a-b)$ e $\sin(a-b)$."
                    },
                    {
                        "faca": r"Conclua a identidade fundamental: $$\langle \tilde{\mathbf{q}}_m, \tilde{\mathbf{k}}_n \rangle = \mathbf{q}^\top R_{n - m} \mathbf{k}$$",
                        "porque": "O produto escalar final depende <b>exclusivamente do deslocamento relativo $(n - m)$</b> e não da posição absoluta onde as palavras estão na página!"
                    }
                ],
                "conclusao": r"Se a palavra 'café' estiver 2 posições à frente de 'quente', a atenção entre elas será rigorosamente a mesma se estiverem no início do texto (posições 1 e 3) ou 100 páginas depois (posições 50.001 e 50.003)! É por isso que o LLaMA 3 consegue ler contextos de 128.000 tokens."
            },
            {
                "tipo": "laboratorio",
                "titulo": "Laboratório NumPy: O Kernel RoPE 2D em Ação",
                "codigo": r'''import numpy as np

# Função de Rotação RoPE 2D
def aplicar_rope_2d(v, pos, theta=0.1):
    angulo = pos * theta
    R = np.array([
        [np.cos(angulo), -np.sin(angulo)],
        [np.sin(angulo),  np.cos(angulo)]
    ])
    return R @ v

# Vetor de Query e Vetor de Key base
q = np.array([1.0, 0.5])
k = np.array([0.8, 1.2])

# Cenário 1: Tokens nas posições m=2 e n=5 (distância relativa = 3)
q_pos2 = aplicar_rope_2d(q, pos=2)
k_pos5 = aplicar_rope_2d(k, pos=5)
prod_escalar_1 = np.dot(q_pos2, k_pos5)

# Cenário 2: Tokens 1000 posições à frente, mas com a MESMA distância relativa (m=1002 e n=1005)
q_pos1002 = aplicar_rope_2d(q, pos=1002)
k_pos1005 = aplicar_rope_2d(k, pos=1005)
prod_escalar_2 = np.dot(q_pos1002, k_pos1005)

print(f"Produto escalar nas posições (2, 5)       : {prod_escalar_1:.6f}")
print(f"Produto escalar nas posições (1002, 1005): {prod_escalar_2:.6f}")
print(f"Diferença numérica: {abs(prod_escalar_1 - prod_escalar_2):.2e}")

assert np.isclose(prod_escalar_1, prod_escalar_2), "O produto escalar do RoPE DEVE depender apenas da distância relativa!"
print("\nComprovação matemática de RoPE executada com sucesso absoluto!")''',
                "experimentos": [
                    "Aumente a distância relativa de 3 para 50 tokens e veja o produto escalar decair naturalmente, refletindo a intuição humana de que palavras muito distantes têm menor acoplamento gramatical imediato.",
                    "Entenda como técnicas modernas de ampliação de contexto (como RoPE Scaling e YaRN) simplesmente dividem o parâmetro $\\theta$ por um fator de escala para permitir que o modelo leia livros inteiros."
                ]
            }
        ],
        "resumo": [
            "Atenção padrão é cega à ordem e exige codificação posicional explícita para diferenciar a sequência das palavras.",
            "Positional Encodings sinusoidais somam ondas aos embeddings, enquanto RoPE rotaciona vetores no plano.",
            "O RoPE transforma a posição absoluta em distância relativa pura via produto de matrizes ortogonais, sendo o padrão do LLaMA 3 e dos LLMs de longo contexto."
        ],
        "proxima": r"Parabéns! Você completou a jornada das 43 Aulas Visuais de Matemática Essencial para IA! Da geometria dos vetores até o coração dos Transformers, você agora domina os fundamentos matemáticos que movem a inteligência artificial moderna.",
        "referencias": [
            {"obra": "Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding", "trecho": "Paper seminal (arXiv:2104.09864)", "uso": "Dedução teórica completa da formulação complexa e matricial de RoPE"},
            {"obra": "Vaswani et al. (2017). Attention Is All You Need", "trecho": "Seção 3.5: Positional Encoding", "uso": "Formulação original com funções trigonométricas de frequências geométricas"}
        ]
    }
}
