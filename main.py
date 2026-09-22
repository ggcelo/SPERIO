from html import escape

import streamlit as st

from state import inicializar_session_state
from modulo_radiografico import mostrar_modulo_radiografico
from modulo_findrisc import mostrar_findrisc
from modulo_interheart import mostrar_interheart
from modulo_periodontal import mostrar_modulo_periodontal
from relatorio import mostrar_relatorio
from planilhas import mostrar_validacao

st.set_page_config(
    page_title="Apoio à Decisão em Periodontia",
    page_icon="🦷",
    layout="wide"
)


# O CSS principal fica concentrado aqui e é aplicado a todos os módulos.
st.markdown(
    """
    <style>
        :root {
            --perio-ink: #17352f;
            --perio-text: #334a45;
            --perio-muted: #6a7f79;
            --perio-green: #24705e;
            --perio-green-dark: #195446;
            --perio-mint: #dcebe5;
            --perio-surface: #ffffff;
            --perio-bg: #f5f7f5;
            --perio-line: #dce4e0;
        }

        html, body, [class*="css"] {
            color: var(--perio-text);
            font-family: Inter, ui-sans-serif, -apple-system,
                BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 88% 2%,
                    rgba(196, 222, 211, .30),
                    transparent 23rem
                ),
                var(--perio-bg);
        }

        [data-testid="stHeader"] {
            background: rgba(245, 247, 245, .88);
            border-bottom: 1px solid rgba(220, 228, 224, .75);
            backdrop-filter: blur(10px);
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1240px;
            padding-top: 2.25rem;
            padding-bottom: 4rem;
        }

        [data-testid="stSidebar"] {
            background: #eef3f0;
            border-right: 1px solid var(--perio-line);
        }

        h1, h2, h3 {
            color: var(--perio-ink);
            letter-spacing: -.025em;
        }

        .perio-brand {
            padding: .35rem .15rem 1rem;
        }

        .perio-brand__mark {
            align-items: center;
            background: var(--perio-green-dark);
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(25, 84, 70, .16);
            color: white;
            display: flex;
            font-size: .82rem;
            font-weight: 800;
            height: 2.55rem;
            justify-content: center;
            margin-bottom: .8rem;
            width: 2.55rem;
        }

        .perio-brand__name {
            color: var(--perio-ink);
            font-size: 1.05rem;
            font-weight: 750;
        }

        .perio-brand__caption,
        .perio-muted {
            color: var(--perio-muted);
            font-size: .79rem;
            line-height: 1.5;
        }

        .perio-case {
            border-top: 1px solid var(--perio-line);
            margin-top: 1rem;
            padding-top: 1rem;
        }

        .perio-case__label,
        .perio-eyebrow,
        .perio-result__eyebrow {
            color: var(--perio-green);
            font-size: .70rem;
            font-weight: 800;
            letter-spacing: .1em;
            text-transform: uppercase;
        }

        .perio-case__value {
            color: var(--perio-ink);
            font-size: .92rem;
            font-weight: 750;
            margin: .25rem 0;
            overflow-wrap: anywhere;
        }

        .perio-hero {
            border-bottom: 1px solid var(--perio-line);
            margin-bottom: 1.25rem;
            padding: .35rem 0 1.45rem;
        }

        .perio-hero h1 {
            color: var(--perio-ink);
            font-size: clamp(2rem, 4vw, 3.05rem);
            line-height: 1.06;
            margin: .55rem 0 0;
            max-width: 940px;
        }

        .perio-hero p {
            color: var(--perio-muted);
            font-size: 1.02rem;
            margin: .75rem 0 0;
            max-width: 820px;
        }

        .perio-flow {
            display: grid;
            gap: .55rem;
            grid-template-columns: repeat(3, 1fr);
            margin: 0 0 1.35rem;
        }

        .perio-flow__step {
            align-items: center;
            background: rgba(255, 255, 255, .72);
            border: 1px solid var(--perio-line);
            border-radius: 12px;
            color: var(--perio-muted);
            display: flex;
            font-size: .82rem;
            font-weight: 650;
            gap: .65rem;
            min-height: 3.2rem;
            padding: .65rem .75rem;
        }

        .perio-flow__step span {
            align-items: center;
            background: #e9efec;
            border-radius: 50%;
            display: inline-flex;
            flex: 0 0 1.7rem;
            font-size: .72rem;
            height: 1.7rem;
            justify-content: center;
        }

        .perio-flow__step.is-active {
            background: var(--perio-mint);
            border-color: #a9c9bc;
            color: var(--perio-ink);
        }

        .perio-flow__step.is-active span {
            background: var(--perio-green-dark);
            color: white;
        }

        .perio-status,
        .perio-result,
        .perio-summary {
            background: rgba(255, 255, 255, .94);
            border: 1px solid var(--perio-line);
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(23, 53, 47, .045);
            min-height: 100%;
            padding: 1rem 1.1rem;
        }

        .perio-status {
            border-left: 4px solid #78908a;
        }

        .perio-status.is-complete {
            border-left-color: #43816f;
        }

        .perio-status.is-na {
            border-left-color: #c08a3f;
        }

        .perio-status.is-warning {
            border-left-color: #c08a3f;
        }

        .perio-status__state {
            color: var(--perio-muted);
            font-size: .67rem;
            font-weight: 780;
            letter-spacing: .07em;
            text-transform: uppercase;
        }

        .perio-status__title {
            color: var(--perio-ink);
            font-size: .94rem;
            font-weight: 760;
            margin-top: .2rem;
        }

        .perio-status__value {
            color: var(--perio-text);
            font-size: .79rem;
            line-height: 1.45;
            margin-top: .32rem;
        }

        .perio-result {
            border-radius: 16px;
            margin: 1rem 0;
            padding: 1.2rem 1.3rem;
        }

        .perio-result__title {
            color: var(--perio-ink);
            font-size: 1.12rem;
            font-weight: 780;
            margin: .3rem 0 .9rem;
        }

        .perio-result__grid {
            display: grid;
            gap: .7rem;
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .perio-result-card {
            background: #f7f9f8;
            border: 1px solid #d8e2de;
            border-left: 4px solid #43816f;
            border-radius: 11px;
            min-width: 0;
            padding: .8rem .9rem;
        }

        .perio-result-card.is-warning {
            border-left-color: #c08a3f;
        }

        .perio-result-card__label {
            color: var(--perio-muted);
            font-size: .67rem;
            font-weight: 760;
            letter-spacing: .07em;
            text-transform: uppercase;
        }

        .perio-result-card__value {
            color: var(--perio-ink);
            font-size: 1.12rem;
            font-weight: 790;
            line-height: 1.3;
            margin-top: .22rem;
            overflow-wrap: anywhere;
        }

        .perio-report-header {
            align-items: flex-start;
            background: var(--perio-ink);
            border-radius: 16px;
            color: #e8f1ed;
            display: flex;
            gap: 1.2rem;
            justify-content: space-between;
            margin: .8rem 0 1.2rem;
            padding: 1.25rem 1.4rem;
        }

        .perio-report-header__label {
            color: #a9c9bc;
            font-size: .69rem;
            font-weight: 800;
            letter-spacing: .1em;
            text-transform: uppercase;
        }

        .perio-report-header__title {
            color: white;
            font-size: 1.28rem;
            font-weight: 780;
            margin-top: .25rem;
        }

        .perio-report-header__meta {
            color: #bed2ca;
            display: flex;
            flex-wrap: wrap;
            font-size: .78rem;
            gap: .35rem 1rem;
            margin-top: .45rem;
        }

        .perio-report-header__count {
            background: rgba(255, 255, 255, .1);
            border: 1px solid rgba(255, 255, 255, .16);
            border-radius: 12px;
            color: white;
            flex: 0 0 auto;
            font-size: 1.4rem;
            font-weight: 800;
            min-width: 8rem;
            padding: .7rem .9rem;
            text-align: center;
        }

        .perio-report-header__count span {
            color: #bed2ca;
            display: block;
            font-size: .68rem;
            font-weight: 650;
            margin-top: .1rem;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, .90);
            border-color: var(--perio-line);
            border-radius: 14px;
            box-shadow: 0 8px 28px rgba(23, 53, 47, .035);
        }

        div[data-testid="stButton"] button,
        div[data-testid="stFormSubmitButton"] button,
        div[data-testid="stDownloadButton"] button {
            border-color: var(--perio-green-dark) !important;
            border-radius: 10px;
            font-weight: 700;
            min-height: 2.7rem;
        }

        div[data-testid="stButton"] button[kind="primary"],
        div[data-testid="stFormSubmitButton"] button[kind="primary"],
        div[data-testid="stDownloadButton"] button[kind="primary"] {
            background: var(--perio-green-dark) !important;
            box-shadow: 0 6px 16px rgba(25, 84, 70, .14);
            color: white !important;
        }

        div[data-testid="stButton"] button[kind="primary"]:hover,
        div[data-testid="stFormSubmitButton"] button[kind="primary"]:hover,
        div[data-testid="stDownloadButton"] button[kind="primary"]:hover {
            background: #123f35 !important;
            border-color: #123f35 !important;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-baseweb="select"] > div,
        [data-testid="stFileUploaderDropzone"] {
            background: #fbfcfb;
            border-color: #cbd8d2;
            border-radius: 9px;
        }

        [data-testid="stAlert"],
        [data-testid="stExpander"] {
            border-radius: 11px;
        }

        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, .68);
            border-color: var(--perio-line);
        }

        div[role="radiogroup"] label:has(input:checked) {
            color: var(--perio-green-dark);
            font-weight: 750;
        }

        hr {
            border-color: var(--perio-line) !important;
        }

        @media (max-width: 760px) {
            [data-testid="stMainBlockContainer"] {
                padding-top: 1.4rem;
            }

            .perio-flow,
            .perio-result__grid {
                grid-template-columns: 1fr;
            }

            .perio-report-header {
                display: block;
            }

            .perio-report-header__count {
                margin-top: .85rem;
                width: 100%;
            }

            .perio-hero h1 {
                font-size: 2.05rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


# INICIALIZA OS DICIONÁRIOS DO SESSION_STATE
inicializar_session_state()

with st.expander("Validação técnica por planilha"):
    mostrar_validacao()

dados_caso = st.session_state["dados_caso"]
dados_clinicos = st.session_state["dados_clinicos"]

dados_caso_preenchidos = (dados_caso["codigo"] is not None) #recebe se o codigo do caso ja foi preenchido
dados_clinicos_preenchidos = (dados_caso["codigo"] is not None)

st.markdown(
    """
    <section class="perio-hero">
        <div class="perio-eyebrow">Apoio à decisão clínica</div>
        <h1>Uma jornada clara, do caso ao relatório.</h1>
        <p>
            Organize a avaliação periodontal, a análise radiográfica e os
            fatores de risco sistêmico em um único fluxo de trabalho.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)


if dados_caso_preenchidos and dados_clinicos_preenchidos: #veirifica se o codigo do caso ja foi preenchido
    classe_etapa_um = "perio-flow__step"                  #pro card que mostra a situação atual do fluxo atualizar
    classe_etapa_dois = "perio-flow__step is-active"      #(somente detalhe visual)

else:
    classe_etapa_um = "perio-flow__step is-active"
    classe_etapa_dois = "perio-flow__step"

st.markdown(
    f"""
    <div class="perio-flow">
        <div class="{classe_etapa_um}"><span>1</span>Preparação do caso</div>
        <div class="{classe_etapa_dois}"><span>2</span>Avaliações</div>
        <div class="perio-flow__step"><span>3</span>Revisão e relatório</div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander(
    "1. Informações compartilhadas do caso", #caso o codigo tenha sido informado, uma proxima interação ira fechar o expander
    expanded=not (dados_caso_preenchidos and dados_clinicos_preenchidos)
):

    
    with st.form("form_dados_compartilhados"): #tudo dentro do with fica armazenado dentro do formulario

        st.markdown("#### Identificação segura")
        coluna_codigo, coluna_idade, coluna_sexo = st.columns([1.5, 1, 1]) #cria 3 colunas já com a largura especifica para cada uma 
                                                                           #essas 3 colunas serão a largura dos inputs dentro do form
        with coluna_codigo:
            codigo_digitado = st.text_input(
                "Código não identificável do caso:",
                value=dados_caso["codigo"] or "",
                placeholder="Exemplo: CASO_001"
            )

        with coluna_idade:
            idade_digitada = st.number_input(
                "Idade:",
                min_value=1,
                max_value=120,
                value=dados_caso["idade"],
                step=1,
                placeholder="Não informado"
            )

        with coluna_sexo:  
            opcoes_sexo = [None, "Feminino", "Masculino"]   #usamos o conceito de indice nao só aqui, mas em todo
            indice_sexo = 0                                 #input objetivo (marcar opcao), para que seja salvo a resposta
                                                            #mesmo que o usuario va para outro modulo, o index manda qual opcao estará assinalada            
            if dados_caso["sexo"] in opcoes_sexo:
                indice_sexo = opcoes_sexo.index(dados_caso["sexo"])

            sexo_digitado = st.selectbox(
                "Sexo:",
                opcoes_sexo,
                index=indice_sexo,
                format_func=lambda opcao: opcao or "Não informado"
            )

        st.markdown("#### Dados clínicos e antropométricos")
        coluna_antropometria, coluna_medidas, coluna_historico = st.columns(3)

        with coluna_antropometria:
            peso_digitado = st.number_input(
                "Peso (kg):",
                min_value=1.0,
                max_value=300.0,
                value=dados_clinicos["peso"],
                step=0.1,
                placeholder="Não informado"
            )

            altura_digitada = st.number_input(
                "Altura (m):",
                min_value=0.5,
                max_value=2.5,
                value=dados_clinicos["altura"],
                step=0.01,
                placeholder="Não informado"
            )

            if peso_digitado is not None and altura_digitada is not None:
                imc_previo = round(
                    peso_digitado / (altura_digitada ** 2), #salva esse imc previo apenas para mostrar, depois ele é apagado e imc é salvo no dicionario
                    2
                )
                st.caption(f"IMC calculado: {imc_previo} kg/m²")

        with coluna_medidas:
            cintura_digitada = st.number_input(
                "Circunferência da cintura (cm):",
                min_value=20.0,
                max_value=250.0,
                value=dados_clinicos["cintura"], # value nao salva nenhum valor, apenas mostra o ultimo salvo, como o index
                step=0.1,
                placeholder="Não informado"
            )

            quadril_digitado = st.number_input(
                "Circunferência do quadril (cm):",
                min_value=20.0,
                max_value=250.0,
                value=dados_clinicos["quadril"],
                step=0.1,
                placeholder="Não informado"
            )

            if cintura_digitada is not None and quadril_digitado is not None:
                st.caption(
                    "Relação cintura-quadril calculada: "
                    f"{cintura_digitada / quadril_digitado:.3f}"
                )

        with coluna_historico:
            opcoes_diabetes = [None, "Sim", "Não", "Não sabe"]
            indice_diabetes = 0

            if dados_clinicos["diabetes"] in opcoes_diabetes:
                indice_diabetes = opcoes_diabetes.index(
                    dados_clinicos["diabetes"]
                )

            diabetes_digitado = st.selectbox(
                "Possui diabetes diagnosticado?",
                opcoes_diabetes,
                index=indice_diabetes,
                format_func=lambda opcao: opcao or "Não informado"
            )

            opcoes_tabagismo = [
                None,
                "Nunca fumou",
                "Ex-fumante há mais de 12 meses",
                "Ex-fumante há 12 meses ou menos",
                "Fumante atual"
            ]
            indice_tabagismo = 0

            if dados_clinicos["tabagismo"] in opcoes_tabagismo:
                indice_tabagismo = opcoes_tabagismo.index(
                    dados_clinicos["tabagismo"]
                )

            tabagismo_digitado = st.selectbox(
                "Situação de tabagismo:",
                opcoes_tabagismo,
                index=indice_tabagismo,
                format_func=lambda opcao: opcao or "Não informado"
            )

            cigarros_dia_digitado = st.number_input(
                "Média de cigarros por dia (atual ou antes de parar):",
                min_value=0,
                max_value=100,
                value=dados_clinicos["cigarros_dia"],
                step=1,
                placeholder="Não informado",
                
            )

        coluna_salvar, coluna_limpar = st.columns(2)

        with coluna_salvar:
            salvar_dados = st.form_submit_button(
                "Salvar dados compartilhados e continuar",
                type="primary",
                width="stretch"
            )

        with coluna_limpar:
            limpar_dados = st.form_submit_button(
                "Limpar dados e iniciar nova avaliação",
                width="stretch"
            )


# A limpeza completa acontece somente quando o usuário pede.
if limpar_dados:
    st.session_state.clear()
    inicializar_session_state()
    st.session_state["mensagem_limpeza"] = (
        "Dados apagados. Uma nova avaliação pode ser iniciada."
    )
    st.rerun()


if "mensagem_limpeza" in st.session_state:
    st.success(st.session_state.pop("mensagem_limpeza"))


#coloca todos os dados do formulario dentro do dados_caso
if salvar_dados:

    if codigo_digitado.strip() == "": #evita a colocar "  "
        st.error("Digite o código do caso.")

    else:
        novo_codigo = codigo_digitado.strip()

        resultado_findrisc_anterior = st.session_state["avaliacao"]["findrisc"]
        resultado_interheart_anterior = (
            st.session_state["avaliacao"]["interheart"]
        )

        dados_compartilhados_alterados = (
            idade_digitada != st.session_state["dados_caso"]["idade"]
            or sexo_digitado != st.session_state["dados_caso"]["sexo"]
            or peso_digitado != st.session_state["dados_clinicos"]["peso"]
            or altura_digitada != st.session_state["dados_clinicos"]["altura"]
            or cintura_digitada != st.session_state["dados_clinicos"]["cintura"]
            or quadril_digitado != st.session_state["dados_clinicos"]["quadril"]
            or diabetes_digitado
            != st.session_state["dados_clinicos"]["diabetes"]
            or tabagismo_digitado
            != st.session_state["dados_clinicos"]["tabagismo"]
            or cigarros_dia_digitado
            != st.session_state["dados_clinicos"]["cigarros_dia"]
        )

        st.session_state["dados_caso"]["codigo"] = novo_codigo
        st.session_state["dados_caso"]["idade"] = idade_digitada
        st.session_state["dados_caso"]["sexo"] = sexo_digitado

        imc = None #salva imc, e nao imc_previo

        if peso_digitado is not None and altura_digitada is not None:
            imc = round(peso_digitado / (altura_digitada ** 2),2)

        st.session_state["dados_clinicos"]["peso"] = peso_digitado
        st.session_state["dados_clinicos"]["altura"] = altura_digitada
        st.session_state["dados_clinicos"]["cintura"] = cintura_digitada
        st.session_state["dados_clinicos"]["quadril"] = quadril_digitado
        st.session_state["dados_clinicos"]["imc"] = imc
        st.session_state["dados_clinicos"]["diabetes"] = diabetes_digitado
        st.session_state["dados_clinicos"]["tabagismo"] = tabagismo_digitado

        # Salva o valor informado sem presumir ausência de consumo.
        st.session_state["dados_clinicos"]["cigarros_dia"] = (cigarros_dia_digitado)

        # Como idade ou sexo podem ter mudado,
        # os resultados que dependem desses dados
        # precisam ser calculados novamente
        #os dados clínicos compartilhados são utilizados
        #por diferentes módulos. Por isso, resultados
        #anteriores precisam ser recalculados.
        if dados_compartilhados_alterados:
            st.session_state["avaliacao"]["findrisc"] = None
            st.session_state["avaliacao"]["interheart"] = None
            st.session_state["avaliacao"]["periodontal"] = None

        # Se um escore já havia sido avaliado, a invalidação também registra
        # quando os novos dados passaram a ser insuficientes.
        if (
            dados_compartilhados_alterados
            and resultado_findrisc_anterior is not None
        ):
            dados_ausentes_findrisc = []

            if diabetes_digitado is None:
                dados_ausentes_findrisc.append("Situação de diabetes")

            if idade_digitada is None:
                dados_ausentes_findrisc.append("Idade")

            if sexo_digitado is None:
                dados_ausentes_findrisc.append("Sexo")

            if imc is None:
                dados_ausentes_findrisc.append("IMC")

            if cintura_digitada is None:
                dados_ausentes_findrisc.append("Circunferência da cintura")

            campos_findrisc = {
                "atividade_fisica": "Atividade física",
                "frutas_vegetais": "Consumo diário de frutas ou vegetais",
                "medicacao_pressao": "Uso de medicamento para pressão alta",
                "glicemia_elevada": "Histórico de glicemia elevada",
                "historico_familiar": "Histórico familiar de diabetes"
            }

            for campo, nome_campo in campos_findrisc.items():
                if st.session_state["dados_findrisc"][campo] is None:
                    dados_ausentes_findrisc.append(nome_campo)

            if (
                diabetes_digitado != "Sim"
                and len(dados_ausentes_findrisc) > 0
            ):
                st.session_state["avaliacao"]["findrisc"] = {
                    "status": "dados_insuficientes",
                    "dados_ausentes": dados_ausentes_findrisc
                }

        if (
            dados_compartilhados_alterados
            and resultado_interheart_anterior is not None
        ):
            dados_ausentes_interheart = []
            dados_invalidos_interheart = []

            campos_compartilhados_interheart = [
                (idade_digitada, "Idade"),
                (sexo_digitado, "Sexo"),
                (cintura_digitada, "Circunferência da cintura"),
                (quadril_digitado, "Circunferência do quadril"),
                (diabetes_digitado, "Situação de diabetes"),
                (tabagismo_digitado, "Situação de tabagismo")
            ]

            for valor, nome_campo in campos_compartilhados_interheart:
                if valor is None:
                    dados_ausentes_interheart.append(nome_campo)

            if tabagismo_digitado in [
                "Fumante atual",
                "Ex-fumante há 12 meses ou menos"
            ]:
                if cigarros_dia_digitado is None:
                    dados_ausentes_interheart.append("Média de cigarros por dia")

                elif cigarros_dia_digitado == 0:
                    dados_invalidos_interheart.append(
                        "Média de cigarros por dia incompatível com o tabagismo"
                    )

            campos_interheart = {
                "hipertensao": "Situação de hipertensão",
                "historico_parental_infarto": "Histórico parental de infarto",
                "estresse": "Situação de estresse",
                "fumo_passivo": "Exposição ao fumo passivo",
                "atividade_lazer": "Atividade física no lazer",
                "tristeza_depressao": "Tristeza ou depressão",
                "alimento_salgado": "Consumo de alimentos salgados",
                "fritura_fast_food": "Consumo de fritura ou fast-food",
                "fruta_diaria": "Consumo diário de frutas",
                "vegetais_diarios": "Consumo diário de vegetais",
                "carne_aves": "Consumo de carne ou aves"
            }

            for campo, nome_campo in campos_interheart.items():
                if st.session_state["dados_interheart"][campo] is None:
                    dados_ausentes_interheart.append(nome_campo)

            if (
                len(dados_ausentes_interheart) > 0
                or len(dados_invalidos_interheart) > 0
            ):
                st.session_state["avaliacao"]["interheart"] = {
                    "status": "dados_insuficientes",
                    "dados_ausentes": dados_ausentes_interheart,
                    "dados_invalidos": dados_invalidos_interheart
                }

        st.success("Dados compartilhados salvos. Escolha um módulo para continuar.")


st.markdown("## Estado da avaliação")


estado_periodontal = "Pendente"
texto_periodontal = "Aguardando classificação."
classe_periodontal = "perio-status"

if st.session_state["avaliacao"]["periodontal"] is not None:
    if "classificacao_final" in st.session_state["avaliacao"]["periodontal"]:
        estado_periodontal = "Concluído"
        texto_periodontal = st.session_state["avaliacao"]["periodontal"]["classificacao_final"]
        classe_periodontal = "perio-status is-complete"

        if st.session_state["avaliacao"]["periodontal"].get(
            "classificacao_provisoria",
            False
        ):
            estado_periodontal = "Provisório"
            classe_periodontal = "perio-status is-warning"

    elif st.session_state["avaliacao"]["periodontal"].get("status") == ("dados_insuficientes"):
        estado_periodontal = "Dados insuficientes"
        texto_periodontal = "Não foi possível concluir estágio e grau."
        classe_periodontal = "perio-status is-warning"

estado_findrisc = "Pendente"
texto_findrisc = "Aguardando cálculo."
classe_findrisc = "perio-status"

if st.session_state["dados_clinicos"]["diabetes"] == "Sim":
    estado_findrisc = "Não aplicável"
    texto_findrisc = "Diabetes já diagnosticado."
    classe_findrisc = "perio-status is-na"

elif (
    st.session_state["avaliacao"]["findrisc"] is not None
    and "pontos" in st.session_state["avaliacao"]["findrisc"]
):
    estado_findrisc = "Concluído"
    texto_findrisc = st.session_state["avaliacao"]["findrisc"]["classificacao"]
    classe_findrisc = "perio-status is-complete"

elif (
    st.session_state["avaliacao"]["findrisc"] is not None
    and st.session_state["avaliacao"]["findrisc"].get("status")
    == "dados_insuficientes"
):
    estado_findrisc = "Dados insuficientes"
    texto_findrisc = "Preencha as informações indicadas no módulo."
    classe_findrisc = "perio-status is-warning"

estado_interheart = "Pendente"
texto_interheart = "Aguardando cálculo."
classe_interheart = "perio-status"

if (
    st.session_state["avaliacao"]["interheart"] is not None
    and "pontos" in st.session_state["avaliacao"]["interheart"]
):
    estado_interheart = "Concluído"
    texto_interheart = st.session_state["avaliacao"]["interheart"]["classificacao"]
    classe_interheart = "perio-status is-complete"

elif (
    st.session_state["avaliacao"]["interheart"] is not None
    and st.session_state["avaliacao"]["interheart"].get("status")
    == "dados_insuficientes"
):
    estado_interheart = "Dados insuficientes"
    texto_interheart = "Preencha as informações indicadas no módulo."
    classe_interheart = "perio-status is-warning"

coluna_periodontal, coluna_findrisc, coluna_interheart = st.columns(3)

for coluna, classe, estado, titulo, texto_estado in [
    (
        coluna_periodontal,
        classe_periodontal,
        estado_periodontal,
        "AAP/EFP 2018",
        texto_periodontal
    ),
    (
        coluna_findrisc,
        classe_findrisc,
        estado_findrisc,
        "FINDRISC",
        texto_findrisc
    ),
    (
        coluna_interheart,
        classe_interheart,
        estado_interheart,
        "INTERHEART",
        texto_interheart
    )
]:
    with coluna:
        st.markdown(
            f"""
            <div class="{classe}">
                <div class="perio-status__state">{escape(estado)}</div>
                <div class="perio-status__title">{escape(titulo)}</div>
                <div class="perio-status__value">{escape(str(texto_estado))}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("## Área de trabalho")
opcoes_modulos = [
    "Análise radiográfica",
    "Classificação periodontal",
    "FINDRISC",
    "INTERHEART",
    "Relatório"
]
modulo = st.radio(
    "Módulo em edição",
    opcoes_modulos,
    horizontal=True,
    key="modulo_navegacao"
)

# EXIBIÇÃO DOS MÓDULOS

with st.container(border=True):

    if modulo == "Análise radiográfica":
        mostrar_modulo_radiografico()

    elif modulo == "Classificação periodontal":
        mostrar_modulo_periodontal()

    elif modulo == "FINDRISC":
        mostrar_findrisc()

    elif modulo == "INTERHEART":
        mostrar_interheart()

    elif modulo == "Relatório":
        mostrar_relatorio()


with st.expander("Limites de uso e responsabilidade profissional"):
    st.caption(
        "Este sistema é uma ferramenta de apoio. Os resultados organizam "
        "informações a partir de critérios e escores publicados, mas não "
        "substituem a interpretação nem a decisão do profissional habilitado."
    )
