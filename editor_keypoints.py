from base64 import b64encode
from io import BytesIO
from math import isfinite
from pathlib import Path
from uuid import uuid4

from PIL import Image
import streamlit as st


PASTA = Path(__file__).parent / "componentes"


def registrar_ponto(dados, numero_objeto, nome, x, y, largura, altura):
    """Valida antes de alterar. Retorna True somente se houve uma mudança."""
    if any(type(valor) not in (int, float) or not isfinite(valor) for valor in (x, y)):
        return False
    if not (0 <= x <= largura - 1 and 0 <= y <= altura - 1):
        return False

    for objeto in dados["resultados_dentes"]:
        if objeto["numero_objeto"] != numero_objeto or nome not in objeto["pontos"]:
            continue
        ponto = (float(x), float(y))
        anterior = objeto["pontos"][nome]
        if anterior is not None and tuple(anterior) == ponto:
            return False
        objeto["pontos"][nome] = ponto
        # Recusa eventos atrasados, inclusive após outro ajuste no mesmo ponto.
        dados["versao_editor"] = uuid4().hex
        return True
    return False


def aplicar_arraste(dados, evento, numero_objeto, nomes, largura, altura):
    """Só aceita eventos da revisão e do objeto que estão sendo exibidos."""
    if not isinstance(evento, dict):
        return False
    if not dados.get("versao_editor") or evento.get("versao") != dados["versao_editor"]:
        return False
    if evento.get("objeto") != numero_objeto or evento.get("nome") not in nomes:
        return False
    return registrar_ponto(
        dados, numero_objeto, evento["nome"], evento.get("x"), evento.get("y"), largura, altura
    )


def mostrar_editor_keypoints(dados, objeto, nomes):
    """Retorna uma alteração ao soltar o ponto; não envia cada movimento."""
    componente_keypoints = st.components.v2.component(
        "sperio_editor_keypoints",
        html='<div class="editor-keypoints"></div>',
        css=(PASTA / "editor_keypoints.css").read_text(encoding="utf-8"),
        js=(PASTA / "editor_keypoints.js").read_text(encoding="utf-8"),
    )
    if "versao_editor" not in dados:
        dados["versao_editor"] = uuid4().hex
    with Image.open(BytesIO(dados["imagem_bytes"])) as imagem:
        largura, altura = imagem.size
        tipo = Image.MIME.get(imagem.format, "image/png")
    imagem_url = f"data:{tipo};base64," + b64encode(dados["imagem_bytes"]).decode("ascii")

    resultado = componente_keypoints(
        key=f"editor_visual_{objeto['numero_objeto']}",
        data={
            "imagem": imagem_url,
            "largura": largura,
            "altura": altura,
            "objeto": objeto["numero_objeto"],
            "caixa": objeto["caixa"],
            "pontos": {nome: objeto["pontos"][nome] for nome in nomes},
            "versao": dados["versao_editor"],
        },
        on_edicao_change=lambda: None,
    )
    return resultado.edicao
