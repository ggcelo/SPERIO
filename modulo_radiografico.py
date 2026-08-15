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

REFERENCIAS_RADICULARES = {
    0: ["RL-c"],
    1: ["RL-m", "RL-d"],
    2: ["RL-m", "RL-d", "RL-c"]
}


def calcular_eixo_dentario(pontos, classe_id): #FUNÇÃO PRA ACHAR O EIXO DO DENTE P/CALCULOS

    cej_m = pontos["CEJ-m"]
    cej_d = pontos["CEJ-d"]


    # Para criar o eixo, precisamos das duas CEJs
    if cej_m is None or cej_d is None:
        return None


    # Calcula o ponto médio entre CEJ-m e CEJ-d
    centro_cervical = (
        (cej_m[0] + cej_d[0]) / 2,
        (cej_m[1] + cej_d[1]) / 2
    )


    # Dente unirradicular
    if classe_id == 0:

        referencia_apical = pontos["RL-c"]

        fonte_referencia = "RL-c"


    # Dente birradicular
    elif classe_id == 1:

        rl_m = pontos["RL-m"]
        rl_d = pontos["RL-d"]


        if rl_m is None or rl_d is None:
            return None


        referencia_apical = (
            (rl_m[0] + rl_d[0]) / 2,
            (rl_m[1] + rl_d[1]) / 2
        )

        fonte_referencia = "média de RL-m e RL-d"


    # Dente trirradicular
    elif classe_id == 2:

        referencia_apical = pontos["RL-c"]

        fonte_referencia = "RL-c"


    else:

        return None


    if referencia_apical is None:
        return None


    # Diferença entre a referência apical
    # e o centro cervical
    delta_x = (
        referencia_apical[0]
        - centro_cervical[0]
    )

    delta_y = (
        referencia_apical[1]
        - centro_cervical[1]
    )


    # Comprimento do vetor
    comprimento = hypot(
        delta_x,
        delta_y
    )


    if comprimento == 0:
        return None


    # Transforma o vetor em um vetor de comprimento 1
    versor_x = delta_x / comprimento

    versor_y = delta_y / comprimento


    return {
        "centro_cervical": centro_cervical,
        "referencia_apical": referencia_apical,
        "versor_x": versor_x,
        "versor_y": versor_y,
        "comprimento": comprimento,
        "fonte_referencia_apical": fonte_referencia
    }


def projetar_no_eixo(ponto, eixo):

    if ponto is None:
        return None


    centro_x, centro_y = eixo["centro_cervical"]

    ponto_x, ponto_y = ponto


    # Deslocamento entre o centro cervical
    # e o ponto que queremos projetar
    delta_x = ponto_x - centro_x

    delta_y = ponto_y - centro_y


    # Descobre quanto desse deslocamento
    # acontece na direção do eixo do dente
    posicao_no_eixo = (
        delta_x * eixo["versor_x"]
        + delta_y * eixo["versor_y"]
    )


    return posicao_no_eixo

def calcular_distancia_projetada(posicao_origem, posicao_destino):

    if (
        posicao_origem is None
        or posicao_destino is None
    ):
        return None


    distancia = (
        posicao_destino
        - posicao_origem
    )


    return distancia

def calcular_pbl(distancia_cej_bl, distancia_cej_rl):

    if (
        distancia_cej_bl is None
        or distancia_cej_rl is None
    ):
        return None


    if distancia_cej_rl <= 0:
        return None


    if distancia_cej_bl < 0:
        return None


    percentual_pbl = (
        distancia_cej_bl
        / distancia_cej_rl
    ) * 100


    return percentual_pbl

#CARREGA O MODELO E O SALVA NO CACHE DO STREAMLIT (doc recomenda)
@st.cache_resource
def carregar_modelo_radiografico(caminho):

    modelo = YOLO(
        caminho,
        task="pose"
    )

    return modelo


def mostrar_modulo_radiografico():
    st.header("Análise radiográfica experimental")

    st.write(
        "Carregue uma radiografia periapical, execute o modelo perio-KPT e "
        "revise os resultados antes de continuar para a classificação "
        "periodontal."
    )

    st.warning(
        "Uso experimental. Os valores de %PBL exigem revisão profissional "
        "e devem ser interpretados em conjunto com os dados clínicos."
    )

    modelo_radiografico = None

    # Verifica se o arquivo do modelo existe
    if not caminho_modelo.exists():

        st.error(
            "Modelo radiográfico não encontrado."
        )

        st.write(
            "Caminho esperado:",
            str(caminho_modelo)
        )


    st.markdown("### 1. Seleção da radiografia")
    st.caption("Formatos aceitos: PNG, JPG ou JPEG.")

    imagem_bytes_salva = st.session_state["dados_radiograficos"][
        "imagem_bytes"
    ]

    nome_arquivo_salvo = st.session_state["dados_radiograficos"][
        "nome_arquivo"
    ]

    rotulo_uploader = "Radiografia periapical:"

    if imagem_bytes_salva is not None:
        rotulo_uploader = "Carregar outra radiografia:"

    imagem_radiografica = st.file_uploader(
        rotulo_uploader,
        type=["png", "jpg", "jpeg"]
    )

    nova_imagem_enviada = imagem_radiografica is not None

    # Se não foi enviada uma nova imagem,
    # usamos a radiografia que já está salva no caso
    if imagem_radiografica is None and imagem_bytes_salva is not None:
        imagem_radiografica = BytesIO(imagem_bytes_salva)
        imagem_radiografica.name = nome_arquivo_salvo

    if (
        imagem_radiografica is None
        and imagem_bytes_salva is None
    ):
        st.info("Análise radiográfica não realizada.")


    if imagem_radiografica is not None:

        nome_novo_arquivo = imagem_radiografica.name

        nome_arquivo_anterior = (
            st.session_state["dados_radiograficos"]["nome_arquivo"]
        )


        # Se foi enviada uma imagem diferente,
        # limpamos resultados da imagem anterior
        if (
            nova_imagem_enviada
            and nome_novo_arquivo != nome_arquivo_anterior
        ):

            st.session_state["dados_radiograficos"][
                "resultados_dentes"
            ] = []

            st.session_state["dados_radiograficos"][
                "pbl_maximo"
            ] = None

            st.session_state["dados_radiograficos"][
                "dente_determinante"
            ] = None

            st.session_state["dados_radiograficos"][
                "superficie_determinante"
            ] = None

            st.session_state["dados_radiograficos"][
                "confirmado"
            ] = False

            st.session_state["dados_radiograficos"][
                "imagem_anotada_bytes"
            ] = None

            st.session_state["avaliacao"]["pbl"] = None

            # Como o %PBL mudou, a classificação periodontal
            # anterior pode não ser mais válida
            st.session_state["avaliacao"]["periodontal"] = None

        if nova_imagem_enviada:
            # Guarda o nome do arquivo
            st.session_state["dados_radiograficos"][
                "nome_arquivo"
            ] = nome_novo_arquivo


            # Guarda o conteúdo da imagem
            st.session_state["dados_radiograficos"][
                "imagem_bytes"
            ] = imagem_radiografica.getvalue()


        # Mostra a imagem
        st.markdown("### 2. Visualização")

        imagem_anotada_atual = st.session_state["dados_radiograficos"][
            "imagem_anotada_bytes"
        ]

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
                # Mostra a radiografia anotada salva
                st.image(
                    imagem_anotada_atual,
                    caption="Detecções e keypoints do modelo",
                    width="stretch"
                )

        st.caption(
            "Arquivo em sessão: "
            + st.session_state["dados_radiograficos"]["nome_arquivo"]
        )

        if caminho_modelo.exists():

            try: #caso ache o caminho onde está, tente carregar o modelo

                modelo_radiografico = carregar_modelo_radiografico( #modelo_radiografico recebe o retorno 'modelo'
                    str(caminho_modelo) #transforma em string pela compatibilidade, nao se pode usar path
                )

                st.caption("Modelo perio-KPT carregado e pronto para análise.")

            except Exception as erro:

                st.error(
                    "O modelo radiográfico não pôde ser carregado."
                )

                st.write(
                    "Erro:",
                    str(erro)
                )

        #TESTA INFERENCIA COM O MODELO
        if (
        st.session_state["dados_radiograficos"]["imagem_bytes"] is not None
        and modelo_radiografico is not None
        ):

            if st.button(
                "Analisar radiografia",
                type="primary",
                width="stretch"
            ):

                try:

                    imagem_bytes = (
                        st.session_state["dados_radiograficos"][
                            "imagem_bytes"
                        ]
                    )


                    imagem_para_modelo = Image.open(
                        BytesIO(imagem_bytes)
                    ).convert("RGB")

                    #DESATIVA TEMPORARIARMENTE UMA OTIMIZAÇÃO DE USO DA CPU DO PYTORCH, SALVANDO O ESTADO ANTIGO
                    estado_mkldnn = torch.backends.mkldnn.enabled 

                    # Desativa temporariamente o MKLDNN para manter
                    # compatibilidade com a execução do modelo radiográfico
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

                    finally: #DEVOLVE O ESTADO ANTIGO

                        torch.backends.mkldnn.enabled = estado_mkldnn


                    resultado = resultados[0]

                    imagem_anotada = imagem_para_modelo.copy()

                    desenho = ImageDraw.Draw(
                        imagem_anotada
                    )


                    if resultado.keypoints is None:

                        st.warning(
                            "O modelo retornou objetos sem keypoints."
                        )

                    else:

                        todos_keypoints = (
                            resultado.keypoints.data #pega os dados dos keypoints do pytorch [x,y, confiança]
                            .cpu() #garante que eles serão pegos da cpu
                            .tolist() #os transforma para uma lista em python
                        )

                        todas_caixas = (
                            resultado.boxes.data
                            .cpu()
                            .tolist()
                        )

                        resultados_dentes_analise = []

                        for numero_objeto, (caixa_objeto, keypoints_objeto) in enumerate(
                            zip(todas_caixas, todos_keypoints),
                            start=1
                        ):

                            confianca_deteccao = caixa_objeto[4]

                            classe_id = int(caixa_objeto[5])

                            if classe_id not in [0, 1, 2]:
                                continue

                            #PEGA OS PONTOS PARA DESNEHAR A CAIXA EM VOLTA DO DENTE
                            x1 = caixa_objeto[0]
                            y1 = caixa_objeto[1]
                            x2 = caixa_objeto[2]
                            y2 = caixa_objeto[3]

                            desenho.rectangle(
                                [
                                    (x1, y1),
                                    (x2, y2)
                                ],
                                outline="yellow",
                                width=3
                            )

                            desenho.text(
                                (x1, y1 - 15),
                                f"Objeto {numero_objeto}",
                                fill="yellow"
                            )

                            classe_radicular = CLASSES_PERIO_KPT.get( #usa o .get para ter um valor padrão ao encontrar um classe id que nao corresponda a nenhum listado
                            classe_id,
                            "Classe desconhecida"
                            )

                            if len(keypoints_objeto) != len(NOMES_KEYPOINTS): #verifica se o numero de keypoints do objeto é igual ao numero de nomes de keypoints, se não for, mostra um aviso e continua para o proximo objeto

                                st.warning(
                                    "Este objeto não possui exatamente 11 keypoints."
                                )

                                continue


                            pontos_objeto = {}

                            for nome, ponto in zip( #atrela cada nome de keypoint com o ponto correspondente do objeto, para melhor organização
                                NOMES_KEYPOINTS,
                                keypoints_objeto
                            ):

                                x, y, confianca = ponto #passa cada ponto para x, y e confiança

                                if x == 0 and y == 0:

                                    pontos_objeto[nome] = None

                                else:

                                    pontos_objeto[nome] = (x,y)
                                    if nome in KEYPOINTS_DESENHAR:
                                    # Desenha o keypoint na radiografia
                                        raio = 5

                                        desenho.ellipse(
                                            [
                                                (x - raio, y - raio),
                                                (x + raio, y + raio)
                                            ],
                                            fill="red",
                                            outline="white"
                                        )


                                        # Escreve o nome do keypoint
                                        desenho.text(
                                            (x + 6, y - 6),
                                            nome,
                                            fill="white"
                                        )

                            referencias_objeto = REFERENCIAS_RADICULARES.get(
                                classe_id,
                                []
                            )

                            for nome_referencia in referencias_objeto:

                                ponto_referencia = pontos_objeto[
                                    nome_referencia
                                ]

                            eixo_objeto = calcular_eixo_dentario(
                            pontos_objeto,
                            classe_id
                            )


                            if eixo_objeto is None:

                                st.warning(
                                    "Não foi possível construir o eixo dentário "
                                    "deste objeto."
                                )

                                continue


                            nomes_para_projetar = [
                                "CEJ-m",
                                "BL-m",
                                "CEJ-d",
                                "BL-d"
                            ] + referencias_objeto #referencias_objeto recebe quais referencias radiculares 
                                                   #serão usadas de acordo com o classe_id

                            projecoes_objeto = {}


                            for nome_ponto in nomes_para_projetar: #passa por cada nome ja verificando as referencias apicais necessarias
                                                                   #fala que para nome, fazer a projeçao (chamar funçao)

                                ponto = pontos_objeto[nome_ponto] #ponto_objeto é o dicionario que contem
                                                                  #nome e coordenadas do dente (feito com o zip)
                                                                  #estamos preparando 'ponto' para passa-lo como parametro
                                                                  #ponto recebe SÓ a coordenada (x,y)

                                posicao = projetar_no_eixo(
                                    ponto,      
                                    eixo_objeto #eixo_objeto é justamente o retorno da função que calcula o eixo 
                                )               #contem o dicionario com coordenadas do centro, versores etc

                                projecoes_objeto[nome_ponto] = posicao #recebe o retorno da função, que sera
                                                                #um dicionário contendo nome do ponto + disntancia projetada


                            #AGORA SIM VAMOS CALCULAR AS DISTANCIAS, DE ACORDO COM SUAS PROJEÇÕES NO EIXO
                            distancia_cej_bl_mesial = calcular_distancia_projetada(
                                projecoes_objeto["CEJ-m"],
                                projecoes_objeto["BL-m"]
                            )
                            distancia_cej_bl_distal = calcular_distancia_projetada(
                                projecoes_objeto["CEJ-d"],
                                projecoes_objeto["BL-d"]
                            )

                            # ESCOLHE A REFERÊNCIA RADICULAR DE CADA SUPERFÍCIE

                            if classe_id == 0:

                                # Unirradicular:
                                # as duas superfícies usam a única referência radicular
                                referencia_mesial = "RL-c"
                                referencia_distal = "RL-c"


                            elif classe_id == 1:

                                # Birradicular:
                                # cada superfície usa sua referência correspondente
                                referencia_mesial = "RL-m"
                                referencia_distal = "RL-d"


                            elif classe_id == 2:

                                # Trirradicular:
                                # mesial usa RL-m e distal usa RL-d
                                referencia_mesial = "RL-m"
                                referencia_distal = "RL-d"


                            else:

                                referencia_mesial = None
                                referencia_distal = None

                            if (
                                referencia_mesial is None
                                or referencia_distal is None
                            ):

                                st.warning(
                                    "Não foi possível determinar as referências radiculares."
                                )

                                continue

                            distancia_cej_rl_mesial = calcular_distancia_projetada(
                                projecoes_objeto["CEJ-m"],
                                projecoes_objeto[referencia_mesial]
                            )


                            distancia_cej_rl_distal = calcular_distancia_projetada(
                                projecoes_objeto["CEJ-d"],
                                projecoes_objeto[referencia_distal]
                            )


                            # -------------------------
                            # CÁLCULO DO %PBL
                            # -------------------------

                            pbl_mesial = calcular_pbl(
                                distancia_cej_bl_mesial,
                                distancia_cej_rl_mesial
                            )


                            pbl_distal = calcular_pbl(
                                distancia_cej_bl_distal,
                                distancia_cej_rl_distal
                            )


                            resultado_dente = {
                                "numero_objeto": numero_objeto,
                                "classe_id": classe_id,
                                "classe_radicular": classe_radicular,
                                "confianca_deteccao": confianca_deteccao,
                                "referencia_mesial": referencia_mesial,
                                "referencia_distal": referencia_distal,
                                "pbl_mesial": pbl_mesial,
                                "pbl_distal": pbl_distal,
                                "ignorado": False
                            }

                            resultados_dentes_analise.append(resultado_dente)

                        buffer_imagem_anotada = BytesIO()

                        imagem_anotada.save(
                            buffer_imagem_anotada,
                            format="PNG"
                        )

                        st.session_state["dados_radiograficos"][
                            "imagem_anotada_bytes"
                        ] = buffer_imagem_anotada.getvalue()

                        st.session_state["dados_radiograficos"][ #Fora do for, ou seja, primeiro acaba todos os dentes e depois salva no session_state
                            "resultados_dentes"
                        ] = resultados_dentes_analise

                        # -------------------------
                        # PROCURA O MAIOR %PBL DA RADIOGRAFIA
                        # -------------------------

                        pbl_maximo_analise = None

                        dente_determinante_analise = None

                        superficie_determinante_analise = None


                        for resultado_dente in resultados_dentes_analise:

                            # -------------------------
                            # SUPERFÍCIE MESIAL
                            # -------------------------

                            pbl_mesial_dente = resultado_dente[
                                "pbl_mesial"
                            ]


                            if pbl_mesial_dente is not None:

                                if (
                                    pbl_maximo_analise is None
                                    or pbl_mesial_dente > pbl_maximo_analise
                                ):

                                    pbl_maximo_analise = pbl_mesial_dente

                                    dente_determinante_analise = resultado_dente[
                                        "numero_objeto"
                                    ]

                                    superficie_determinante_analise = "mesial"


                            # -------------------------
                            # SUPERFÍCIE DISTAL
                            # -------------------------

                            pbl_distal_dente = resultado_dente[
                                "pbl_distal"
                            ]


                            if pbl_distal_dente is not None:

                                if (
                                    pbl_maximo_analise is None
                                    or pbl_distal_dente > pbl_maximo_analise
                                ):

                                    pbl_maximo_analise = pbl_distal_dente

                                    dente_determinante_analise = resultado_dente[
                                        "numero_objeto"
                                    ]


                                    superficie_determinante_analise = "distal"


                        # SALVA O RESULTADO RADIOGRÁFICO
                        # ----------------------------
                        if pbl_maximo_analise is None:

                            st.session_state["dados_radiograficos"][
                                "pbl_maximo"
                            ] = None

                            st.session_state["dados_radiograficos"][
                                "dente_determinante"
                            ] = None

                            st.session_state["dados_radiograficos"][
                                "superficie_determinante"
                            ] = None

                            st.session_state["avaliacao"][
                                "pbl"
                            ] = None

                            st.session_state["avaliacao"][
                                "periodontal"
                            ] = None

                            st.warning(
                                "Nenhum %PBL válido pôde ser calculado."
                            )


                        else:

                            st.session_state["dados_radiograficos"][
                                "pbl_maximo"
                            ] = pbl_maximo_analise

                            st.session_state["dados_radiograficos"][
                                "dente_determinante"
                            ] = dente_determinante_analise

                            st.session_state["dados_radiograficos"][
                                "superficie_determinante"
                            ] = superficie_determinante_analise


                            # Integra o resultado radiográfico
                            # com o restante da aplicação
                            st.session_state["avaliacao"][
                                "pbl"
                            ] = pbl_maximo_analise

                            # O resultado periodontal deve ser recalculado
                            # caso o %PBL tenha sido atualizado
                            st.session_state["avaliacao"][
                                "periodontal"
                            ] = None

                            st.rerun()

                except Exception as erro:

                    st.error(
                        "Não foi possível analisar a radiografia."
                    )

                    st.write(
                        "Erro:",
                        str(erro)
                    )
        # -------------------------
        # EXIBIÇÃO DA ANÁLISE SALVA
        # -------------------------

        resultados_salvos = (
            st.session_state["dados_radiograficos"][
                "resultados_dentes"
            ]
        )

        imagem_anotada_bytes = (
            st.session_state["dados_radiograficos"][
                "imagem_anotada_bytes"
            ]
        )


        # -------------------------
        # RESUMO DOS DENTES ANALISADOS
        # -------------------------

        if len(resultados_salvos) > 0:
            st.markdown("### 3. Resultados por dente")
            st.caption(
                "A numeração representa a ordem visual dos objetos detectados "
                "e não corresponde à numeração odontológica FDI."
            )

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



        # -------------------------
        # IGNORAR OBJETO DA ANÁLISE
        # -------------------------

        resultados_salvos = (
            st.session_state["dados_radiograficos"][
                "resultados_dentes"
            ]
        )


        if len(resultados_salvos) > 0:

            st.markdown("### 4. Revisão das detecções")

            st.write(
                "Se algum objeto detectado estiver visualmente "
                "muito incorreto, ele pode ser ignorado no cálculo final."
            )


            objetos_disponiveis = []

            for resultado_dente in resultados_salvos:

                if resultado_dente["ignorado"] == False:

                    objetos_disponiveis.append(
                        resultado_dente["numero_objeto"]
                    )


            if len(objetos_disponiveis) > 0:

                objeto_para_ignorar = st.selectbox(
                    "Objeto a ignorar:",
                    objetos_disponiveis,
                    index=None,
                    placeholder="Selecione um objeto"
                )


                if st.button(
                    "Ignorar objeto selecionado",
                    width="stretch"
                ):

                    if objeto_para_ignorar is None:

                        st.warning(
                            "Selecione primeiro um objeto."
                        )

                    else:

                        for resultado_dente in resultados_salvos:

                            if (
                                resultado_dente["numero_objeto"]
                                == objeto_para_ignorar
                            ):

                                resultado_dente[
                                    "ignorado"
                                ] = True


                        # -------------------------
                        # RECALCULA O MAIOR %PBL
                        # SEM OS OBJETOS IGNORADOS
                        # -------------------------

                        pbl_maximo_novo = None

                        dente_determinante_novo = None

                        superficie_determinante_nova = None


                        for resultado_dente in resultados_salvos:

                            # Se o objeto foi ignorado,
                            # não participa da análise
                            if resultado_dente["ignorado"]:

                                continue


                            pbl_mesial = resultado_dente[
                                "pbl_mesial"
                            ]

                            pbl_distal = resultado_dente[
                                "pbl_distal"
                            ]

                            numero_objeto = resultado_dente[
                                "numero_objeto"
                            ]


                            # Verifica a superfície mesial
                            if pbl_mesial is not None:

                                if (
                                    pbl_maximo_novo is None
                                    or pbl_mesial > pbl_maximo_novo
                                ):

                                    pbl_maximo_novo = pbl_mesial

                                    dente_determinante_novo = (
                                        numero_objeto
                                    )

                                    superficie_determinante_nova = (
                                        "mesial"
                                    )


                            # Verifica a superfície distal
                            if pbl_distal is not None:

                                if (
                                    pbl_maximo_novo is None
                                    or pbl_distal > pbl_maximo_novo
                                ):

                                    pbl_maximo_novo = pbl_distal

                                    dente_determinante_novo = (
                                        numero_objeto
                                    )

                                    superficie_determinante_nova = (
                                        "distal"
                                    )
                        st.session_state["dados_radiograficos"][
                            "pbl_maximo"
                        ] = pbl_maximo_novo

                        st.session_state["dados_radiograficos"][
                            "dente_determinante"
                        ] = dente_determinante_novo

                        st.session_state["dados_radiograficos"][
                            "superficie_determinante"
                        ] = superficie_determinante_nova


                        st.session_state["avaliacao"][
                            "pbl"
                        ] = pbl_maximo_novo

                        # Como o %PBL foi recalculado,
                        # a classificação periodontal anterior é invalidada
                        st.session_state["avaliacao"][
                            "periodontal"
                        ] = None

                        st.rerun()

             # -------------------------
            # OBJETOS IGNORADOS
            # -------------------------

            objetos_ignorados = []

            for resultado_dente in resultados_salvos:

                if resultado_dente["ignorado"]:

                    objetos_ignorados.append(
                        resultado_dente["numero_objeto"]
                    )


            if len(objetos_ignorados) > 0:

                st.warning(
                    "Objetos ignorados na análise: "
                    + ", ".join(
                        str(numero)
                        for numero in objetos_ignorados
                    )
                )
            # -------------------------
            # RESULTADO RADIOGRÁFICO ATUAL
            # -------------------------

            pbl_atual = (
                st.session_state["dados_radiograficos"][
                    "pbl_maximo"
                ]
            )

            dente_atual = (
                st.session_state["dados_radiograficos"][
                    "dente_determinante"
                ]
            )

            superficie_atual = (
                st.session_state["dados_radiograficos"][
                    "superficie_determinante"
                ]
            )


            if pbl_atual is None:

                st.warning(
                    "Nenhum %PBL válido está disponível."
                )

            else:
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
                    f"%PBL de {pbl_atual:.2f}% disponível no módulo "
                    "periodontal."
                )

