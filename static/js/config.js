async function salvarConfig() {
    const resposta = await fetch("/api/config", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            nome_site: document.getElementById("nome_site").value,
            subtitulo: document.getElementById("subtitulo").value
        })
    });

    if (resposta.ok) {
        alert("Dados do site salvos.");
        location.reload();
    } else {
        alert("Não foi possível salvar.");
    }
}

async function adicionarJogo() {
    const mensagem = document.getElementById("mensagem");
    mensagem.textContent = "Salvando...";

    const dados = {
        nome: document.getElementById("nome").value,
        categoria: document.getElementById("categoria").value,
        versao: document.getElementById("versao").value,
        tamanho: document.getElementById("tamanho").value,
        imagem: document.getElementById("imagem").value,
        link: document.getElementById("link").value,
        descricao: document.getElementById("descricao").value,
        destaque: document.getElementById("destaque").checked
    };

    const resposta = await fetch("/api/jogos", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(dados)
    });

    const retorno = await resposta.json();

    if (!resposta.ok) {
        mensagem.textContent = retorno.erro || "Erro ao cadastrar.";
        return;
    }

    mensagem.textContent = "Jogo cadastrado com sucesso.";
    setTimeout(() => location.reload(), 700);
}

async function excluirJogo(id) {
    if (!confirm("Excluir este jogo?")) return;

    const resposta = await fetch(`/api/jogos/${id}`, {
        method: "DELETE"
    });

    if (resposta.ok) {
        const item = document.getElementById(`jogo-${id}`);
        if (item) item.remove();
    } else {
        alert("Não foi possível excluir.");
    }
}
