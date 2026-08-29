import torch

import streamlit as st
from pathlib import Path
from io import BytesIO
from math import hypot
from PIL import Image, ImageDraw
from ultralytics import YOLO


pasta_projeto = Path(__file__).parent

caminho_modelo = (
    pasta_projeto
    / "models"
    / "perio_kpt_oficial_fold0_best.pt"
)

CONFIANCA_POSE = 0.48
IOU_POSE = 0.30

NOMES_KEYPOINTS = [
    "CEJ-m",
    "BL-m",
    "RL-m",
    "CEJ-d",
    "BL-d",
    "RL-d",
    "RL-c",
    "FA",
    "FBL-m",
    "FBL-d",
    "ARR"
]

KEYPOINTS_DESENHAR = [
    "CEJ-m",
    "BL-m",
    "RL-m",
    "CEJ-d",
    "BL-d",
    "RL-d",
    "RL-c"
]

CLASSES_PERIO_KPT = {
    0: "Single Root",
    1: "Double Root",
    2: "Tripple Root",
    3: "ARR",
    4: "PLS"
}


def calcular_pbl(cej, bl, apice):

    if cej is None or bl is None or apice is None:
        return None

    distancia_cej_apice = hypot(
        cej[0] - apice[0],
        cej[1] - apice[1]
    )

    if distancia_cej_apice == 0:
        return None

    distancia_bl_apice = hypot(
        bl[0] - apice[0],
        bl[1] - apice[1]
    )

    percentual_pbl = (
        (distancia_cej_apice - distancia_bl_apice)
        / distancia_cej_apice
    ) * 100

    return percentual_pbl


def desenhar_linhas_distancia(desenho, cej, bl, apice):

    if cej is not None and apice is not None:
        desenho.line(
            [cej, apice],
            fill="lime",
            width=3
        )

    if bl is not None and apice is not None:
        desenho.line(
            [bl, apice],
            fill="cyan",
            width=3
        )


def invalidar_calculo_radiografico():

    dados_radiograficos = st.session_state["dados_radiograficos"]

    dados_radiograficos["pbl_calculado"] = False
    dados_radiograficos["pbl_maximo"] = None
    dados_radiograficos["dente_determinante"] = None
    dados_radiograficos["superficie_determinante"] = None
    dados_radiograficos["confirmado"] = False

    for resultado_dente in dados_radiograficos["resultados_dentes"]:
        resultado_dente["pbl_mesial"] = None
        resultado_dente["pbl_distal"] = None

    st.session_state["avaliacao"]["pbl"] = None
    st.session_state["avaliacao"]["periodontal"] = None


def atualizar_coordenada_keypoint(numero_objeto, nome_keypoint):

    chave_x = f"keypoint_{numero_objeto}_{nome_keypoint}_x"
    chave_y = f"keypoint_{numero_objeto}_{nome_keypoint}_y"

    for resultado_dente in st.session_state["dados_radiograficos"][
        "resultados_dentes"
    ]:
        if resultado_dente["numero_objeto"] == numero_objeto:
            resultado_dente["pontos"][nome_keypoint] = (
                st.session_state[chave_x],
                st.session_state[chave_y]
            )
            break

    invalidar_calculo_radiografico()


def criar_imagem_anotada(imagem_bytes, resultados_dentes, mostrar_linhas):

    imagem_anotada = Image.open(
        BytesIO(imagem_bytes)
    ).convert("RGB")

    desenho = ImageDraw.Draw(imagem_anotada)

    for resultado_dente in resultados_dentes:
        x1, y1, x2, y2 = resultado_dente["caixa"]
        pontos_objeto = resultado_dente["pontos"]
        ignorado = resultado_dente["ignorado"]

        cor_caixa = "gray" if ignorado else "yellow"
        texto_classe = (
            f"Objeto {resultado_dente['numero_objeto']} - "
            f"{resultado_dente['classe_radicular']}"
        )

        if ignorado:
            texto_classe += " - ignorado"

        desenho.rectangle(
            [(x1, y1), (x2, y2)],
            outline=cor_caixa,
            width=3
        )

        desenho.text(
            (x1, y1 - 15),
            texto_classe,
            fill=cor_caixa
        )

        if mostrar_linhas and not ignorado:
            desenhar_linhas_distancia(
                desenho,
                pontos_objeto["CEJ-m"],
                pontos_objeto["BL-m"],
                pontos_objeto[resultado_dente["referencia_mesial"]]
            )

            desenhar_linhas_distancia(
                desenho,
                pontos_objeto["CEJ-d"],
                pontos_objeto["BL-d"],
                pontos_objeto[resultado_dente["referencia_distal"]]
            )

        for nome in KEYPOINTS_DESENHAR:
            ponto = pontos_objeto[nome]

            if ponto is None:
                continue

            x, y = ponto
            raio = 5

            desenho.ellipse(
                [
                    (x - raio, y - raio),
                    (x + raio, y + raio)
                ],
                fill="red",
                outline="white"
            )

            desenho.text(
                (x + 6, y - 6),
                nome,
                fill="white"
            )

    buffer_imagem = BytesIO()
    imagem_anotada.save(buffer_imagem, format="PNG")

    return buffer_imagem.getvalue()


def calcular_pbl_dos_dentes(resultados_dentes):

    pbl_maximo = None
    dente_determinante = None
    superficie_determinante = None

    for resultado_dente in resultados_dentes:
        if resultado_dente["ignorado"]:
            resultado_dente["pbl_mesial"] = None
            resultado_dente["pbl_distal"] = None
            continue

        pontos_objeto = resultado_dente["pontos"]

        pbl_mesial = calcular_pbl(
            pontos_objeto["CEJ-m"],
            pontos_objeto["BL-m"],
            pontos_objeto[resultado_dente["referencia_mesial"]]
        )

        pbl_distal = calcular_pbl(
            pontos_objeto["CEJ-d"],
            pontos_objeto["BL-d"],
            pontos_objeto[resultado_dente["referencia_distal"]]
        )

        resultado_dente["pbl_mesial"] = pbl_mesial
        resultado_dente["pbl_distal"] = pbl_distal

        if pbl_mesial is not None:
            if pbl_maximo is None or pbl_mesial > pbl_maximo:
                pbl_maximo = pbl_mesial
                dente_determinante = resultado_dente["numero_objeto"]
                superficie_determinante = "mesial"

        if pbl_distal is not None:
            if pbl_maximo is None or pbl_distal > pbl_maximo:
                pbl_maximo = pbl_distal
                dente_determinante = resultado_dente["numero_objeto"]
                superficie_determinante = "distal"

    return pbl_maximo, dente_determinante, superficie_determinante


# CARREGA O MODELO E O SALVA NO CACHE DO STREAMLIT
@st.cache_resource
def carregar_modelo_radiografico(caminho):

    modelo = YOLO(
        caminho,
        task="pose"
    )

    return modelo


def mostrar_modulo_radiografico():
    st.header("Análise radiográfica")

    st.write(
        "Carregue uma radiografia periapical, execute o modelo perio-KPT e "
        "revise os resultados antes de continuar para a classificação "
        "periodontal."
    )

    dados_radiograficos = st.session_state["dados_radiograficos"]
    dados_radiograficos.setdefault(
        "pbl_calculado",
        dados_radiograficos["pbl_maximo"] is not None
    )

    modelo_radiografico = None

    if not caminho_modelo.exists():
        st.error("Modelo radiográfico não encontrado.")
        st.write("Caminho esperado:", str(caminho_modelo))

    st.markdown("### 1. Seleção da radiografia")

    imagem_bytes_salva = dados_radiograficos["imagem_bytes"]
    nome_arquivo_salvo = dados_radiograficos["nome_arquivo"]

    rotulo_uploader = "Radiografia periapical:"

    if imagem_bytes_salva is not None:
        rotulo_uploader = "Carregar outra radiografia:"

    imagem_radiografica = st.file_uploader(
        rotulo_uploader,
        type=["png", "jpg", "jpeg"]
    )

    nova_imagem_enviada = imagem_radiografica is not None

    if imagem_radiografica is None and imagem_bytes_salva is not None:
        imagem_radiografica = BytesIO(imagem_bytes_salva)
        imagem_radiografica.name = nome_arquivo_salvo

    if imagem_radiografica is None and imagem_bytes_salva is None:
        return

    nome_novo_arquivo = imagem_radiografica.name
    nome_arquivo_anterior = dados_radiograficos["nome_arquivo"]

    if (
        nova_imagem_enviada
        and nome_novo_arquivo != nome_arquivo_anterior
    ):
        dados_radiograficos["resultados_dentes"] = []
        dados_radiograficos["imagem_anotada_bytes"] = None
        invalidar_calculo_radiografico()

    if nova_imagem_enviada:
        dados_radiograficos["nome_arquivo"] = nome_novo_arquivo
        dados_radiograficos["imagem_bytes"] = imagem_radiografica.getvalue()

    resultados_salvos = dados_radiograficos["resultados_dentes"]

    # Limpa resultados antigos que não possuem coordenadas editáveis.
    if len(resultados_salvos) > 0 and "pontos" not in resultados_salvos[0]:
        dados_radiograficos["resultados_dentes"] = []
        dados_radiograficos["imagem_anotada_bytes"] = None
        invalidar_calculo_radiografico()
        resultados_salvos = []

    imagem_anotada_atual = None

    if len(resultados_salvos) > 0:
        imagem_anotada_atual = criar_imagem_anotada(
            dados_radiograficos["imagem_bytes"],
            resultados_salvos,
            dados_radiograficos["pbl_calculado"]
        )
        dados_radiograficos["imagem_anotada_bytes"] = imagem_anotada_atual

    st.markdown("### 2. Visualização")

    if imagem_anotada_atual is None:
        st.image(
            imagem_radiografica,
            caption="Radiografia original",
            width="stretch"
        )
    else:
        coluna_original, coluna_anotada = st.columns(2)

        with coluna_original:
            st.image(
                imagem_radiografica,
                caption="Radiografia original",
                width="stretch"
            )

        with coluna_anotada:
            st.image(
                imagem_anotada_atual,
                caption="Classes e keypoints revisados",
                width="stretch"
            )

            if dados_radiograficos["pbl_calculado"]:
                st.caption(
                    "Linhas verdes: CEJ-ápice. "
                    "Linhas azuis: BL-ápice."
                )

    st.caption(
        "Arquivo em sessão: "
        + dados_radiograficos["nome_arquivo"]
    )

    if caminho_modelo.exists():
        try:
            modelo_radiografico = carregar_modelo_radiografico(
                str(caminho_modelo)
            )
            st.caption("Modelo perio-KPT carregado e pronto para análise.")

        except Exception as erro:
            st.error("O modelo radiográfico não pôde ser carregado.")
            st.write("Erro:", str(erro))

    if (
        dados_radiograficos["imagem_bytes"] is not None
        and modelo_radiografico is not None
    ):
        if st.button(
            "Analisar radiografia",
            type="primary",
            width="stretch"
        ):
            try:
                imagem_para_modelo = Image.open(
                    BytesIO(dados_radiograficos["imagem_bytes"])
                ).convert("RGB")

                estado_mkldnn = torch.backends.mkldnn.enabled
                torch.backends.mkldnn.enabled = False

                try:
                    resultados = modelo_radiografico.predict(
                        source=imagem_para_modelo,
                        conf=CONFIANCA_POSE,
                        iou=IOU_POSE,
                        device="cpu",
                        save=False,
                        verbose=False
                    )

                finally:
                    torch.backends.mkldnn.enabled = estado_mkldnn

                resultado = resultados[0]

                if resultado.keypoints is None:
                    st.warning(
                        "O modelo retornou objetos sem keypoints."
                    )

                else:
                    todos_keypoints = (
                        resultado.keypoints.data
                        .cpu()
                        .tolist()
                    )

                    todas_caixas = (
                        resultado.boxes.data
                        .cpu()
                        .tolist()
                    )

                    resultados_dentes_analise = []

                    for numero_objeto, dados_objeto in enumerate(
                        zip(todas_caixas, todos_keypoints),
                        start=1
                    ):
                        caixa_objeto, keypoints_objeto = dados_objeto
                        confianca_deteccao = caixa_objeto[4]
                        classe_id = int(caixa_objeto[5])

                        if classe_id not in [0, 1, 2]:
                            continue

                        if len(keypoints_objeto) != len(NOMES_KEYPOINTS):
                            st.warning(
                                "Este objeto não possui exatamente 11 "
                                "keypoints."
                            )
                            continue

                        pontos_objeto = {}

                        for nome, ponto in zip(
                            NOMES_KEYPOINTS,
                            keypoints_objeto
                        ):
                            x, y, confianca = ponto

                            if x == 0 and y == 0:
                                pontos_objeto[nome] = None
                            else:
                                pontos_objeto[nome] = (x, y)

                        if classe_id == 0:
                            referencia_mesial = "RL-c"
                            referencia_distal = "RL-c"
                        else:
                            referencia_mesial = "RL-m"
                            referencia_distal = "RL-d"

                        resultado_dente = {
                            "numero_objeto": numero_objeto,
                            "classe_id": classe_id,
                            "classe_radicular": CLASSES_PERIO_KPT.get(
                                classe_id,
                                "Classe desconhecida"
                            ),
                            "confianca_deteccao": confianca_deteccao,
                            "caixa": caixa_objeto[:4],
                            "pontos": pontos_objeto,
                            "referencia_mesial": referencia_mesial,
                            "referencia_distal": referencia_distal,
                            "pbl_mesial": None,
                            "pbl_distal": None,
                            "ignorado": False
                        }

                        resultados_dentes_analise.append(resultado_dente)

                    dados_radiograficos[
                        "resultados_dentes"
                    ] = resultados_dentes_analise

                    for chave in list(st.session_state.keys()):
                        if (
                            chave.startswith("keypoint_")
                            or chave == "objeto_editar_keypoints"
                            or chave == "objeto_para_ignorar"
                        ):
                            del st.session_state[chave]

                    invalidar_calculo_radiografico()

                    if len(resultados_dentes_analise) == 0:
                        st.warning(
                            "Nenhum dente válido foi encontrado."
                        )
                    else:
                        st.rerun()

            except Exception as erro:
                st.error("Não foi possível analisar a radiografia.")
                st.write("Erro:", str(erro))

    resultados_salvos = dados_radiograficos["resultados_dentes"]

    if len(resultados_salvos) == 0:
        return

    st.markdown("### 3. Revisão das detecções")
    st.caption(
        "A numeração representa a ordem visual dos objetos detectados "
        "e não corresponde à numeração odontológica FDI."
    )

    aba_keypoints, aba_ignorar = st.tabs([
        "Coordenadas dos keypoints",
        "Ignorar dente"
    ])

    with aba_keypoints:
        st.write(
            "Selecione um objeto e ajuste as coordenadas X e Y. "
            "A imagem será atualizada a cada alteração."
        )

        numeros_objetos = [
            resultado_dente["numero_objeto"]
            for resultado_dente in resultados_salvos
        ]

        objeto_para_editar = st.selectbox(
            "Objeto a revisar:",
            numeros_objetos,
            key="objeto_editar_keypoints"
        )

        resultado_para_editar = next(
            resultado_dente
            for resultado_dente in resultados_salvos
            if resultado_dente["numero_objeto"] == objeto_para_editar
        )

        largura_imagem, altura_imagem = Image.open(
            BytesIO(dados_radiograficos["imagem_bytes"])
        ).size

        for nome_keypoint in KEYPOINTS_DESENHAR:
            ponto = resultado_para_editar["pontos"][nome_keypoint]

            if ponto is None:
                st.caption(
                    f"{nome_keypoint}: não detectado pelo modelo. "
                    "Informe X e Y para posicioná-lo."
                )

                coordenada_x = 0.0
                coordenada_y = 0.0

            else:
                coordenada_x = float(ponto[0])
                coordenada_y = float(ponto[1])

            st.markdown(f"**{nome_keypoint}**")
            coluna_x, coluna_y = st.columns(2)

            chave_x = (
                f"keypoint_{objeto_para_editar}_{nome_keypoint}_x"
            )
            chave_y = (
                f"keypoint_{objeto_para_editar}_{nome_keypoint}_y"
            )

            with coluna_x:
                st.number_input(
                    "Coordenada X",
                    min_value=0.0,
                    max_value=float(largura_imagem - 1),
                    value=coordenada_x,
                    step=1.0,
                    format="%.1f",
                    key=chave_x,
                    on_change=atualizar_coordenada_keypoint,
                    args=(objeto_para_editar, nome_keypoint)
                )

            with coluna_y:
                st.number_input(
                    "Coordenada Y",
                    min_value=0.0,
                    max_value=float(altura_imagem - 1),
                    value=coordenada_y,
                    step=1.0,
                    format="%.1f",
                    key=chave_y,
                    on_change=atualizar_coordenada_keypoint,
                    args=(objeto_para_editar, nome_keypoint)
                )

        imagem_revisao = criar_imagem_anotada(
            dados_radiograficos["imagem_bytes"],
            resultados_salvos,
            dados_radiograficos["pbl_calculado"]
        )

        st.image(
            imagem_revisao,
            caption="Posição atual dos keypoints",
            width="stretch"
        )

        if dados_radiograficos["pbl_calculado"]:
            st.caption(
                "Linhas verdes: CEJ-ápice. Linhas azuis: BL-ápice."
            )

    with aba_ignorar:
        st.write(
            "Dentes cortados ou detectados incorretamente podem ser "
            "ignorados e não participarão do cálculo."
        )

        objetos_disponiveis = [
            resultado_dente["numero_objeto"]
            for resultado_dente in resultados_salvos
            if not resultado_dente["ignorado"]
        ]

        if len(objetos_disponiveis) > 0:
            objeto_para_ignorar = st.selectbox(
                "Objeto a ignorar:",
                objetos_disponiveis,
                index=None,
                placeholder="Selecione um objeto",
                key="objeto_para_ignorar"
            )

            if st.button(
                "Ignorar objeto selecionado",
                width="stretch"
            ):
                if objeto_para_ignorar is None:
                    st.warning("Selecione primeiro um objeto.")
                else:
                    for resultado_dente in resultados_salvos:
                        if (
                            resultado_dente["numero_objeto"]
                            == objeto_para_ignorar
                        ):
                            resultado_dente["ignorado"] = True
                            break

                    invalidar_calculo_radiografico()

                    if "objeto_para_ignorar" in st.session_state:
                        del st.session_state["objeto_para_ignorar"]

                    st.rerun()
        else:
            st.warning("Todos os objetos foram ignorados.")

        objetos_ignorados = [
            resultado_dente["numero_objeto"]
            for resultado_dente in resultados_salvos
            if resultado_dente["ignorado"]
        ]

        if len(objetos_ignorados) > 0:
            st.warning(
                "Objetos ignorados na análise: "
                + ", ".join(
                    str(numero)
                    for numero in objetos_ignorados
                )
            )

    st.markdown("### 4. Cálculo do %PBL")

    if st.button(
        "Calcular %PBL com os keypoints revisados",
        type="primary",
        width="stretch"
    ):
        pbl_maximo, dente_determinante, superficie_determinante = (
            calcular_pbl_dos_dentes(resultados_salvos)
        )

        dados_radiograficos["pbl_calculado"] = True
        dados_radiograficos["pbl_maximo"] = pbl_maximo
        dados_radiograficos["dente_determinante"] = dente_determinante
        dados_radiograficos[
            "superficie_determinante"
        ] = superficie_determinante
        dados_radiograficos["confirmado"] = pbl_maximo is not None

        st.session_state["avaliacao"]["pbl"] = pbl_maximo
        st.session_state["avaliacao"]["periodontal"] = None

        st.rerun()

    if not dados_radiograficos["pbl_calculado"]:
        st.info(
            "Revise os keypoints e clique no botão para calcular o %PBL."
        )
        return

    linhas_resultados = []

    for resultado_dente in resultados_salvos:
        pbl_mesial = resultado_dente["pbl_mesial"]
        pbl_distal = resultado_dente["pbl_distal"]

        linhas_resultados.append(
            {
                "Objeto": resultado_dente["numero_objeto"],
                "Classe radicular": resultado_dente["classe_radicular"],
                "Confiança": (
                    f"{resultado_dente['confianca_deteccao']:.3f}"
                ),
                "%PBL mesial": (
                    f"{pbl_mesial:.2f}%"
                    if pbl_mesial is not None
                    else "Não disponível"
                ),
                "%PBL distal": (
                    f"{pbl_distal:.2f}%"
                    if pbl_distal is not None
                    else "Não disponível"
                ),
                "Situação": (
                    "Ignorado"
                    if resultado_dente["ignorado"]
                    else "Considerado"
                )
            }
        )

    st.dataframe(
        linhas_resultados,
        hide_index=True,
        width="stretch"
    )

    pbl_atual = dados_radiograficos["pbl_maximo"]

    if pbl_atual is None:
        st.warning("Nenhum %PBL válido pôde ser calculado.")
        return

    dente_atual = dados_radiograficos["dente_determinante"]
    superficie_atual = dados_radiograficos["superficie_determinante"]

    st.markdown(
        f"""
        <section class="perio-result">
            <div class="perio-result__eyebrow">
                Resultado radiográfico final
            </div>
            <div class="perio-result__title">
                Maior perda óssea radiográfica considerada
            </div>
            <div class="perio-result__grid">
                <div class="perio-result-card">
                    <div class="perio-result-card__label">
                        Maior %PBL
                    </div>
                    <div class="perio-result-card__value">
                        {pbl_atual:.2f}%
                    </div>
                </div>
                <div class="perio-result-card">
                    <div class="perio-result-card__label">
                        Objeto determinante
                    </div>
                    <div class="perio-result-card__value">
                        {dente_atual}
                    </div>
                </div>
                <div class="perio-result-card">
                    <div class="perio-result-card__label">
                        Superfície determinante
                    </div>
                    <div class="perio-result-card__value">
                        {superficie_atual}
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )

    st.success(
        f"%PBL de {pbl_atual:.2f}% disponível no módulo periodontal."
    )
