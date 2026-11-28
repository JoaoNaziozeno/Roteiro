# -*- coding: utf-8 -*-
"""
Conferência dos geradores de conta do Treino: para cada gerador (treino_contas*.py), a resposta refeita aqui
com o NumPy (ou com Python puro, por outro caminho) a partir dos dados sorteados (o campo "d" da questão).
Usado por test_treino.py.
"""
import math

import numpy as np


# ---------------------------------------------------------------- respostas refeitas com o NumPy
def _cos(u, v):
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


def _transf(d):
    k = d["k"]
    rot = lambda g: np.round([[np.cos(g), -np.sin(g)], [np.sin(g), np.cos(g)]]).astype(int).tolist()
    return {"rot90": rot(np.pi / 2), "rot-90": rot(-np.pi / 2), "rot180": rot(np.pi), "refx": [[1, 0], [0, -1]],
            "refy": [[-1, 0], [0, 1]], "esc": [[k, 0], [0, k]], "estx": [[k, 0], [0, 1]]}[d["nome"]]


def _forma(d):
    try:
        return "x".join(map(str, (np.zeros(d["a"]) @ np.zeros(d["w"])).shape))
    except ValueError:
        return "erro"


def _eigvec(d):
    A, v = np.array(d["A"], float), np.array(d["v"], float)
    w = A @ v
    return float(w[0] / v[0]) if abs(w[0] * v[1] - w[1] * v[0]) < 1e-9 else "nao"


def _ncomp(d):
    acc = np.cumsum(d["l"]) / np.sum(d["l"]) * 100
    return int(np.argmax(acc >= d["meta"] - 1e-9)) + 1


def _svd(d):
    U, S, Vt = np.linalg.svd(np.ones((d["m"], d["k"])), full_matrices=d["full"])
    return "x".join(map(str, {"U": U, "S": S, "Vt": Vt}[d["what"]].shape))


def _det(M):
    return float(np.linalg.det(np.array(M, float)))


CHECK = {
    "vsoma": lambda d: np.add(d["u"], d["v"]),
    "vescala": lambda d: d["a"] * np.array(d["u"]),
    "vcomb": lambda d: d["a"] * np.array(d["u"]) + d["b"] * np.array(d["v"]),
    "vdesloc": lambda d: np.subtract(d["B"], d["A"]),
    "combcoef": lambda d: np.linalg.solve(np.array([d["b1"], d["b2"]], float).T, d["w"]),
    "base2": lambda d: _det(np.array([d["u"], d["v"]]).T),
    "dot": lambda d: float(np.dot(d["u"], d["v"])),
    "dotang": lambda d: {1: "agudo", 0: "reto", -1: "obtuso"}[int(np.sign(np.dot(d["u"], d["v"])))],
    "projesc": lambda d: float(np.dot(d["u"], d["v"]) / np.linalg.norm(d["v"])),
    "ortok": lambda d: -d["u"][1] * d["c"] / d["u"][0],
    "l2": lambda d: float(np.linalg.norm(d["v"])),
    "l1": lambda d: float(np.linalg.norm(d["v"], 1)),
    "dist2": lambda d: float(np.linalg.norm(np.subtract(d["B"], d["A"]))),
    "manh": lambda d: float(np.abs(np.subtract(d["B"], d["A"])).sum()),
    "cos": lambda d: _cos(d["u"], d["v"]),
    "cosesp": lambda d: _cos(d["u"], d["v"]),
    "angesp": lambda d: float(np.degrees(np.arccos(np.clip(_cos(d["u"], d["v"]), -1, 1)))),
    "matvec": lambda d: np.array(d["A"]) @ d["x"],
    "matcol": lambda d: np.array(d["A"]) @ d["e"],
    "transf": _transf,
    "matmulij": lambda d: float((np.array(d["A"]) @ np.array(d["B"]))[d["i"], d["j"]]),
    "matmul2": lambda d: np.array(d["A"]) @ np.array(d["B"]),
    "hada": lambda d: np.array(d["A"]) * np.array(d["B"]),
    "forma": _forma,
    "det2": lambda d: _det(d["A"]),
    "det3": lambda d: _det(d["A"]),
    "sist2": lambda d: np.linalg.solve(np.array(d["A"], float), d["b"]),
    "detarea": lambda d: abs(_det(d["A"])),
    "detsing": lambda d: d["b"] * d["c"] / d["a"],
    "inv2": lambda d: np.linalg.inv(np.array(d["A"], float)),
    "invdiag": lambda d: np.linalg.inv(np.array(d["D"], float)),
    "axb": lambda d: np.linalg.solve(np.array(d["A"], float), d["b"]),
    "eigtri": lambda d: sorted(np.linalg.eigvals(np.array(d["A"], float)).real),
    "eigtd": lambda d: sorted(np.roots([1, -d["T"], d["D"]]).real),
    "eigvec": _eigvec,
    "eigpot": lambda d: d["lam"] ** d["k"] * np.array(d["v"]),
    "varexp": lambda d: 100 * d["l"][0] / sum(d["l"]),
    "varsing": lambda d: 100 * d["s"][0] ** 2 / sum(x * x for x in d["s"]),
    "ncomp": _ncomp,
    "svdshape": _svd,
    "pcaproj": lambda d: float((np.array(d["x"]) - d["mu"]) @ np.array(d["w"])),
}
ORDEM_LIVRE = ("eigtri", "eigtd")   # par de autovalores: a ordem não importa


def _arr(v):
    return np.array(v, dtype=float)


def perto(v, esperado, casas):
    """A alternativa certa bate com a conta, até o arredondamento que aparece na tela."""
    if isinstance(v, str) or isinstance(esperado, str):
        return v == esperado
    a, b = _arr(v), _arr(esperado)
    return a.shape == b.shape and bool(np.all(np.abs(a - b) <= 0.5 * 10 ** -casas + 1e-9))


def distinta(v, esperado, casas):
    """A alternativa errada fica longe da certa (pelo menos meia unidade da última casa mostrada)."""
    if isinstance(v, str) or isinstance(esperado, str):
        return v != esperado
    a, b = _arr(v), _arr(esperado)
    return a.shape != b.shape or bool(np.any(np.abs(a - b) >= 0.5 * 10 ** -casas))


# ---------------------------------------------------------------- Fundamentos e Cálculo (treino_contas_calc.py)
def _dnum(f, x, h=1e-5):
    """Derivada numérica (diferença central): outro caminho até a resposta das contas de derivada."""
    return (f(x + h) - f(x - h)) / (2 * h)


def _inequa(d):
    k = (d["c"] - d["b"]) / d["a"]
    flip = {">": "<", "<": ">", r"\geq": r"\leq", r"\leq": r"\geq"}
    return f"{d['op'] if d['a'] > 0 else flip[d['op']]}|{int(round(k))}"


def _logprop(d):
    a, b = d["a"], d["b"]
    return float({"prod": np.log2(a * b), "div": np.log2(a / b), "pot": np.log2(float(a) ** d["k"])}[d["tipo"]])


def _knn(d):
    P, q = np.array(d["P"], float), np.array(d["q"], float)
    dist = np.linalg.norm(P - q, axis=1) if d["metr"] == "euclidiana" else np.abs(P - q).sum(axis=1)
    return "ABC"[int(np.argmin(dist))]


def _dpot(d):
    f = lambda x: d["a"] * x ** d["k"]
    d1, d2 = _dnum(f, 1.7), _dnum(f, 2.3)
    e = round(math.log(d2 / d1) / math.log(2.3 / 1.7))     # descobre o expoente da derivada pela razão
    return [d1 / 1.7 ** e, e]


def _sig(z):
    return 1 / (1 + math.exp(-z))


def _f2(d):
    return lambda x, y: d["a"] * x * x + d["b"] * x * y + d["c"] * y * y


def _hess(d):
    f, h = _f2(d), 1e-3
    fxx = (f(h, 0) - 2 * f(0, 0) + f(-h, 0)) / h ** 2
    fyy = (f(0, h) - 2 * f(0, 0) + f(0, -h)) / h ** 2
    fxy = (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h * h)
    return [[fxx, fxy], [fxy, fyy]]


def _sela(d):
    ev = np.linalg.eigvalsh(np.array(d["H"], float))
    return "min" if np.all(ev > 0) else "max" if np.all(ev < 0) else "sela"


def _jacob(d):
    F = lambda x, y: np.array([x * x + d["a"] * y, d["b"] * x * y], float)
    x0, y0, h = d["x0"], d["y0"], 1e-5
    jx = (F(x0 + h, y0) - F(x0 - h, y0)) / (2 * h)
    jy = (F(x0, y0 + h) - F(x0, y0 - h)) / (2 * h)
    return np.column_stack([jx, jy])


def _gd(d, passos):
    w = d["w0"]
    for _ in range(passos):
        w = w - d["eta"] * _dnum(lambda v: (v - d["c"]) ** 2, w)
    return w


def _gdlr(d):
    w, sinais = 1.0, set()
    for _ in range(60):
        w -= d["eta"] * 2 * d["a"] * w
        sinais.add(np.sign(w))
        if abs(w) > 1e3:
            return "diverge"
    return "oscila" if len(sinais) > 1 else "suave"


CHECK.update({
    "linz": lambda d: float(np.dot(d["w"], d["x"]) + d["b"]),
    "linlado": lambda d: float(np.dot(d["w"], d["x"]) + d["b"]),
    "distplano": lambda d: float(abs(np.dot(d["w"], d["x"]) + d["b"]) / np.linalg.norm(d["w"])),
    "inequa": _inequa,
    "logprop": _logprop,
    "logeq": lambda d: float(np.log2(d["rhs"] / d["c"])),
    "lse": lambda d: float(np.logaddexp.reduce([float(d["a"])] * d["k"])),
    "expdecay": lambda d: d["L0"] * 0.5 ** d["t"],
    "soma": lambda d: sum(d["a"] * i + d["b"] for i in range(1, d["N"] + 1)),
    "prod": lambda d: float(np.prod(d["x"])),
    "argmax": lambda d: int(np.argmax(d["x"])) + 1,
    "indic": lambda d: float(np.mean(np.array(d["y"]) == np.array(d["yh"]))),
    "knn": _knn,
    "secante": lambda d: (d["a"] * (d["x0"] + d["h"]) ** 2 - d["a"] * d["x0"] ** 2) / d["h"],
    "derivlim": lambda d: _dnum(lambda x: d["a"] * x * x + d["b"] * x, d["x0"]),
    "limfrac": lambda d: (d["k"] * (d["c"] + 1e-7) ** 2 - d["k"] * d["c"] ** 2) / 1e-7,
    "diffnum": lambda d: ((d["x0"] + d["h"]) ** 3 - (d["x0"] - d["h"]) ** 3) / (2 * d["h"]),
    "dpoly": lambda d: float(np.polyval(np.polyder(d["cs"]), d["x0"])),
    "dpot": _dpot,
    "dprod": lambda d: _dnum(lambda x: (x + d["a"]) * (x * x + d["b"]), d["x0"]),
    "dmse": lambda d: _dnum(lambda w: (w * d["x"] - d["y"]) ** 2, d["w"]),
    "cadeia": lambda d: _dnum(lambda x: (d["a"] * x + d["b"]) ** d["k"], d["x0"]),
    "cadeialn": lambda d: _dnum(lambda x: math.log(d["a"] * x + d["b"]), d["x0"]),
    "cadeia3": lambda d: _dnum(lambda x: (d["pp"] * d["m"] * x + d["qq"]) ** 2, d["x0"]),
    "passo1": lambda d: d["w"] - d["eta"] * _dnum(lambda w: (w * d["x"] + d["b"] - d["y"]) ** 2, d["w"]),
    "sigd": lambda d: _dnum(_sig, math.log(d["s"] / (1 - d["s"]))),
    "relud": lambda d: (np.array(d["z"]) > 0).astype(float),
    "tanhd": lambda d: _dnum(math.tanh, math.atanh(d["t"])),
    "vanish": lambda d: 0.25 ** d["k"],
    "parcial": lambda d: (_dnum(lambda x: _f2(d)(x, d["y0"]), d["x0"]) if d["qual"] == "x" else _dnum(lambda y: _f2(d)(d["x0"], y), d["y0"])),
    "grad": lambda d: [_dnum(lambda x: d["a"] * x * x + d["b"] * d["y0"] ** 2 + d["c"] * x * d["y0"], d["x0"]),
                       _dnum(lambda y: d["a"] * d["x0"] ** 2 + d["b"] * y * y + d["c"] * d["x0"] * y, d["y0"])],
    "graddir": lambda d: -np.array(d["g"], float),
    "hess": _hess,
    "sela": _sela,
    "jacob": _jacob,
    "gdpasso": lambda d: _gd(d, 1),
    "gd2": lambda d: _gd(d, 2),
    "gdlr": _gdlr,
    "minibatch": lambda d: math.ceil(d["N"] / d["B"]),
    "momentum": lambda d: 0.9 * d["vp"] + 0.1 * d["g"],
    "rmsprop": lambda d: 0.9 * d["s"] + 0.1 * d["g"] ** 2,
    "adambias": lambda d: [0.1 * d["g"], 0.1 * d["g"] / (1 - 0.9 ** 1)],
    "warmup": lambda d: d["em"] * d["t"] / d["Tw"],
    "cosdecay": lambda d: 0.5 * d["em"] * (1 + math.cos(math.pi * d["t"] / d["T"])),
})


# ---------------------------------------------------------------- Probabilidade, Estatística e Informação (treino_contas_prob.py)
def _regra(k):
    v = {1: 68, 2: 95, 3: 99.7}[k]
    assert abs(100 * math.erf(k / math.sqrt(2)) - v) < 0.5, k      # a regra 68-95-99,7 bate com a normal de verdade
    return v


def _pmfcum(d):
    ps, k = np.array(d["ps"], float), d["k"]
    return float(ps[:k + 1].sum() if d["tipo"] == "le" else ps[k + 1:].sum())


def _bayes(d):
    N = 1_000_000                                                  # por contagem, numa população grande
    doentes = N * d["prev"]
    vp, falsos = doentes * d["sens"], (N - doentes) * d["fp"]
    return 100 * vp / (vp + falsos)


def _ic(d):
    se = d["sd"] / math.sqrt(d["m"])
    return [d["xb"] - 1.96 * se, d["xb"] + 1.96 * se]


def _H(ps):
    ps = np.array(ps, float)
    return float(-(ps * np.log2(ps)).sum())


def _softmax(d):
    z = np.array(d["z"], float)
    e = np.exp(z - z.max())
    return float((e / e.sum())[d["i"]])


def _cegrad(d):
    y = np.zeros(3)
    y[d["c"]] = 1
    return np.array(d["ps"], float) - y


def _kl(d):
    Pd, Qd = np.array(d["P"], float), np.array(d["Q"], float)
    return float((Pd * np.log2(Pd / Qd)).sum())


CHECK.update({
    "pmffalta": lambda d: 1 - sum(p for j, p in enumerate(d["ps"]) if j != d["i"]),
    "pmfcum": _pmfcum,
    "unifarea": lambda d: (d["hi"] - d["lo"]) / d["b"],
    "media": lambda d: float(np.mean(d["xs"])),
    "mediana": lambda d: float(np.median(d["xs"])),
    "variancia": lambda d: float(np.var(d["xs"]) if d["tipo"] == "var" else np.std(d["xs"])),
    "zscore": lambda d: (d["x"] - d["mu"]) / d["sd"],
    "esper": lambda d: float(np.dot(d["xs"], d["ps"])),
    "esperjogo": lambda d: d["pw"] * d["W"] - (1 - d["pw"]) * d["Lo"],
    "cov": lambda d: float(np.cov(d["xs"], d["ys"], bias=True)[0, 1]),
    "corrsinal": lambda d: float(np.corrcoef(d["xs"], d["ys"])[0, 1]),
    "bayes": _bayes,
    "condtab": lambda d: 100 * d["a"] / (d["a"] + d["c"]),
    "odds": lambda d: 100 * (d["LR"] / d["k"]) / (1 + d["LR"] / d["k"]),
    "pelomenos": lambda d: 100 * (1 - (1 - d["pr"]) ** d["m"]),
    "regra689": lambda d: _regra(d["k"]),
    "normtail": lambda d: (100 - _regra(d["k"])) / 2,
    "bernoulliL": lambda d: d["pr"] ** d["h"] * (1 - d["pr"]) ** (d["m"] - d["h"]),
    "erropadrao": lambda d: d["sd"] / math.sqrt(d["m"]),
    "amostra4x": lambda d: d["k"] ** 2,
    "ic95": _ic,
    "pvalor": lambda d: "rej" if d["pv"] < d["alpha"] else "nrej",
    "zteste": lambda d: (d["xb"] - d["mu0"]) / (d["sd"] / math.sqrt(d["m"])),
    "mlebern": lambda d: d["h"] / d["m"],
    "nll": lambda d: float(-np.log(d["ps"]).sum()),
    "mlemu": lambda d: float(np.mean(d["xs"])),
    "biasvar": lambda d: d["b"] ** 2 + d["va"] + d["ru"],
    "diagfit": lambda d: "under" if d["tr"] >= 20 else "over" if d["va"] - d["tr"] >= 10 else "bom",
    "amostrasn": lambda d: 16 * d["pr"] * (1 - d["pr"]) / d["d"] ** 2,
    "icdiff": lambda d: "pos" if d["lo"] > 0 else "neg" if d["hi"] < 0 else "acaso",
    "acuraciase": lambda d: 200 * math.sqrt(d["pr"] * (1 - d["pr"]) / d["m"]),
    "entropia": lambda d: _H(d["ps"]),
    "surpresa": lambda d: float(-np.log2(1 / d["den"])),
    "entmax": lambda d: _H([1 / d["k"]] * d["k"]),
    "softmax": _softmax,
    "ce": lambda d: -math.log(d["pr"]),
    "cegrad": _cegrad,
    "kl": _kl,
    "ceent": lambda d: d["HPQ"] - d["HP"],
    "mse": lambda d: float(np.mean((np.array(d["yh"]) - np.array(d["y"])) ** 2)),
    "mae": lambda d: float(np.mean(np.abs(np.array(d["yh"]) - np.array(d["y"])))),
    "huber": lambda d: 0.5 * d["r"] ** 2 if abs(d["r"]) <= 1 else abs(d["r"]) - 0.5,
})


# ---------------------------------------------------------------- Transformers e embeddings (treino_contas_transf.py)
def _shape_qkv(d):
    X, W = np.zeros((d["n"], d["dm"])), np.zeros((d["dm"], d["dk"]))
    Q = K = V = X @ W
    S = Q @ K.T
    return "x".join(map(str, {"Q": Q, "S": S, "O": S @ V}[d["what"]].shape))


def _shape_mha(d):
    n, dm, h = d["n"], d["dm"], d["h"]
    Q = (np.zeros((n, dm)) @ np.zeros((dm, dm))).reshape(n, h, dm // h)      # divide em cabeças
    cabeca = Q[:, 0, :]
    out = {"cabeca": cabeca, "concat": Q.reshape(n, -1), "atencao": cabeca @ cabeca.T}[d["what"]]
    return "x".join(map(str, out.shape))


def _rot(d):
    g = math.radians(d["ang"])
    return np.round(np.array([[math.cos(g), -math.sin(g)], [math.sin(g), math.cos(g)]]) @ np.array(d["x"], float), 9)


def _dist2cos(d):
    u, v = np.array([1.0, 0.0]), np.array([d["c"], math.sqrt(1 - d["c"] ** 2)])    # dois vetores unitários com esse cosseno
    D = float(np.sum((u - v) ** 2))
    return D if d["tipo"] == "d" else 1 - D / 2


CHECK.update({
    "quaseort": lambda d: 1 / math.sqrt(d["d"]),
    "normsq": lambda d: math.sqrt(d["d"]),
    "paramsffn": lambda d: np.zeros((d["dm"], 4 * d["dm"])).size + np.zeros((4 * d["dm"], d["dm"])).size,
    "normaliza": lambda d: np.array(d["v"], float) / np.linalg.norm(d["v"]),
    "dist2cos": _dist2cos,
    "rmsnorm": lambda d: np.array(d["x"], float) / np.sqrt(np.mean(np.square(d["x"]))),
    "qkvshape": _shape_qkv,
    "qproj": lambda d: np.array(d["x"], float) @ np.array(d["W"], float),
    "paramsqkv": lambda d: 3 * np.zeros((d["dm"], d["dm"])).size,
    "attscore": lambda d: d["s"] / math.sqrt(d["dk"]),
    "attpesos": lambda d: float(np.exp(d["s"][0]) / np.exp(d["s"]).sum()),
    "attout": lambda d: d["w"][0] * np.array(d["v1"], float) + d["w"][1] * np.array(d["v2"], float),
    "varscale": lambda d: math.sqrt(d["dk"]),
    "dk": lambda d: d["dm"] / d["h"],
    "mhashape": _shape_mha,
    "mhaparams": lambda d: 4 * np.zeros((d["dm"], d["dm"])).size,
    "rope": _rot,
    "roperel": lambda d: d["m"] - d["k"],
    "pefreq": lambda d: len(range(0, d["d"], 2)),
})
