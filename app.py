from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from pathlib import Path
import json
import webbrowser
import threading

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "jogos.json"

app = Flask(__name__)

def carregar_dados():
    if not DATA_FILE.exists():
        return {"config": {"nome_site": "NIGHTFALL GAMES", "subtitulo": "Downloads e novidades do mundo dos jogos"}, "jogos": []}
    with DATA_FILE.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_dados(dados):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

@app.route("/")
def inicio():
    dados = carregar_dados()
    destaques = [j for j in dados.get("jogos", []) if j.get("destaque")][:3]
    if not destaques:
        destaques = dados.get("jogos", [])[:3]
    return render_template("index.html", config=dados.get("config", {}), destaques=destaques)

@app.route("/downloads")
def downloads():
    dados = carregar_dados()
    busca = request.args.get("q", "").strip().lower()
    jogos = dados.get("jogos", [])
    if busca:
        jogos = [
            j for j in jogos
            if busca in j.get("nome", "").lower()
            or busca in j.get("categoria", "").lower()
            or busca in j.get("descricao", "").lower()
        ]
    return render_template("downloads.html", config=dados.get("config", {}), jogos=jogos, busca=busca)

@app.route("/config")
def configuracao():
    dados = carregar_dados()
    return render_template("config.html", config=dados.get("config", {}), jogos=dados.get("jogos", []))

@app.route("/api/config", methods=["POST"])
def atualizar_config():
    dados = carregar_dados()
    payload = request.get_json(force=True)
    dados["config"] = {
        "nome_site": str(payload.get("nome_site", "NIGHTFALL GAMES")).strip()[:80],
        "subtitulo": str(payload.get("subtitulo", "")).strip()[:180]
    }
    salvar_dados(dados)
    return jsonify({"ok": True})

@app.route("/api/jogos", methods=["POST"])
def adicionar_jogo():
    dados = carregar_dados()
    payload = request.get_json(force=True)

    nome = str(payload.get("nome", "")).strip()
    link = str(payload.get("link", "")).strip()

    if not nome or not link:
        return jsonify({"ok": False, "erro": "Nome e link são obrigatórios."}), 400

    proximo_id = max([int(j.get("id", 0)) for j in dados.get("jogos", [])] + [0]) + 1

    jogo = {
        "id": proximo_id,
        "nome": nome[:100],
        "categoria": str(payload.get("categoria", "Jogo")).strip()[:60],
        "descricao": str(payload.get("descricao", "")).strip()[:350],
        "imagem": str(payload.get("imagem", "")).strip()[:500],
        "link": link[:1000],
        "versao": str(payload.get("versao", "")).strip()[:40],
        "tamanho": str(payload.get("tamanho", "")).strip()[:40],
        "destaque": bool(payload.get("destaque", False))
    }

    dados.setdefault("jogos", []).append(jogo)
    salvar_dados(dados)
    return jsonify({"ok": True, "jogo": jogo})

@app.route("/api/jogos/<int:jogo_id>", methods=["PUT"])
def editar_jogo(jogo_id):
    dados = carregar_dados()
    payload = request.get_json(force=True)

    for jogo in dados.get("jogos", []):
        if int(jogo.get("id", 0)) == jogo_id:
            jogo.update({
                "nome": str(payload.get("nome", jogo.get("nome", ""))).strip()[:100],
                "categoria": str(payload.get("categoria", jogo.get("categoria", ""))).strip()[:60],
                "descricao": str(payload.get("descricao", jogo.get("descricao", ""))).strip()[:350],
                "imagem": str(payload.get("imagem", jogo.get("imagem", ""))).strip()[:500],
                "link": str(payload.get("link", jogo.get("link", ""))).strip()[:1000],
                "versao": str(payload.get("versao", jogo.get("versao", ""))).strip()[:40],
                "tamanho": str(payload.get("tamanho", jogo.get("tamanho", ""))).strip()[:40],
                "destaque": bool(payload.get("destaque", jogo.get("destaque", False)))
            })
            salvar_dados(dados)
            return jsonify({"ok": True})

    return jsonify({"ok": False, "erro": "Jogo não encontrado."}), 404

@app.route("/api/jogos/<int:jogo_id>", methods=["DELETE"])
def excluir_jogo(jogo_id):
    dados = carregar_dados()
    jogos_antes = len(dados.get("jogos", []))
    dados["jogos"] = [j for j in dados.get("jogos", []) if int(j.get("id", 0)) != jogo_id]

    if len(dados["jogos"]) == jogos_antes:
        return jsonify({"ok": False, "erro": "Jogo não encontrado."}), 404

    salvar_dados(dados)
    return jsonify({"ok": True})

def abrir_navegador():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.2, abrir_navegador).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
