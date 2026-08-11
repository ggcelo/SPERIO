import torch

import streamlit as st
from html import escape
from datetime import datetime
from pathlib import Path
from io import BytesIO
from math import hypot
from PIL import Image, ImageDraw
from ultralytics import YOLO

pasta_projeto = Path(__file__).parent

caminho_modelo = (
    pasta_projeto
    / "models"
    / "perio_kpt_7kpt_fold0_best.pt"
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
    "RL-c"
]

CLASSES_RADICULARES = {
    0: "Dente unirradicular",
    1: "Dente birradicular",
    2: "Dente trirradicular"
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

st.set_page_config(
    page_title="Apoio à Decisão em Periodontia",
    page_icon="🦷",
    layout="wide"
)

#CARREGA O MODELO E O SALVA NO CACHE DO STREAMLIT (doc recomenda)
@st.cache_resource
def carregar_modelo_radiografico(caminho):

    modelo = YOLO(
        caminho,
        task="pose"
    )

    return modelo

st.title("Aplicação de Apoio à Decisão Clínica em Periodontia")

st.write(
    "Sistema para classificação periodontal e integração "
    "de ferramentas de rastreamento de risco."
)

st.divider()


modulo = st.selectbox(
    "Escolha um módulo:",
    [
        "Classificação periodontal",
        "FINDRISC",
        "INTERHEART",
        "Análise radiográfica"
    ]
)

st.write("Módulo selecionado:", modulo)

#DICIONÁRIO DOS RESULTADOS

if "avaliacao" not in st.session_state: 
    st.session_state["avaliacao"] = {
        "periodontal": None,
        "findrisc": None,
        "interheart": None,
        "pbl": None
    }

# DICIONÁRIO DO MÓDULO RADIOGRÁFICO
if "dados_radiograficos" not in st.session_state:
    st.session_state["dados_radiograficos"] = {
        "nome_arquivo": None,
        "imagem_bytes": None,
        "resultados_dentes": [],
        "pbl_maximo": None,
        "dente_determinante": None,
        "superficie_determinante": None,
        "confirmado": False,
        "imagem_anotada_bytes": None
    }
st.write(st.session_state["dados_radiograficos"])

# MÓDULO RADIOGRÁFICO

if modulo == "Análise radiográfica":

    st.header("Análise radiográfica")

    st.write(
        "Envie uma radiografia periapical para análise."
    )

    modelo_radiografico = None

    # Verifica se o arquivo do modelo existe
    if caminho_modelo.exists():

        st.success(
            "Modelo radiográfico encontrado."
        )

        try: #caso ache o caminho onde está, tente carregar o modelo

            modelo_radiografico = carregar_modelo_radiografico( #modelo_radiografico recebe o retorno 'modelo'
                str(caminho_modelo) #transforma em string pela compatibilidade, nao se pode usar path
            )

            st.success(
                "Modelo radiográfico carregado com sucesso."
            )

        except Exception as erro:

            st.error(
                "O modelo radiográfico não pôde ser carregado."
            )

            st.write(
                "Erro:",
                str(erro)
            )

    else:

        st.error(
            "Modelo radiográfico não encontrado."
        )

        st.write(
            "Caminho esperado:",
            str(caminho_modelo)
        )


    imagem_radiografica = st.file_uploader(
        "Selecione a radiografia:",
        type=["png", "jpg", "jpeg"]
    )


    if imagem_radiografica is not None:

        nome_novo_arquivo = imagem_radiografica.name

        nome_arquivo_anterior = (
            st.session_state["dados_radiograficos"]["nome_arquivo"]
        )


        # Se foi enviada uma imagem diferente,
        # limpamos resultados da imagem anterior
        if nome_novo_arquivo != nome_arquivo_anterior:

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

        # Guarda o nome do arquivo
        st.session_state["dados_radiograficos"][
            "nome_arquivo"
        ] = nome_novo_arquivo


        # Guarda o conteúdo da imagem
        st.session_state["dados_radiograficos"][
            "imagem_bytes"
        ] = imagem_radiografica.getvalue()


        # Mostra a imagem
        st.image(
            imagem_radiografica,
            caption="Radiografia selecionada"
        )


        st.success(
            "Radiografia carregada e armazenada com sucesso."
        )


        st.write(
            "Arquivo armazenado:",
            st.session_state["dados_radiograficos"]["nome_arquivo"]
        )

        #TESTA INFERENCIA COM O MODELO
        if (
        st.session_state["dados_radiograficos"]["imagem_bytes"] is not None
        and modelo_radiografico is not None
        ):

            if st.button("Analisar radiografia"):

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


                    st.success(
                        "Inferência radiográfica executada com sucesso."
                    )


                    st.write(
                        "Objetos detectados pelo modelo:",
                        len(resultado.boxes)
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

                            classe_radicular = CLASSES_RADICULARES.get( #usa o .get para ter um valor padrão ao encontrar um classe id que nao corresponda a nenhum listado
                            classe_id,
                            "Classe desconhecida"
                            )
                            
                            st.write(
                                f"Objeto {numero_objeto}"
                            )

                            st.write(
                                "Classe radicular:",
                                classe_radicular
                            )

                            st.write(
                                "Confiança da detecção:",
                                f"{confianca_deteccao:.3f}"
                            )

                            if len(keypoints_objeto) != len(NOMES_KEYPOINTS): #verifica se o numero de keypoints do objeto é igual ao numero de nomes de keypoints, se não for, mostra um aviso e continua para o proximo objeto

                                st.warning(
                                    "Este objeto não possui exatamente 7 keypoints."
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
                                    st.write(f"{nome}: não detectado")
                                                          
                                else:

                                    pontos_objeto[nome] = (x,y)
                                        
                                   # Desenha o keypoint na radiografia
                                    raio = 4

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

                                    st.write(       #escreve cada ponto com suas informações, no loop for
                                        f"{nome}: "
                                        f"x = {x:.1f}, "
                                        f"y = {y:.1f}, "
                                        f"confiança = {confianca:.3f}"
                                    )


                            st.write(
                                "Pontos organizados:",
                                pontos_objeto
                            )

                            referencias_objeto = REFERENCIAS_RADICULARES.get(
                                classe_id,
                                []
                            )
                            
                            st.write(
                                "Referências radiculares utilizadas:",
                                referencias_objeto
                            )

                            for nome_referencia in referencias_objeto:

                                ponto_referencia = pontos_objeto[
                                    nome_referencia
                                ]

                                st.write(
                                    nome_referencia,
                                    "→",
                                    ponto_referencia
                                )

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


                            st.write(
                                "Centro cervical:",
                                eixo_objeto["centro_cervical"]
                            )


                            st.write(
                                "Referência apical do eixo:",
                                eixo_objeto["referencia_apical"]
                            )


                            st.write(
                                "Fonte da referência apical:",
                                eixo_objeto["fonte_referencia_apical"]
                            )


                            st.write(
                                "Direção do eixo:",
                                (
                                    eixo_objeto["versor_x"],
                                    eixo_objeto["versor_y"]
                                )
                            )


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


                                if posicao is None:

                                    st.write(
                                        nome_ponto,
                                        "→ projeção não disponível"
                                    )

                                else:

                                    st.write(
                                        nome_ponto,
                                        "→ posição no eixo:",
                                        f"{posicao:.2f}"
                                    )


                            #AGORA SIM VAMOS CALCULAR AS DISTANCIAS, DE ACORDO COM SUAS PROJEÇÕES NO EIXO
                            distancia_cej_bl_mesial = calcular_distancia_projetada(
                                projecoes_objeto["CEJ-m"],
                                projecoes_objeto["BL-m"]
                            )
                            distancia_cej_bl_distal = calcular_distancia_projetada(
                                projecoes_objeto["CEJ-d"],
                                projecoes_objeto["BL-d"]
                            )

                            if distancia_cej_bl_mesial is None:

                                st.write(
                                    "Distância CEJ → BL mesial: não disponível"
                                )

                            else:

                                st.write(
                                    "Distância projetada CEJ → BL mesial:",
                                    f"{distancia_cej_bl_mesial:.2f}"
                                )


                            if distancia_cej_bl_distal is None:

                                st.write(
                                    "Distância CEJ → BL distal: não disponível"
                                )

                            else:

                                st.write(
                                    "Distância projetada CEJ → BL distal:",
                                    f"{distancia_cej_bl_distal:.2f}"
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


                            st.write(
                                "Referência radicular mesial:",
                                referencia_mesial
                            )

                            st.write(
                                "Distância projetada CEJ → referência mesial:",
                                distancia_cej_rl_mesial
                            )


                            st.write(
                                "Referência radicular distal:",
                                referencia_distal
                            )

                            st.write(
                                "Distância projetada CEJ → referência distal:",
                                distancia_cej_rl_distal
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


                            if pbl_mesial is None:

                                st.write(
                                    "%PBL mesial: não disponível"
                                )

                            else:

                                st.write(
                                    "%PBL mesial:",
                                    f"{pbl_mesial:.2f}%"
                                )


                            if pbl_distal is None:

                                st.write(
                                    "%PBL distal: não disponível"
                                )

                            else:

                                st.write(
                                    "%PBL distal:",
                                    f"{pbl_distal:.2f}%"
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

                        st.write(
                            "Resultados dos dentes:", #mostra o resultado da lista dos dados adquiridos no modulo radiografico
                            st.session_state[         #cada item da lista contem um dicionario com resultado_dente 
                                "dados_radiograficos"
                            ]["resultados_dentes"]
                        )

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


                            st.success(
                                "Resultado radiográfico armazenado com sucesso."
                            )


                            st.write(
                                "Maior %PBL:",
                                f"{pbl_maximo_analise:.2f}%"
                            )

                            st.write(
                                "Objeto determinante:",
                                dente_determinante_analise
                            )

                            st.write(
                                "Superfície determinante:",
                                superficie_determinante_analise
                            )

                            

                            st.divider()

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


        # Mostra a radiografia anotada salva
        if imagem_anotada_bytes is not None:

            st.subheader(
                "Radiografia com detecções"
            )

            st.image(
                imagem_anotada_bytes,
                caption="Caixas e keypoints detectados pelo modelo"
            )


        # -------------------------
        # RESUMO DOS DENTES ANALISADOS
        # -------------------------

        if len(resultados_salvos) > 0:

            st.subheader(
                "Resultados por dente"
            )


            for resultado_dente in resultados_salvos:

                numero_objeto = resultado_dente[
                    "numero_objeto"
                ]

                classe_radicular = resultado_dente[
                    "classe_radicular"
                ]

                confianca_deteccao = resultado_dente[
                    "confianca_deteccao"
                ]

                pbl_mesial = resultado_dente[
                    "pbl_mesial"
                ]

                pbl_distal = resultado_dente[
                    "pbl_distal"
                ]


                st.markdown(
                    f"### Objeto {numero_objeto}"
                )

                st.write(
                    "Classe radicular:",
                    classe_radicular
                )

                st.write(
                    "Confiança da detecção:",
                    f"{confianca_deteccao:.3f}"
                )


                if pbl_mesial is None:

                    st.write(
                        "%PBL mesial: não disponível"
                    )

                else:

                    st.write(
                        "%PBL mesial:",
                        f"{pbl_mesial:.2f}%"
                    )


                if pbl_distal is None:

                    st.write(
                        "%PBL distal: não disponível"
                    )

                else:

                    st.write(
                        "%PBL distal:",
                        f"{pbl_distal:.2f}%"
                    )


                st.divider()



        # -------------------------
        # IGNORAR OBJETO DA ANÁLISE
        # -------------------------

        resultados_salvos = (
            st.session_state["dados_radiograficos"][
                "resultados_dentes"
            ]
        )


        if len(resultados_salvos) > 0:

            st.subheader(
                "Revisão das detecções"
            )

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
                    "Ignorar objeto selecionado"
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


                        st.success(
                            f"Objeto {objeto_para_ignorar} "
                            "ignorado na análise."
                        )

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

                        if pbl_maximo_novo is None:

                            st.warning(
                                "Nenhum %PBL válido permaneceu "
                                "após ignorar o objeto."
                            )

                        else:

                            st.write(
                                "Novo maior %PBL:",
                                f"{pbl_maximo_novo:.2f}%"
                            )

                            st.write(
                                "Novo objeto determinante:",
                                dente_determinante_novo
                            )

                            st.write(
                                "Nova superfície determinante:",
                                superficie_determinante_nova
                            )

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


            st.subheader(
                "Resultado radiográfico final"
            )


            if pbl_atual is None:

                st.warning(
                    "Nenhum %PBL válido está disponível."
                )

            else:

                st.write(
                    "Maior %PBL considerado:",
                    f"{pbl_atual:.2f}%"
                )

                st.write(
                    "Objeto determinante:",
                    dente_atual
                )

                st.write(
                    "Superfície determinante:",
                    superficie_atual
                )





st.divider()
st.subheader("Teste de estado da aplicação")


# Se "contador" ainda não existir no estado da sessão,
# ele será criado com valor inicial igual a zero.
if "contador" not in st.session_state:
    st.session_state["contador"] = 0


# Quando o botão é clicado, alteramos diretamente
# o valor armazenado no estado da sessão.
if st.button("Somar 1"):
    st.session_state["contador"] += 1


st.write(
    "Valor do contador:",
    st.session_state["contador"]
)


if st.button("Zerar contador"):
    st.session_state["contador"] = 0
    st.rerun()

st.divider()
st.subheader("Primeiro estado de uma avaliação")

#----------------------------------------------
#dicionario dos resultados 'avaliacao' foi retirado daqui e posto ANTES do Modulo Radiografico
#----------------------------------------------

st.write(st.session_state["avaliacao"])


pbl_digitado = st.number_input(
    "Digite um %PBL de teste:",
    min_value=0.0,
    max_value=100.0,
    step=0.1
)


if st.button("Salvar PBL"):
    st.session_state["avaliacao"]["pbl"] = pbl_digitado
    st.rerun()


st.write(
    "PBL salvo:",
    st.session_state["avaliacao"]["pbl"]
)

st.divider()

if st.button("Apagar %PBL"):
    st.session_state["avaliacao"]["pbl"] = None
    st.rerun()

#DICIONÁRIO DOS DADOS DO CASO

if "dados_caso" not in st.session_state: 
    st.session_state["dados_caso"] = {
        "codigo": None,
        "idade": None,
        "sexo": None
    }


st.subheader("Dados do caso")

with st.form("form_dados_caso"): #tudo dentro do with fica armazenado dentro do formulario

    codigo_digitado = st.text_input(
        "Código do caso:"
    )

    idade_digitada = st.number_input(
        "Idade:",
        min_value=1,
        max_value=120,
        value=None,
        step=1
    )

    sexo_digitado = st.selectbox(
        "Sexo:",
        ["Feminino", "Masculino"],
        index=None,
        placeholder="Selecione"
    )

    salvar_dados = st.form_submit_button(
        "Salvar dados do caso"
    )

#coloca todos os dados do formulario dentro do dados_caso
if salvar_dados:

    if codigo_digitado.strip() == "": #evita a colocar "  "
        st.error("Digite o código do caso.")

    elif idade_digitada is None:
        st.error("Digite a idade.")

    elif sexo_digitado is None:
        st.error("Selecione o sexo.")

    else:
        st.session_state["dados_caso"]["codigo"] = codigo_digitado.strip()
        st.session_state["dados_caso"]["idade"] = idade_digitada
        st.session_state["dados_caso"]["sexo"] = sexo_digitado

        st.success("Dados do caso salvos.")
    st.write(st.session_state["dados_caso"])

st.divider()

st.subheader("Dados clínicos")

#DICIONARIO DOS DADOS CLINICOS COMPARTILHADOS

if "dados_clinicos" not in st.session_state:
    st.session_state["dados_clinicos"] = {
        "peso": None,
        "altura": None,
        "cintura": None,
        "quadril": None,
        "imc": None,
        "diabetes": None,
        "tabagismo": None,
        "cigarros_dia": None
    }

with st.form("form_dados_clinicos"):

    peso_digitado = st.number_input(
        "Peso (kg):",
        min_value=1.0,
        max_value=300.0,
        value=None,
        step=0.1
    )

    altura_digitada = st.number_input(
        "Altura (m):",
        min_value=0.5,
        max_value=2.5,
        value=None,
        step=0.01
    )

    cintura_digitada = st.number_input(
        "Circunferência da cintura (cm):",
        min_value=20.0,
        max_value=250.0,
        value=None,
        step=0.1
    )

    quadril_digitado = st.number_input(
        "Circunferência do quadril (cm):",
        min_value=20.0,
        max_value=250.0,
        value=None,
        step=0.1
    )

    diabetes_digitado = st.selectbox(
        "Possui diabetes diagnosticado?",
        ["Sim", "Não", "Não sabe"],
        index=None,
        placeholder="Selecione"
    )

    tabagismo_digitado = st.selectbox(
        "Situação de tabagismo:",
        [
            "Nunca fumou",
            "Ex-fumante há mais de 12 meses",
            "Fumante atual ou nos últimos 12 meses"
        ],
        index=None,
        placeholder="Selecione"
    )

    cigarros_dia_digitado = st.number_input(
        "Média de cigarros por dia:",
        min_value=0,
        max_value=100,
        value=None,
        step=1
    )

    salvar_clinicos = st.form_submit_button(
        "Salvar dados clínicos"
    )


if salvar_clinicos:

    if peso_digitado is None:
        st.error("Digite o peso.")

    elif altura_digitada is None:
        st.error("Digite a altura.")

    elif cintura_digitada is None:
        st.error("Digite a circunferência da cintura.")

    elif quadril_digitado is None:
        st.error("Digite a circunferência do quadril.")

    elif diabetes_digitado is None:
        st.error("Informe a situação de diabetes.")

    elif tabagismo_digitado is None:
        st.error("Informe a situação de tabagismo.")

    elif (
        tabagismo_digitado == "Fumante atual ou nos últimos 12 meses"
        and cigarros_dia_digitado is None
    ):
        st.error("Informe a média de cigarros por dia.")
    
    else:
        imc = round(
            peso_digitado / (altura_digitada ** 2),
            2
        )

        st.session_state["dados_clinicos"]["peso"] = peso_digitado
        st.session_state["dados_clinicos"]["altura"] = altura_digitada
        st.session_state["dados_clinicos"]["cintura"] = cintura_digitada
        st.session_state["dados_clinicos"]["quadril"] = quadril_digitado
        st.session_state["dados_clinicos"]["imc"] = imc
        st.session_state["dados_clinicos"]["diabetes"] = diabetes_digitado
        st.session_state["dados_clinicos"]["tabagismo"] = tabagismo_digitado
        st.session_state["dados_clinicos"]["cigarros_dia"] = cigarros_dia_digitado

        st.success("Dados clínicos salvos.")


st.write(
    "Dados clínicos salvos:",
    st.session_state["dados_clinicos"]
)

st.divider()

st.subheader("FINDRISC")

#DICIONARIO DOS DADOS ESPECIFICOS DO FINDRISC

if "dados_findrisc" not in st.session_state:
    st.session_state["dados_findrisc"] = {
        "atividade_fisica": None,
        "frutas_vegetais": None,
        "medicacao_pressao": None,
        "glicemia_elevada": None,
        "historico_familiar": None
    }

with st.form("form_findrisc"):

    atividade_fisica = st.selectbox(
        "Realiza pelo menos 30 minutos de atividade física por dia?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    frutas_vegetais = st.selectbox(
        "Consome frutas ou vegetais diariamente?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    medicacao_pressao = st.selectbox(
        "Já utilizou regularmente medicamento para pressão alta?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    glicemia_elevada = st.selectbox(
        "Alguma vez foi identificada glicemia elevada?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    historico_familiar = st.selectbox(
        "Histórico familiar de diabetes:",
        [
            "Nenhum familiar",
            "Avós, tios ou primos",
            "Pais, irmãos ou filhos"
        ],
        index=None,
        placeholder="Selecione"
    )

    salvar_findrisc = st.form_submit_button(
        "Salvar dados do FINDRISC"
    )

if salvar_findrisc:

    if atividade_fisica is None:
        st.error("Informe a atividade física.")

    elif frutas_vegetais is None:
        st.error("Informe o consumo de frutas ou vegetais.")

    elif medicacao_pressao is None:
        st.error("Informe o uso de medicamento para pressão alta.")

    elif glicemia_elevada is None:
        st.error("Informe se já houve glicemia elevada.")

    elif historico_familiar is None:
        st.error("Informe o histórico familiar de diabetes.")

    else:
        st.session_state["dados_findrisc"]["atividade_fisica"] = atividade_fisica
        st.session_state["dados_findrisc"]["frutas_vegetais"] = frutas_vegetais
        st.session_state["dados_findrisc"]["medicacao_pressao"] = medicacao_pressao
        st.session_state["dados_findrisc"]["glicemia_elevada"] = glicemia_elevada
        st.session_state["dados_findrisc"]["historico_familiar"] = historico_familiar

        st.success("Dados do FINDRISC salvos.")

if st.button("Calcular FINDRISC"):

    idade = st.session_state["dados_caso"]["idade"]
    sexo = st.session_state["dados_caso"]["sexo"]

    imc = st.session_state["dados_clinicos"]["imc"]
    cintura = st.session_state["dados_clinicos"]["cintura"]

    dados_findrisc = st.session_state["dados_findrisc"]


    if (
        idade is None
        or sexo is None
        or imc is None
        or cintura is None
        or None in dados_findrisc.values()
    ):
        st.error(
            "Preencha e salve todos os dados necessários "
            "antes de calcular o FINDRISC."
        )

    else:

        pontos = 0


        # Idade
        if idade < 45:
            pontos += 0

        elif idade < 55:
            pontos += 2

        elif idade < 65:
            pontos += 3

        else:
            pontos += 4


        # IMC
        if imc < 25:
            pontos += 0

        elif imc < 30:
            pontos += 1

        else:
            pontos += 3


        # Circunferência da cintura
        if sexo == "Masculino":

            if cintura < 94:
                pontos += 0

            elif cintura <= 102:
                pontos += 3

            else:
                pontos += 4


        elif sexo == "Feminino":

            if cintura < 80:
                pontos += 0

            elif cintura <= 88:
                pontos += 3

            else:
                pontos += 4


        # Atividade física
        if dados_findrisc["atividade_fisica"] == "Não":
            pontos += 2


        # Frutas e vegetais
        if dados_findrisc["frutas_vegetais"] == "Não":
            pontos += 1


        # Medicamento para hipertensão
        if dados_findrisc["medicacao_pressao"] == "Sim":
            pontos += 2


        # Histórico de glicemia elevada
        if dados_findrisc["glicemia_elevada"] == "Sim":
            pontos += 5


        # Histórico familiar
        if dados_findrisc["historico_familiar"] == "Avós, tios ou primos":
            pontos += 3

        elif dados_findrisc["historico_familiar"] == "Pais, irmãos ou filhos":
            pontos += 5

        if pontos < 7:
            classificacao = "Baixo"
            estimativa = "Aproximadamente 1 em 100"

        elif pontos < 12:
            classificacao = "Levemente moderado"
            estimativa = "Aproximadamente 1 em 25"

        elif pontos < 15:
            classificacao = "Moderado"
            estimativa = "Aproximadamente 1 em 6"

        elif pontos < 21:
            classificacao = "Alto"
            estimativa = "Aproximadamente 1 em 3"

        else:
            classificacao = "Muito alto"
            estimativa = "Aproximadamente 1 em 2"

         # Salva o resultado da avaliação
        st.session_state["avaliacao"]["findrisc"] = {
            "pontos": pontos,
            "classificacao": classificacao,
            "estimativa": estimativa
        }

        st.success("FINDRISC calculado com sucesso.")

resultado_findrisc = st.session_state["avaliacao"]["findrisc"]


if resultado_findrisc is not None:

    st.subheader("Resultado FINDRISC")

    st.write(
        "Pontuação:",
        resultado_findrisc["pontos"]
    )

    st.write(
        "Classificação:",
        resultado_findrisc["classificacao"]
    )

    st.write(
        "Risco estimado em 10 anos:",
        resultado_findrisc["estimativa"]
    )

st.divider()

st.subheader("INTERHEART")

#DICIONARIO DOS DADOS ESPECIFICOS DO INTERHEART

if "dados_interheart" not in st.session_state:
    st.session_state["dados_interheart"] = {
        "hipertensao": None,
        "historico_parental_infarto": None,
        "estresse": None,
        "fumo_passivo": None,
        "atividade_lazer": None,
        "tristeza_depressao": None,
        "alimento_salgado": None,
        "fritura_fast_food": None,
        "fruta_diaria": None,
        "vegetais_diarios": None,
        "carne_aves": None
    }

with st.form("form_interheart"):

    hipertensao = st.selectbox(
        "Possui hipertensão/pressão alta diagnosticada?",
        ["Sim", "Não", "Não sabe"],
        index=None,
        placeholder="Selecione"
    )

    historico_parental_infarto = st.selectbox(
        "Pai ou mãe possui histórico de infarto?",
        ["Sim", "Não", "Não sabe"],
        index=None,
        placeholder="Selecione"
    )

    estresse = st.selectbox(
        "Estresse no trabalho ou em casa:",
        [
            "Nunca ou em alguns períodos",
            "Vários períodos ou permanente"
        ],
        index=None,
        placeholder="Selecione"
    )

    fumo_passivo = st.selectbox(
        "Exposição ao fumo passivo por uma hora ou mais por semana?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    atividade_lazer = st.selectbox(
        "Atividade física no lazer:",
        [
            "Moderada ou intensa",
            "Sedentário ou esforço mínimo"
        ],
        index=None,
        placeholder="Selecione"
    )

    tristeza_depressao = st.selectbox(
        "Tristeza ou depressão por duas semanas ou mais?",
        ["Sim", "Não"],
         index=None,
        placeholder="Selecione"
    )

    alimento_salgado = st.selectbox(
        "Consome alimentos salgados uma ou mais vezes ao dia?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    fritura_fast_food = st.selectbox(
        "Consome fritura ou fast-food três ou mais vezes por semana?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    fruta_diaria = st.selectbox(
        "Consome frutas diariamente?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    vegetais_diarios = st.selectbox(
        "Consome vegetais diariamente?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    carne_aves = st.selectbox(
        "Consome carne ou aves duas ou mais vezes ao dia?",
        ["Sim", "Não"],
        index=None,
        placeholder="Selecione"
    )

    salvar_interheart = st.form_submit_button(
        "Salvar dados do INTERHEART"
    )

if salvar_interheart:

    if hipertensao is None:
        st.error("Informe a situação de hipertensão.")

    elif historico_parental_infarto is None:
        st.error("Informe o histórico parental de infarto.")

    elif estresse is None:
        st.error("Informe a situação de estresse.")

    elif fumo_passivo is None:
        st.error("Informe a exposição ao fumo passivo.")

    elif atividade_lazer is None:
        st.error("Informe a atividade física no lazer.")

    elif tristeza_depressao is None:
        st.error("Informe a situação de tristeza ou depressão.")

    elif alimento_salgado is None:
        st.error("Informe o consumo de alimentos salgados.")

    elif fritura_fast_food is None:
        st.error("Informe o consumo de fritura ou fast-food.")

    elif fruta_diaria is None:
        st.error("Informe o consumo diário de frutas.")

    elif vegetais_diarios is None:
        st.error("Informe o consumo diário de vegetais.")

    elif carne_aves is None:
        st.error("Informe o consumo de carne ou aves.")

    else:
        st.session_state["dados_interheart"]["hipertensao"] = hipertensao

        st.session_state["dados_interheart"]["historico_parental_infarto"] = (
            historico_parental_infarto
        )

        st.session_state["dados_interheart"]["estresse"] = estresse

        st.session_state["dados_interheart"]["fumo_passivo"] = fumo_passivo

        st.session_state["dados_interheart"]["atividade_lazer"] = (
            atividade_lazer
        )

        st.session_state["dados_interheart"]["tristeza_depressao"] = (
            tristeza_depressao
        )

        st.session_state["dados_interheart"]["alimento_salgado"] = (
            alimento_salgado
        )

        st.session_state["dados_interheart"]["fritura_fast_food"] = (
            fritura_fast_food
        )

        st.session_state["dados_interheart"]["fruta_diaria"] = fruta_diaria

        st.session_state["dados_interheart"]["vegetais_diarios"] = (
            vegetais_diarios
        )

        st.session_state["dados_interheart"]["carne_aves"] = carne_aves

        st.success("Dados do INTERHEART salvos.")

    st.write(
    "Dados do INTERHEART salvos:",
    st.session_state["dados_interheart"]
)
    
if st.button("Calcular INTERHEART"):

    idade = st.session_state["dados_caso"]["idade"]
    sexo = st.session_state["dados_caso"]["sexo"]

    cintura = st.session_state["dados_clinicos"]["cintura"]
    quadril = st.session_state["dados_clinicos"]["quadril"]
    diabetes = st.session_state["dados_clinicos"]["diabetes"]
    tabagismo = st.session_state["dados_clinicos"]["tabagismo"]
    cigarros_dia = st.session_state["dados_clinicos"]["cigarros_dia"]

    dados_interheart = st.session_state["dados_interheart"]

    if (
        idade is None
        or sexo is None
        or cintura is None
        or quadril is None
        or diabetes is None
        or tabagismo is None
        or None in dados_interheart.values()
    ):
        st.error(
            "Preencha e salve todos os dados necessários "
            "antes de calcular o INTERHEART."
        )   
    else:

        rcq = round(cintura / quadril, 3)

        pontos_itens = {}


        # Idade e sexo
        if sexo == "Masculino" and idade >= 55:
            pontos_itens["idade_sexo"] = 2

        elif sexo == "Feminino" and idade >= 65:
            pontos_itens["idade_sexo"] = 2

        else:
            pontos_itens["idade_sexo"] = 0


        # Tabagismo
        if tabagismo == "Nunca fumou":
            pontos_itens["tabagismo"] = 0

        elif tabagismo == "Ex-fumante há mais de 12 meses":
            pontos_itens["tabagismo"] = 2

        else:

            if cigarros_dia <= 5:
                pontos_itens["tabagismo"] = 2

            elif cigarros_dia <= 10:
                pontos_itens["tabagismo"] = 4

            elif cigarros_dia <= 15:
                pontos_itens["tabagismo"] = 6

            elif cigarros_dia <= 20:
                pontos_itens["tabagismo"] = 7

            else:
                pontos_itens["tabagismo"] = 11


        # Fumo passivo
        if dados_interheart["fumo_passivo"] == "Sim":
            pontos_itens["fumo_passivo"] = 2
        else:
            pontos_itens["fumo_passivo"] = 0


        # Diabetes
        if diabetes == "Sim":
            pontos_itens["diabetes"] = 6
        else:
            pontos_itens["diabetes"] = 0


        # Hipertensão
        if dados_interheart["hipertensao"] == "Sim":
            pontos_itens["hipertensao"] = 5
        else:
            pontos_itens["hipertensao"] = 0


        # Histórico parental de infarto
        if dados_interheart["historico_parental_infarto"] == "Sim":
            pontos_itens["historico_parental_infarto"] = 4
        else:
            pontos_itens["historico_parental_infarto"] = 0


        # Relação cintura-quadril
        if rcq < 0.873:
            pontos_itens["rcq"] = 0

        elif rcq < 0.964:
            pontos_itens["rcq"] = 2

        else:
            pontos_itens["rcq"] = 4


        # Estresse
        if dados_interheart["estresse"] == "Vários períodos ou permanente":
            pontos_itens["estresse"] = 3
        else:
            pontos_itens["estresse"] = 0


        # Tristeza ou depressão
        if dados_interheart["tristeza_depressao"] == "Sim":
            pontos_itens["tristeza_depressao"] = 3
        else:
            pontos_itens["tristeza_depressao"] = 0


        # Alimentação
        if dados_interheart["alimento_salgado"] == "Sim":
            pontos_itens["alimento_salgado"] = 1
        else:
            pontos_itens["alimento_salgado"] = 0


        if dados_interheart["fritura_fast_food"] == "Sim":
            pontos_itens["fritura_fast_food"] = 1
        else:
            pontos_itens["fritura_fast_food"] = 0


        if dados_interheart["fruta_diaria"] == "Não":
            pontos_itens["fruta_diaria"] = 1
        else:
            pontos_itens["fruta_diaria"] = 0


        if dados_interheart["vegetais_diarios"] == "Não":
            pontos_itens["vegetais_diarios"] = 1
        else:
            pontos_itens["vegetais_diarios"] = 0


        if dados_interheart["carne_aves"] == "Sim":
            pontos_itens["carne_aves"] = 2
        else:
            pontos_itens["carne_aves"] = 0


        # Atividade física no lazer
        if (
            dados_interheart["atividade_lazer"]
            == "Sedentário ou esforço mínimo"
        ):
            pontos_itens["atividade_lazer"] = 2

        else:
            pontos_itens["atividade_lazer"] = 0


        # Soma dos pontos
        pontos_total = sum(
            pontos_itens.values()
        )


        # Classificação
        if pontos_total <= 9:
            classificacao = "Baixo risco"

        elif pontos_total <= 15:
            classificacao = "Risco moderado"

        else:
            classificacao = "Alto risco"


        # Salva o resultado
        st.session_state["avaliacao"]["interheart"] = {
            "pontos": pontos_total,
            "classificacao": classificacao,
            "rcq": rcq,
            "pontos_itens": pontos_itens
        }

        st.success("INTERHEART calculado com sucesso.")


resultado_interheart = st.session_state["avaliacao"]["interheart"]


if resultado_interheart is not None:

    st.subheader("Resultado INTERHEART")

    st.write(
        "Relação cintura-quadril:",
        resultado_interheart["rcq"]
    )

    st.write(
        "Pontuação:",
        resultado_interheart["pontos"]
    )

    st.write(
        "Classificação:",
        resultado_interheart["classificacao"]
    )

st.divider()

st.subheader("Classificação periodontal AAP/EFP")


# DICIONÁRIO DOS DADOS ESPECÍFICOS DA CLASSIFICAÇÃO PERIODONTAL

if "dados_periodontais" not in st.session_state:
    st.session_state["dados_periodontais"] = {
        "cal": None,
        "dentes_perdidos": None,
        "sondagem": None,
        "perda_vertical": None,
        "furca": None,
        "defeito_rebordo": None,
        "disfuncao_mastigatoria": None,
        "colapso_mordida": None,
        "migracao_dentaria": None,
        "abertura_leque": None,
        "mobilidade": None,
        "dentes_remanescentes": None,
        "percentual_dentes_envolvidos": None,
        "padrao_molar_incisivo": None,
        "progressao_5_anos": None,
        "fenotipo": None,
        "hba1c": None
    }


st.write(
    "Dados periodontais salvos:",
    st.session_state["dados_periodontais"]
)

st.markdown("### Estágio — critérios de severidade")


# O %PBL já vem da avaliação radiográfica
pbl = st.session_state["avaliacao"]["pbl"]


if pbl is None:
    st.info("Nenhum %PBL foi informado até o momento.")

else:
    st.write(
        "Perda óssea radiográfica (%PBL):",
        pbl,
        "%"
    )


with st.form("form_severidade_periodontal"):

    cal = st.number_input(
        "CAL interproximal máximo (mm):",
        min_value=0.0,
        value=None,
        step=0.1
    )

    dentes_perdidos = st.number_input(
        "Número de dentes perdidos atribuíveis à periodontite:",
        min_value=0,
        max_value=32,
        value=None,
        step=1
    )

    salvar_severidade = st.form_submit_button(
        "Salvar critérios de severidade"
    )


if salvar_severidade:

    st.session_state["dados_periodontais"]["cal"] = cal

    st.session_state["dados_periodontais"]["dentes_perdidos"] = (
        dentes_perdidos
    )

    st.success("Critérios de severidade salvos.")


st.write(
    "Severidade salva:",
    {
        "CAL": st.session_state["dados_periodontais"]["cal"],
        "%PBL": st.session_state["avaliacao"]["pbl"],
        "Dentes perdidos": st.session_state["dados_periodontais"]["dentes_perdidos"]
    }
)


st.markdown("### Estágio — fatores de complexidade")


with st.form("form_complexidade_periodontal_1"):

    sondagem = st.number_input(
        "Profundidade máxima de sondagem (mm):",
        min_value=0.0,
        value=None,
        step=0.1
    )

    perda_vertical = st.number_input(
        "Perda óssea vertical máxima (mm):",
        min_value=0.0,
        value=None,
        step=0.1
    )

    furca = st.selectbox(
        "Maior classe de furca:",
        [
            "Nenhuma",
            "I",
            "II",
            "III"
        ],
        index=None,
        placeholder="Selecione"
    )

    defeito_rebordo = st.selectbox(
        "Defeito do rebordo:",
        [
            "Nenhum",
            "Moderado",
            "Grave"
        ],
        index=None,
        placeholder="Selecione"
    )

    salvar_complexidade_1 = st.form_submit_button(
        "Salvar fatores de complexidade"
    )


if salvar_complexidade_1:

    st.session_state["dados_periodontais"]["sondagem"] = sondagem

    st.session_state["dados_periodontais"]["perda_vertical"] = (
        perda_vertical
    )

    st.session_state["dados_periodontais"]["furca"] = furca

    st.session_state["dados_periodontais"]["defeito_rebordo"] = (
        defeito_rebordo
    )

    st.success("Fatores de complexidade salvos.")


st.write(
    "Complexidade salva:",
    {
        "Sondagem": st.session_state["dados_periodontais"]["sondagem"],
        "Perda vertical": st.session_state["dados_periodontais"]["perda_vertical"],
        "Furca": st.session_state["dados_periodontais"]["furca"],
        "Defeito de rebordo": st.session_state["dados_periodontais"]["defeito_rebordo"]
    }
)

st.markdown("#### Outros fatores de complexidade")


with st.form("form_complexidade_periodontal_2"):

    disfuncao_mastigatoria = st.selectbox(
        "Há disfunção mastigatória?",
        ["Não", "Sim"],
        index=None,
        placeholder="Selecione"
    )

    mobilidade = st.selectbox(
        "Maior grau de mobilidade dentária:",
        [
            "Nenhuma",
            "I",
            "II",
            "III"
        ],
        index=None,
        placeholder="Selecione"
    )

    dentes_remanescentes = st.number_input(
        "Número de dentes remanescentes:",
        min_value=0,
        max_value=32,
        value=None,
        step=1
    )

    colapso_mordida = st.selectbox(
        "Há colapso de mordida?",
        ["Não", "Sim"],
        index=None,
        placeholder="Selecione"
    )

    migracao_dentaria = st.selectbox(
        "Há migração dentária?",
        ["Não", "Sim"],
        index=None,
        placeholder="Selecione"
    )

    abertura_leque = st.selectbox(
        "Há abertura em leque?",
        ["Não", "Sim"],
        index=None,
        placeholder="Selecione"
    )

    salvar_complexidade_2 = st.form_submit_button(
        "Salvar outros fatores de complexidade"
    )


if salvar_complexidade_2:

    st.session_state["dados_periodontais"]["disfuncao_mastigatoria"] = (
        disfuncao_mastigatoria
    )

    st.session_state["dados_periodontais"]["mobilidade"] = mobilidade

    st.session_state["dados_periodontais"]["dentes_remanescentes"] = (
        dentes_remanescentes
    )

    st.session_state["dados_periodontais"]["colapso_mordida"] = (
        colapso_mordida
    )

    st.session_state["dados_periodontais"]["migracao_dentaria"] = (
        migracao_dentaria
    )

    st.session_state["dados_periodontais"]["abertura_leque"] = (
        abertura_leque
    )

    st.success("Outros fatores de complexidade salvos.")


st.write(
    "Outros fatores de complexidade salvos:",
    {
        "Disfunção mastigatória":
            st.session_state["dados_periodontais"]["disfuncao_mastigatoria"],

        "Mobilidade":
            st.session_state["dados_periodontais"]["mobilidade"],

        "Dentes remanescentes":
            st.session_state["dados_periodontais"]["dentes_remanescentes"],

        "Colapso de mordida":
            st.session_state["dados_periodontais"]["colapso_mordida"],

        "Migração dentária":
            st.session_state["dados_periodontais"]["migracao_dentaria"],

        "Abertura em leque":
            st.session_state["dados_periodontais"]["abertura_leque"]
    }
)

st.markdown("### Extensão e distribuição")


with st.form("form_extensao_periodontal"):

    percentual_dentes_envolvidos = st.number_input(
        "Percentual de dentes envolvidos pela periodontite (%):",
        min_value=0.0,
        max_value=100.0,
        value=None,
        step=0.1
    )

    padrao_molar_incisivo = st.selectbox(
        "Há padrão molar/incisivo?",
        ["Não", "Sim"],
        index=None,
        placeholder="Selecione"
    )

    salvar_extensao = st.form_submit_button(
        "Salvar extensão e distribuição"
    )


if salvar_extensao:

    st.session_state["dados_periodontais"]["percentual_dentes_envolvidos"] = (
        percentual_dentes_envolvidos
    )

    st.session_state["dados_periodontais"]["padrao_molar_incisivo"] = (
        padrao_molar_incisivo
    )

    st.success("Dados de extensão e distribuição salvos.")


st.write(
    "Extensão e distribuição salvas:",
    {
        "Percentual de dentes envolvidos":
            st.session_state["dados_periodontais"][
                "percentual_dentes_envolvidos"
            ],

        "Padrão molar/incisivo":
            st.session_state["dados_periodontais"][
                "padrao_molar_incisivo"
            ]
    }
)

st.markdown("### Grau — progressão e modificadores")


# Dados que já foram preenchidos anteriormente
idade = st.session_state["dados_caso"]["idade"]

diabetes = st.session_state["dados_clinicos"]["diabetes"]

tabagismo = st.session_state["dados_clinicos"]["tabagismo"]

cigarros_dia = st.session_state["dados_clinicos"]["cigarros_dia"]


st.write(
    "Idade:",
    idade if idade is not None else "Não informada"
)

st.write(
    "Diabetes:",
    diabetes if diabetes is not None else "Não informado"
)

st.write(
    "Tabagismo:",
    tabagismo if tabagismo is not None else "Não informado"
)


with st.form("form_grau_periodontal"):

    progressao_5_anos = st.number_input(
        "Progressão periodontal em 5 anos (mm):",
        min_value=0.0,
        value=None,
        step=0.1
    )

    fenotipo = st.selectbox(
        "Fenótipo clínico em relação ao biofilme:",
        [
            "Biofilme abundante com baixa destruição",
            "Destruição proporcional ao biofilme",
            "Destruição superior à esperada"
        ],
        index=None,
        placeholder="Selecione"
    )

    hba1c = st.number_input(
        "HbA1c (%), quando disponível:",
        min_value=0.1,
        max_value=20.0,
        value=None,
        step=0.1
    )

    salvar_grau = st.form_submit_button(
        "Salvar dados para graduação"
    )


if salvar_grau:

    if hba1c is not None and diabetes != "Sim":

        st.error(
            "A HbA1c só deve ser informada quando "
            "o paciente possui diabetes diagnosticado."
        )

    else:

        st.session_state["dados_periodontais"]["progressao_5_anos"] = (
            progressao_5_anos
        )

        st.session_state["dados_periodontais"]["fenotipo"] = (
            fenotipo
        )

        st.session_state["dados_periodontais"]["hba1c"] = (
            hba1c
        )

        st.success("Dados para graduação salvos.")


st.write(
    "Dados para graduação salvos:",
    {
        "Progressão em 5 anos":
            st.session_state["dados_periodontais"]["progressao_5_anos"],

        "Fenótipo":
            st.session_state["dados_periodontais"]["fenotipo"],

        "HbA1c":
            st.session_state["dados_periodontais"]["hba1c"]
    }
)

#CALCULOS DE CLSSIFICAÇÃO DO ESTÁGIO - agora ficou pegado
st.markdown("### Classificação do estágio")


if st.button("Calcular estágio pela severidade"):

    dados_periodontais = st.session_state["dados_periodontais"]

    cal = dados_periodontais["cal"]
    dentes_perdidos = dados_periodontais["dentes_perdidos"]

    pbl = st.session_state["avaliacao"]["pbl"]


    # Começamos sem estágio definido
    estagio_severidade = None
    criterio_severidade = None


    # 1. CAL é o critério principal
    if cal is not None:

        if 1 <= cal < 3:
            estagio_severidade = "I"

        elif 3 <= cal < 5:
            estagio_severidade = "II"

        elif cal >= 5:
            estagio_severidade = "III"

        criterio_severidade = "CAL"


    # 2. Se não houver CAL, usamos o %PBL
    elif pbl is not None:

        if pbl < 15:
            estagio_severidade = "I"

        elif pbl <= 33:
            estagio_severidade = "II"

        else:
            estagio_severidade = "III"

        criterio_severidade = "%PBL"


    # 3. Perda dentária pode elevar o estágio
    if dentes_perdidos is not None:

        if dentes_perdidos >= 5:
            estagio_severidade = "IV"
            criterio_severidade = "Perda dentária"

        elif dentes_perdidos >= 1:

            if (
                estagio_severidade is None
                or estagio_severidade in ["I", "II"]
            ):
                estagio_severidade = "III"
                criterio_severidade = "Perda dentária"


    # 4. Verifica se foi possível determinar um estágio
    if estagio_severidade is None:

        st.warning(
            "Não foi possível determinar o estágio "
            "com os dados de severidade disponíveis."
        )

    else:

        # Cria o dicionário de resultado periodontal,
        # caso ele ainda esteja vazio
        if st.session_state["avaliacao"]["periodontal"] is None:
            st.session_state["avaliacao"]["periodontal"] = {}


        # Salva o resultado parcial
        st.session_state["avaliacao"]["periodontal"][
            "estagio_severidade"
        ] = estagio_severidade

        st.session_state["avaliacao"]["periodontal"][
            "criterio_severidade"
        ] = criterio_severidade

        st.success(
            "Estágio pela severidade calculado com sucesso."
        )
resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


if (
    resultado_periodontal is not None
    and "estagio_severidade" in resultado_periodontal
):

    st.subheader("Resultado parcial do estágio")

    st.write(
        "Estágio pela severidade:",
        resultado_periodontal["estagio_severidade"]
    )

    st.write(
        "Critério determinante:",
        resultado_periodontal["criterio_severidade"]
    )

    st.info(
        "Resultado parcial. Os fatores de complexidade "
        "ainda serão avaliados."
    )

resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


if (
    resultado_periodontal is not None
    and "estagio" in resultado_periodontal
):

    st.subheader("Estágio periodontal")

    st.write(
        "Estágio pela severidade:",
        resultado_periodontal["estagio_severidade"]
    )

    st.write(
        "Estágio final:",
        resultado_periodontal["estagio"]
    )

    st.write(
        "Fatores de complexidade identificados:",
        resultado_periodontal["fatores_complexidade"]
    )

#APLICA FATORES DE COMPLEXIDADES
if st.button("Aplicar fatores de complexidade"):

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    if (
        resultado_periodontal is None
        or "estagio_severidade" not in resultado_periodontal
    ):
        st.error(
            "Calcule primeiro o estágio pela severidade."
        )

    else:

        dados_periodontais = st.session_state["dados_periodontais"]

        estagio_final = resultado_periodontal["estagio_severidade"]

        fatores_complexidade = []


        # Profundidade de sondagem
        sondagem = dados_periodontais["sondagem"]

        if sondagem is not None:

            if sondagem >= 6:

                if estagio_final in ["I", "II"]:
                    estagio_final = "III"

                fatores_complexidade.append(
                    "Profundidade de sondagem ≥ 6 mm"
                )

            elif sondagem > 4:

                if estagio_final == "I":
                    estagio_final = "II"

                fatores_complexidade.append(
                    "Profundidade de sondagem > 4 mm"
                )


        # Perda óssea vertical
        perda_vertical = dados_periodontais["perda_vertical"]

        if (
            perda_vertical is not None
            and perda_vertical >= 3
        ):

            if estagio_final in ["I", "II"]:
                estagio_final = "III"

            fatores_complexidade.append(
                "Perda óssea vertical ≥ 3 mm"
            )


        # Furca
        furca = dados_periodontais["furca"]

        if furca in ["II", "III"]:

            if estagio_final in ["I", "II"]:
                estagio_final = "III"

            fatores_complexidade.append(
                "Envolvimento de furca classe II ou III"
            )


        # Defeito do rebordo
        defeito_rebordo = dados_periodontais["defeito_rebordo"]

        if defeito_rebordo == "Moderado":

            if estagio_final in ["I", "II"]:
                estagio_final = "III"

            fatores_complexidade.append(
                "Defeito moderado de rebordo"
            )

        elif defeito_rebordo == "Grave":

            estagio_final = "IV"

            fatores_complexidade.append(
                "Defeito grave de rebordo"
            )


        # Disfunção mastigatória
        if (
            dados_periodontais["disfuncao_mastigatoria"]
            == "Sim"
        ):

            estagio_final = "IV"

            fatores_complexidade.append(
                "Disfunção mastigatória"
            )


        # Mobilidade
        mobilidade = dados_periodontais["mobilidade"]

        if mobilidade in ["II", "III"]:

            estagio_final = "IV"

            fatores_complexidade.append(
                "Mobilidade dentária grau II ou III"
            )


        # Colapso de mordida
        if dados_periodontais["colapso_mordida"] == "Sim":

            estagio_final = "IV"

            fatores_complexidade.append(
                "Colapso de mordida"
            )


        # Migração dentária
        if dados_periodontais["migracao_dentaria"] == "Sim":

            estagio_final = "IV"

            fatores_complexidade.append(
                "Migração dentária"
            )


        # Abertura em leque
        if dados_periodontais["abertura_leque"] == "Sim":

            estagio_final = "IV"

            fatores_complexidade.append(
                "Abertura em leque"
            )


        # Dentição reduzida
        dentes_remanescentes = (
            dados_periodontais["dentes_remanescentes"]
        )

        dentes_perdidos = (
            dados_periodontais["dentes_perdidos"]
        )

        if (
            dentes_remanescentes is not None
            and dentes_remanescentes < 20
            and dentes_perdidos is not None
            and dentes_perdidos > 0
        ):

            estagio_final = "IV"

            fatores_complexidade.append(
                "Menos de 20 dentes remanescentes"
            )


        # Salva o estágio final
        resultado_periodontal["estagio"] = estagio_final

        resultado_periodontal["fatores_complexidade"] = (
            fatores_complexidade
        )

        st.success(
            "Fatores de complexidade aplicados com sucesso."
        )

        # CALCULA EXTENSÃO E DISTRIBUIÇÃO

st.markdown("### Classificação da extensão e distribuição")


if st.button("Calcular extensão/distribuição"):

    dados_periodontais = st.session_state["dados_periodontais"]

    percentual = dados_periodontais["percentual_dentes_envolvidos"]

    padrao_molar_incisivo = dados_periodontais[
        "padrao_molar_incisivo"
    ]


    # O padrão molar/incisivo tem prioridade
    if padrao_molar_incisivo == "Sim":

        extensao_distribuicao = "Padrão molar/incisivo"


    # Se não houver padrão molar/incisivo,
    # precisamos do percentual de dentes envolvidos
    elif percentual is None:

        st.error(
            "Informe o percentual de dentes envolvidos "
            "antes de calcular a extensão."
        )

        extensao_distribuicao = None


    # Menos de 30% = localizada
    elif percentual < 30:

        extensao_distribuicao = "Localizada"


    # 30% ou mais = generalizada
    else:

        extensao_distribuicao = "Generalizada"


    # Só salva se conseguimos calcular
    if extensao_distribuicao is not None:

        if st.session_state["avaliacao"]["periodontal"] is None:
            st.session_state["avaliacao"]["periodontal"] = {}

        st.session_state["avaliacao"]["periodontal"][
            "extensao_distribuicao"
        ] = extensao_distribuicao

        st.success(
            "Extensão/distribuição calculada com sucesso."
        )


resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


if (
    resultado_periodontal is not None
    and "extensao_distribuicao" in resultado_periodontal
):

    st.write(
        "Extensão/distribuição:",
        resultado_periodontal["extensao_distribuicao"]
    )
# CALCULA O GRAU-BASE PELA PROGRESSÃO

st.markdown("### Classificação do grau")


if st.button("Calcular grau pela progressão"):

    dados_periodontais = st.session_state["dados_periodontais"]

    progressao = dados_periodontais["progressao_5_anos"]

    fenotipo = dados_periodontais["fenotipo"]

    idade = st.session_state["dados_caso"]["idade"]

    pbl = st.session_state["avaliacao"]["pbl"]


    grau_base = None

    criterio_grau_base = None

    razao_pbl_idade = None


    # 1. Primeiro usamos a progressão direta em 5 anos
    if progressao is not None:

        if progressao == 0:
            grau_base = "A"

        elif progressao < 2:
            grau_base = "B"

        else:
            grau_base = "C"

        criterio_grau_base = "Progressão em 5 anos"


    # 2. Se não houver progressão direta,
    # usamos a relação %PBL / idade
    elif pbl is not None and idade is not None:

        razao_pbl_idade = round(
            pbl / idade,
            2
        )

        if razao_pbl_idade < 0.25:
            grau_base = "A"

        elif razao_pbl_idade <= 1:
            grau_base = "B"

        else:
            grau_base = "C"

        criterio_grau_base = "%PBL / idade"


        # O fenótipo pode elevar a estimativa indireta

        if (
            fenotipo == "Destruição proporcional ao biofilme"
            and grau_base == "A"
        ):
            grau_base = "B"
            criterio_grau_base = "%PBL / idade + fenótipo"


        elif fenotipo == "Destruição superior à esperada":
            grau_base = "C"
            criterio_grau_base = "%PBL / idade + fenótipo"


    # 3. Se não houver progressão nem %PBL/idade,
    # tentamos usar apenas o fenótipo
    elif fenotipo is not None:

        if fenotipo == "Biofilme abundante com baixa destruição":
            grau_base = "A"

        elif fenotipo == "Destruição proporcional ao biofilme":
            grau_base = "B"

        else:
            grau_base = "C"

        criterio_grau_base = "Fenótipo"


    # 4. Se nenhum critério estiver disponível
    if grau_base is None:

        st.warning(
            "Não foi possível calcular o grau com "
            "os dados de progressão disponíveis."
        )


    else:

        if st.session_state["avaliacao"]["periodontal"] is None:
            st.session_state["avaliacao"]["periodontal"] = {}


        st.session_state["avaliacao"]["periodontal"][
            "grau_base"
        ] = grau_base

        st.session_state["avaliacao"]["periodontal"][
            "criterio_grau_base"
        ] = criterio_grau_base

        st.session_state["avaliacao"]["periodontal"][
            "razao_pbl_idade"
        ] = razao_pbl_idade


        st.success(
            "Grau-base calculado com sucesso."
        )


resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


if (
    resultado_periodontal is not None
    and "grau_base" in resultado_periodontal
):

    st.subheader("Resultado parcial do grau")

    st.write(
        "Grau-base:",
        resultado_periodontal["grau_base"]
    )

    st.write(
        "Critério utilizado:",
        resultado_periodontal["criterio_grau_base"]
    )


    if resultado_periodontal["razao_pbl_idade"] is not None:

        st.write(
            "Relação %PBL / idade:",
            resultado_periodontal["razao_pbl_idade"]
        )


    st.info(
        "Resultado parcial. Tabagismo e diabetes "
        "ainda serão aplicados como modificadores."
    )

    # APLICA OS MODIFICADORES DO GRAU

if st.button("Aplicar modificadores do grau"):

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


    # Primeiro precisamos ter um grau-base calculado
    if (
        resultado_periodontal is None
        or "grau_base" not in resultado_periodontal
    ):

        st.error(
            "Calcule primeiro o grau pela progressão."
        )


    else:

        dados_periodontais = st.session_state["dados_periodontais"]

        tabagismo = st.session_state["dados_clinicos"]["tabagismo"]

        cigarros_dia = st.session_state["dados_clinicos"]["cigarros_dia"]

        diabetes = st.session_state["dados_clinicos"]["diabetes"]

        hba1c = dados_periodontais["hba1c"]


        # Começamos pelo grau obtido na etapa anterior
        grau_final = resultado_periodontal["grau_base"]

        modificadores_grau = []


        # -------------------------
        # TABAGISMO
        # -------------------------

        if tabagismo == "Fumante atual ou nos últimos 12 meses":

            if cigarros_dia is None:

                st.error(
                    "Informe a média de cigarros por dia."
                )

            elif cigarros_dia < 10:

                # Grau B não pode diminuir um Grau C
                if grau_final == "A":
                    grau_final = "B"

                modificadores_grau.append(
                    "Tabagismo < 10 cigarros/dia"
                )

            else:

                grau_final = "C"

                modificadores_grau.append(
                    "Tabagismo ≥ 10 cigarros/dia"
                )


        # -------------------------
        # DIABETES
        # -------------------------

        if diabetes == "Sim":

            if hba1c is None:

                st.warning(
                    "Diabetes informado, mas sem HbA1c. "
                    "O diabetes não modificou o grau."
                )

            elif hba1c < 7:

                # Grau B não pode diminuir um Grau C
                if grau_final == "A":
                    grau_final = "B"

                modificadores_grau.append(
                    "Diabetes com HbA1c < 7%"
                )

            else:

                grau_final = "C"

                modificadores_grau.append(
                    "Diabetes com HbA1c ≥ 7%"
                )


        elif diabetes == "Não sabe":

            st.warning(
                "Situação de diabetes desconhecida. "
                "Nenhum modificador de diabetes foi aplicado."
            )


        # Salva o resultado final
        resultado_periodontal["grau"] = grau_final

        resultado_periodontal["modificadores_grau"] = (
            modificadores_grau
        )


        st.success(
            "Modificadores aplicados com sucesso."
        )
        resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


if (
    resultado_periodontal is not None
    and "grau" in resultado_periodontal
):

    st.subheader("Grau periodontal")

    st.write(
        "Grau-base:",
        resultado_periodontal["grau_base"]
    )

    st.write(
        "Grau final:",
        resultado_periodontal["grau"]
    )

    st.write(
        "Modificadores identificados:",
        resultado_periodontal["modificadores_grau"]
    )
    # CONSOLIDA A CLASSIFICAÇÃO PERIODONTAL FINAL

st.markdown("### Classificação periodontal final")


if st.button("Gerar classificação periodontal final"):

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


    # Verifica se existe resultado periodontal
    if resultado_periodontal is None:

        st.error(
            "Ainda não há resultados periodontais calculados."
        )


    # Verifica se o estágio final já foi calculado
    elif "estagio" not in resultado_periodontal:

        st.error(
            "Calcule primeiro o estágio periodontal final."
        )


    # Verifica se a extensão/distribuição já foi calculada
    elif "extensao_distribuicao" not in resultado_periodontal:

        st.error(
            "Calcule primeiro a extensão/distribuição."
        )


    # Verifica se o grau final já foi calculado
    elif "grau" not in resultado_periodontal:

        st.error(
            "Calcule primeiro o grau periodontal final."
        )


    else:

        estagio = resultado_periodontal["estagio"]

        extensao = resultado_periodontal[
            "extensao_distribuicao"
        ]

        grau = resultado_periodontal["grau"]


        classificacao_final = (
            f"Periodontite Estágio {estagio}, "
            f"{extensao}, "
            f"Grau {grau}"
        )


        resultado_periodontal[
            "classificacao_final"
        ] = classificacao_final


        st.success(
            "Classificação periodontal final gerada com sucesso."
        )
        resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


if (
    resultado_periodontal is not None
    and "classificacao_final" in resultado_periodontal
):

    st.subheader("Resultado periodontal final")

    st.write(
        "Estágio:",
        resultado_periodontal["estagio"]
    )

    st.write(
        "Extensão/distribuição:",
        resultado_periodontal["extensao_distribuicao"]
    )

    st.write(
        "Grau:",
        resultado_periodontal["grau"]
    )

    st.success(
        resultado_periodontal["classificacao_final"]
    )

    st.divider()

st.header("Relatório integrado")


# Pegamos os dados principais já armazenados
dados_caso = st.session_state["dados_caso"]

resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

resultado_findrisc = st.session_state["avaliacao"]["findrisc"]

resultado_interheart = st.session_state["avaliacao"]["interheart"]


st.subheader("Identificação do caso")

st.write(
    "Código:",
    dados_caso["codigo"]
)

st.write(
    "Idade:",
    dados_caso["idade"]
)

st.write(
    "Sexo:",
    dados_caso["sexo"]
)


st.subheader("Resumo dos resultados")


# CLASSIFICAÇÃO PERIODONTAL

if (
    resultado_periodontal is not None
    and "classificacao_final" in resultado_periodontal
):

    st.write(
        "Classificação periodontal:",
        resultado_periodontal["classificacao_final"]
    )

else:

    st.write(
        "Classificação periodontal: ainda não concluída."
    )


# FINDRISC

if resultado_findrisc is not None:

    st.write(
        "FINDRISC:",
        resultado_findrisc["pontos"],
        "pontos —",
        resultado_findrisc["classificacao"]
    )

else:

    st.write(
        "FINDRISC: ainda não calculado."
    )


# INTERHEART

if resultado_interheart is not None:

    st.write(
        "INTERHEART:",
        resultado_interheart["pontos"],
        "pontos —",
        resultado_interheart["classificacao"]
    )

else:

    st.write(
        "INTERHEART: ainda não calculado."
    )
# DETALHAMENTO DOS RESULTADOS

st.subheader("Detalhamento periodontal")


if resultado_periodontal is not None:

    if "estagio" in resultado_periodontal:

        st.write(
            "Estágio final:",
            resultado_periodontal["estagio"]
        )


    if "criterio_severidade" in resultado_periodontal:

        st.write(
            "Critério principal de severidade:",
            resultado_periodontal["criterio_severidade"]
        )


    if "extensao_distribuicao" in resultado_periodontal:

        st.write(
            "Extensão/distribuição:",
            resultado_periodontal["extensao_distribuicao"]
        )


    if "grau" in resultado_periodontal:

        st.write(
            "Grau final:",
            resultado_periodontal["grau"]
        )


    if "criterio_grau_base" in resultado_periodontal:

        st.write(
            "Critério utilizado para o grau-base:",
            resultado_periodontal["criterio_grau_base"]
        )

else:

    st.write(
        "Ainda não existem resultados periodontais."
    )


# %PBL

pbl = st.session_state["avaliacao"]["pbl"]


if pbl is not None:

    st.write(
        "Perda óssea radiográfica (%PBL):",
        pbl,
        "%"
    )

else:

    st.write(
        "Perda óssea radiográfica (%PBL): não informada."
    )


# Fatores de complexidade

if (
    resultado_periodontal is not None
    and "fatores_complexidade" in resultado_periodontal
):

    fatores = resultado_periodontal["fatores_complexidade"]

    if len(fatores) > 0:

        st.write(
            "Fatores de complexidade identificados:"
        )

        for fator in fatores:
            st.write("-", fator)

    else:

        st.write(
            "Fatores de complexidade identificados: nenhum."
        )


# Modificadores do grau

if (
    resultado_periodontal is not None
    and "modificadores_grau" in resultado_periodontal
):

    modificadores = resultado_periodontal["modificadores_grau"]

    if len(modificadores) > 0:

        st.write(
            "Modificadores do grau identificados:"
        )

        for modificador in modificadores:
            st.write("-", modificador)

    else:

        st.write(
            "Modificadores do grau identificados: nenhum."
        )


# Relação %PBL / idade

if (
    resultado_periodontal is not None
    and "razao_pbl_idade" in resultado_periodontal
    and resultado_periodontal["razao_pbl_idade"] is not None
):

    st.write(
        "Relação %PBL / idade:",
        resultado_periodontal["razao_pbl_idade"]
    )


# FINDRISC

st.subheader("Detalhamento FINDRISC")


if resultado_findrisc is not None:

    st.write(
        "Pontuação:",
        resultado_findrisc["pontos"]
    )

    st.write(
        "Classificação:",
        resultado_findrisc["classificacao"]
    )

    st.write(
        "Risco estimado em 10 anos:",
        resultado_findrisc["estimativa"]
    )

else:

    st.write(
        "FINDRISC ainda não calculado."
    )


# INTERHEART

st.subheader("Detalhamento INTERHEART")


if resultado_interheart is not None:

    st.write(
        "Pontuação:",
        resultado_interheart["pontos"]
    )

    st.write(
        "Classificação:",
        resultado_interheart["classificacao"]
    )

    st.write(
        "Relação cintura-quadril:",
        resultado_interheart["rcq"]
    )

else:

    st.write(
        "INTERHEART ainda não calculado."
    )


# DADOS UTILIZADOS NO RELATÓRIO

st.subheader("Dados utilizados")


dados_clinicos = st.session_state["dados_clinicos"]


with st.expander("Ver dados clínicos compartilhados"):

    st.write(
        "Peso:",
        dados_clinicos["peso"],
        "kg"
    )

    st.write(
        "Altura:",
        dados_clinicos["altura"],
        "m"
    )

    st.write(
        "IMC:",
        dados_clinicos["imc"],
        "kg/m²"
    )

    st.write(
        "Circunferência da cintura:",
        dados_clinicos["cintura"],
        "cm"
    )

    st.write(
        "Circunferência do quadril:",
        dados_clinicos["quadril"],
        "cm"
    )

    st.write(
        "Diabetes:",
        dados_clinicos["diabetes"]
    )

    st.write(
        "Tabagismo:",
        dados_clinicos["tabagismo"]
    )


    # Cigarros por dia só é relevante para fumantes
    if (
        dados_clinicos["tabagismo"]
        == "Fumante atual ou nos últimos 12 meses"
    ):

        st.write(
            "Média de cigarros por dia:",
            dados_clinicos["cigarros_dia"]
        )
    
# DADOS ESPECÍFICOS DOS MÓDULOS


# FINDRISC

dados_findrisc = st.session_state["dados_findrisc"]


with st.expander("Ver dados utilizados no FINDRISC"):

    st.write(
        "Atividade física:",
        dados_findrisc["atividade_fisica"]
    )

    st.write(
        "Consumo diário de frutas ou vegetais:",
        dados_findrisc["frutas_vegetais"]
    )

    st.write(
        "Uso de medicamento para pressão alta:",
        dados_findrisc["medicacao_pressao"]
    )

    st.write(
        "Histórico de glicemia elevada:",
        dados_findrisc["glicemia_elevada"]
    )

    st.write(
        "Histórico familiar de diabetes:",
        dados_findrisc["historico_familiar"]
    )


# INTERHEART

dados_interheart = st.session_state["dados_interheart"]


with st.expander("Ver dados utilizados no INTERHEART"):

    st.write(
        "Hipertensão:",
        dados_interheart["hipertensao"]
    )

    st.write(
        "Histórico parental de infarto:",
        dados_interheart["historico_parental_infarto"]
    )

    st.write(
        "Estresse:",
        dados_interheart["estresse"]
    )

    st.write(
        "Exposição ao fumo passivo:",
        dados_interheart["fumo_passivo"]
    )

    st.write(
        "Atividade física no lazer:",
        dados_interheart["atividade_lazer"]
    )

    st.write(
        "Tristeza ou depressão:",
        dados_interheart["tristeza_depressao"]
    )

    st.write(
        "Consumo de alimentos salgados:",
        dados_interheart["alimento_salgado"]
    )

    st.write(
        "Consumo de fritura ou fast-food:",
        dados_interheart["fritura_fast_food"]
    )

    st.write(
        "Consumo diário de frutas:",
        dados_interheart["fruta_diaria"]
    )

    st.write(
        "Consumo diário de vegetais:",
        dados_interheart["vegetais_diarios"]
    )

    st.write(
        "Consumo de carne ou aves:",
        dados_interheart["carne_aves"]
    )


# CLASSIFICAÇÃO PERIODONTAL

dados_periodontais = st.session_state["dados_periodontais"]


with st.expander(
    "Ver dados utilizados na classificação periodontal"
):

    st.write(
        "CAL interproximal máximo:",
        dados_periodontais["cal"],
        "mm"
    )

    st.write(
        "Dentes perdidos por periodontite:",
        dados_periodontais["dentes_perdidos"]
    )

    st.write(
        "Profundidade máxima de sondagem:",
        dados_periodontais["sondagem"],
        "mm"
    )

    st.write(
        "Perda óssea vertical máxima:",
        dados_periodontais["perda_vertical"],
        "mm"
    )

    st.write(
        "Furca:",
        dados_periodontais["furca"]
    )

    st.write(
        "Defeito do rebordo:",
        dados_periodontais["defeito_rebordo"]
    )

    st.write(
        "Disfunção mastigatória:",
        dados_periodontais["disfuncao_mastigatoria"]
    )

    st.write(
        "Mobilidade dentária:",
        dados_periodontais["mobilidade"]
    )

    st.write(
        "Dentes remanescentes:",
        dados_periodontais["dentes_remanescentes"]
    )

    st.write(
        "Colapso de mordida:",
        dados_periodontais["colapso_mordida"]
    )

    st.write(
        "Migração dentária:",
        dados_periodontais["migracao_dentaria"]
    )

    st.write(
        "Abertura em leque:",
        dados_periodontais["abertura_leque"]
    )

    st.write(
        "Percentual de dentes envolvidos:",
        dados_periodontais["percentual_dentes_envolvidos"],
        "%"
    )

    st.write(
        "Padrão molar/incisivo:",
        dados_periodontais["padrao_molar_incisivo"]
    )

    st.write(
        "Progressão periodontal em 5 anos:",
        dados_periodontais["progressao_5_anos"],
        "mm"
    )

    st.write(
        "Fenótipo clínico:",
        dados_periodontais["fenotipo"]
    )


    if dados_periodontais["hba1c"] is not None:

        st.write(
            "HbA1c:",
            dados_periodontais["hba1c"],
            "%"
        )

# SITUAÇÃO DA AVALIAÇÃO

st.subheader("Situação da avaliação")


# Lista que armazenará tudo que estiver faltando
pendencias = []


# Dados do caso

if (
    dados_caso["codigo"] is None
    or dados_caso["idade"] is None
    or dados_caso["sexo"] is None
):

    pendencias.append(
        "Dados de identificação do caso incompletos."
    )


# %PBL

if pbl is None:

    pendencias.append(
        "%PBL ainda não informado."
    )


# FINDRISC

if resultado_findrisc is None:

    pendencias.append(
        "FINDRISC ainda não calculado."
    )


# INTERHEART

if resultado_interheart is None:

    pendencias.append(
        "INTERHEART ainda não calculado."
    )


# Classificação periodontal

if (
    resultado_periodontal is None
    or "classificacao_final" not in resultado_periodontal
):

    pendencias.append(
        "Classificação periodontal ainda não concluída."
    )


# RESULTADO DA VERIFICAÇÃO

if len(pendencias) == 0:

    st.success(
        "Avaliação completa. "
        "Todos os resultados necessários estão disponíveis."
    )

else:

    st.warning(
        "A avaliação ainda possui pendências."
    )

    for pendencia in pendencias:

        st.write(
            "-",
            pendencia
        )
# AVISOS E LIMITAÇÕES

st.subheader("Avisos e limitações")


st.info(
    "Esta aplicação é uma ferramenta de apoio à decisão clínica "
    "e não substitui a avaliação e a decisão do profissional."
)


st.write(
    "- FINDRISC e INTERHEART são utilizados como instrumentos "
    "de rastreamento de risco e não estabelecem diagnóstico médico."
)


st.write(
    "- A classificação periodontal depende dos dados clínicos "
    "e radiográficos informados na aplicação."
)


st.write(
    "- O %PBL deve ser interpretado em conjunto com os demais "
    "achados clínicos utilizados na classificação periodontal."
)


st.write(
    "- Dados ausentes podem limitar ou impedir determinados "
    "cálculos e classificações."
)


# PREPARAÇÃO DO RELATÓRIO FINAL

st.subheader("Preparação do relatório final")


if len(pendencias) == 0:
    
    data_hora_relatorio = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    # Prepara os fatores de complexidade para o relatório
    fatores_complexidade = resultado_periodontal[
        "fatores_complexidade"
    ]

    if len(fatores_complexidade) > 0:

        fatores_texto = ", ".join(
            fatores_complexidade
        )

    else:

        fatores_texto = "Nenhum"


    # Prepara os modificadores do grau para o relatório
    modificadores_grau = resultado_periodontal[
        "modificadores_grau"
    ]

    if len(modificadores_grau) > 0:

        modificadores_texto = ", ".join(
            modificadores_grau
        )

    else:

        modificadores_texto = "Nenhum"

    # Começamos pela identificação do caso
    texto_relatorio = (
        "RELATÓRIO INTEGRADO\n"
        "\n"
        "IDENTIFICAÇÃO DO CASO\n"
        f"Código: {dados_caso['codigo']}\n"
        f"Idade: {dados_caso['idade']}\n"
        f"Sexo: {dados_caso['sexo']}\n"
    )


    # Resumo dos resultados
    texto_relatorio += (
        "\n"
        "RESUMO DOS RESULTADOS\n"
        f"Classificação periodontal: "
        f"{resultado_periodontal['classificacao_final']}\n"
        f"FINDRISC: {resultado_findrisc['pontos']} pontos - "
        f"{resultado_findrisc['classificacao']}\n"
        f"INTERHEART: {resultado_interheart['pontos']} pontos - "
        f"{resultado_interheart['classificacao']}\n"
        f"%PBL: {pbl}%\n"
    )


    # Classificação periodontal
    texto_relatorio += (
        "\n"
        "CLASSIFICAÇÃO PERIODONTAL\n"
        f"Estágio final: {resultado_periodontal['estagio']}\n"
        f"Extensão/distribuição: "
        f"{resultado_periodontal['extensao_distribuicao']}\n"
        f"Grau final: {resultado_periodontal['grau']}\n"
        f"Critério de severidade: "
        f"{resultado_periodontal['criterio_severidade']}\n"
        f"Critério do grau-base: "
        f"{resultado_periodontal['criterio_grau_base']}\n"
        f"Fatores de complexidade: {fatores_texto}\n"
        f"Modificadores do grau: {modificadores_texto}\n"
    )

    if resultado_periodontal["razao_pbl_idade"] is not None:

        texto_relatorio += (
            f"Relação %PBL / idade: "
            f"{resultado_periodontal['razao_pbl_idade']}\n"
        )


    # FINDRISC
    texto_relatorio += (
        "\n"
        "FINDRISC\n"
        f"Pontuação: {resultado_findrisc['pontos']}\n"
        f"Classificação: {resultado_findrisc['classificacao']}\n"
        f"Estimativa em 10 anos: "
        f"{resultado_findrisc['estimativa']}\n"
    )

    texto_relatorio += (
        "\n"
        "DADOS CLÍNICOS UTILIZADOS\n"
        f"Peso: {dados_clinicos['peso']} kg\n"
        f"Altura: {dados_clinicos['altura']} m\n"
        f"IMC: {dados_clinicos['imc']} kg/m²\n"
        f"Cintura: {dados_clinicos['cintura']} cm\n"
        f"Quadril: {dados_clinicos['quadril']} cm\n"
        f"Diabetes: {dados_clinicos['diabetes']}\n"
        f"Tabagismo: {dados_clinicos['tabagismo']}\n"
    )

    if (
        dados_clinicos["tabagismo"]
        == "Fumante atual ou nos últimos 12 meses"
    ):

        texto_relatorio += (
            f"Média de cigarros por dia: "
            f"{dados_clinicos['cigarros_dia']}\n"
        )
        
    texto_relatorio += (
        "\n"
        "DADOS UTILIZADOS NO FINDRISC\n"
        f"Atividade física: "
        f"{dados_findrisc['atividade_fisica']}\n"
        f"Frutas ou vegetais diariamente: "
        f"{dados_findrisc['frutas_vegetais']}\n"
        f"Medicamento para pressão alta: "
        f"{dados_findrisc['medicacao_pressao']}\n"
        f"Glicemia elevada: "
        f"{dados_findrisc['glicemia_elevada']}\n"
        f"Histórico familiar de diabetes: "
        f"{dados_findrisc['historico_familiar']}\n"
    )



    # INTERHEART
    texto_relatorio += (
        "\n"
        "INTERHEART\n"
        f"Pontuação: {resultado_interheart['pontos']}\n"
        f"Classificação: {resultado_interheart['classificacao']}\n"
        f"Relação cintura-quadril: "
        f"{resultado_interheart['rcq']}\n"
    )

    texto_relatorio += (
        "\n"
        "DADOS UTILIZADOS NA CLASSIFICAÇÃO PERIODONTAL\n"
        f"CAL máximo: {dados_periodontais['cal']} mm\n"
        f"%PBL: {pbl}%\n"
        f"Dentes perdidos por periodontite: "
        f"{dados_periodontais['dentes_perdidos']}\n"
        f"Profundidade máxima de sondagem: "
        f"{dados_periodontais['sondagem']} mm\n"
        f"Perda óssea vertical máxima: "
        f"{dados_periodontais['perda_vertical']} mm\n"
        f"Furca: {dados_periodontais['furca']}\n"
        f"Defeito do rebordo: "
        f"{dados_periodontais['defeito_rebordo']}\n"
        f"Disfunção mastigatória: "
        f"{dados_periodontais['disfuncao_mastigatoria']}\n"
        f"Mobilidade: {dados_periodontais['mobilidade']}\n"
        f"Dentes remanescentes: "
        f"{dados_periodontais['dentes_remanescentes']}\n"
        f"Colapso de mordida: "
        f"{dados_periodontais['colapso_mordida']}\n"
        f"Migração dentária: "
        f"{dados_periodontais['migracao_dentaria']}\n"
        f"Abertura em leque: "
        f"{dados_periodontais['abertura_leque']}\n"
        f"Percentual de dentes envolvidos: "
        f"{dados_periodontais['percentual_dentes_envolvidos']}%\n"
        f"Padrão molar/incisivo: "
        f"{dados_periodontais['padrao_molar_incisivo']}\n"
        f"Progressão em 5 anos: "
        f"{dados_periodontais['progressao_5_anos']} mm\n"
        f"Fenótipo: {dados_periodontais['fenotipo']}\n"
    )

    if dados_periodontais["hba1c"] is not None:

        texto_relatorio += (
            f"HbA1c: {dados_periodontais['hba1c']}%\n"
        )

    # Avisos
    texto_relatorio += (
        "\n"
        "AVISOS E LIMITAÇÕES\n"
        "- Esta aplicação é uma ferramenta de apoio à decisão clínica "
        "e não substitui a avaliação e a decisão do profissional.\n"
        "- FINDRISC e INTERHEART são instrumentos de rastreamento "
        "de risco e não estabelecem diagnóstico médico.\n"
        "- A classificação periodontal depende da qualidade "
        "dos dados informados.\n"
    )

    texto_relatorio += (
    "\n"
    "IDENTIFICAÇÃO DO RELATÓRIO\n"
    f"Caso: {dados_caso['codigo']}\n"
    f"Gerado em: {data_hora_relatorio}\n"
    "Aplicação: Apoio à Decisão Clínica em Periodontia\n"
    )


    # Mostra uma prévia
    st.text_area(
        "Prévia do relatório:",
        texto_relatorio,
        height=400
    )


    # DOWNLOAD DO RELATÓRIO

    nome_arquivo = (
        f"relatorio_{dados_caso['codigo']}.txt"
    )


    st.download_button(
        label="Baixar relatório",
        data=texto_relatorio,
        file_name=nome_arquivo,
        mime="text/plain"
    )

    # RELATÓRIO EM HTML


    
        # Retira o primeiro título do texto,
    # pois o HTML já terá seu próprio título
    texto_html = texto_relatorio.replace(
        "RELATÓRIO INTEGRADO\n\n",
        "",
        1
    )


    # Prepara o texto para ser usado com segurança no HTML
    texto_seguro = escape(texto_html)


    # Cria o HTML formatado
    html_relatorio = f"""
    <!DOCTYPE html>

    <html>

    <head>

        <meta charset="UTF-8">

        <title>Relatório integrado</title>

        <style>

            @page {{
                size: A4;
                margin: 20mm;
            }}


            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 40px auto;
                color: #222222;
            }}


            h1 {{
                text-align: center;
                margin-bottom: 30px;
            }}


            pre {{
                font-family: Arial, sans-serif;
                font-size: 15px;
                line-height: 1.6;
                white-space: pre-wrap;
            }}


            @media print {{

                body {{
                    max-width: none;
                    margin: 0;
                }}

            }}

        </style>

    </head>


    <body>

        <h1>Relatório Integrado</h1>

        <pre>{texto_seguro}</pre>

    </body>

    </html>
    """


    # Nome do arquivo
    nome_arquivo_html = (
        f"relatorio_{dados_caso['codigo']}.html"
    )


    # Botão de download
    st.download_button(
        label="Baixar relatório para impressão",
        data=html_relatorio,
        file_name=nome_arquivo_html,
        mime="text/html"
    )


else:

    st.warning(
        "O relatório final só poderá ser preparado "
        "quando a avaliação estiver completa."
    )
