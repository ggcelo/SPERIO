from html import escape
from pathlib import Path

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
    layout="wide",
    initial_sidebar_state="expanded"
)


# Estilos compartilhados por todos os módulos, sem dependências externas.
st.markdown(
    "<style>" + Path(__file__).with_name("interface.css").read_text(encoding="utf-8")
    + "</style>",
    unsafe_allow_html=True
)


st.markdown(
    """
    <header class="perio-heading">
        <h1>SPERIO</h1>
        <p>
            Classificação AAP/EFP, análise radiográfica e escores de risco sistêmico.
            Preencha os dados do caso e selecione a avaliação que deseja realizar.
        </p>
    </header>
    """,
    unsafe_allow_html=True
)


# INICIALIZA OS DICIONÁRIOS DO SESSION_STATE
inicializar_session_state()

with st.sidebar:
    st.markdown("SPERIO")
    navegacao_lateral = st.empty()
    st.divider()
    with st.expander("Validação técnica por planilha"):
        mostrar_validacao()

dados_caso = st.session_state["dados_caso"]
dados_clinicos = st.session_state["dados_clinicos"]

dados_caso_preenchidos = (dados_caso["codigo"] is not None) #recebe se o codigo do caso ja foi preenchido
dados_clinicos_preenchidos = (dados_caso["codigo"] is not None)

with st.expander(
    "Dados compartilhados do caso", #caso o codigo tenha sido informado, uma proxima interação ira fechar o expander
    expanded=not (dados_caso_preenchidos and dados_clinicos_preenchidos)
):

    
    with st.form("form_dados_compartilhados"): #tudo dentro do with fica armazenado dentro do formulario

        st.markdown("#### Identificação do caso")
        coluna_codigo, coluna_idade, coluna_sexo = st.columns(
            [1.5, 1, 1], gap="large"
        )
        with coluna_codigo:
            codigo_digitado = st.text_input(
                "Código não identificável do caso:",
                value=dados_caso["codigo"] or "",
                placeholder="Informe o código do caso"
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

        st.markdown("#### Medidas antropométricas")
        coluna_antropometria, coluna_medidas = st.columns(2, gap="large")

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

        st.markdown("#### Histórico clínico")
        with st.container():
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

        coluna_salvar, coluna_limpar = st.columns(2, gap="large")

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


opcoes_modulos = [
    "Análise radiográfica",
    "Classificação periodontal",
    "FINDRISC",
    "INTERHEART",
    "Relatório"
]
with navegacao_lateral.container():
    modulo = st.radio(
        "Avaliações",
        opcoes_modulos,
        key="modulo_navegacao"
    )

# EXIBIÇÃO DOS MÓDULOS

with st.container(key="area_avaliacao"):

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


if modulo != "Relatório":
    with st.container(key="resumo_avaliacoes"):
        st.markdown("### Situação das avaliações")


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

        itens_estado = [
            (classe_periodontal, estado_periodontal, "AAP/EFP 2018", texto_periodontal),
            (classe_findrisc, estado_findrisc, "FINDRISC", texto_findrisc),
            (classe_interheart, estado_interheart, "INTERHEART", texto_interheart)
        ]
        linhas_estado = "".join(
            f'<div class="{classe}" role="listitem">'
            f'<div class="perio-status__title">{escape(titulo)}</div>'
            f'<div class="perio-status__value">{escape(str(texto_estado))}</div>'
            f'<div class="perio-status__state">{escape(estado)}</div>'
            '</div>'
            for classe, estado, titulo, texto_estado in itens_estado
        )
        st.markdown(
            f'<div class="perio-status-list" role="list">{linhas_estado}</div>',
            unsafe_allow_html=True
        )


with st.expander("Limites de uso e responsabilidade profissional"):
    st.caption(
        "Este sistema é uma ferramenta de apoio. Os resultados organizam "
        "informações a partir de critérios e escores publicados, mas não "
        "substituem a interpretação nem a decisão do profissional habilitado."
    )
