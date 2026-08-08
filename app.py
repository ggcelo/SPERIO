import streamlit as st


st.set_page_config(
    page_title="Apoio à Decisão em Periodontia",
    page_icon="🦷",
    layout="wide"
)


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

#resultados
if "avaliacao" not in st.session_state: 
    st.session_state["avaliacao"] = {
        "periodontal": None,
        "findrisc": None,
        "interheart": None,
        "pbl": None
    }

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
    st.session_state["avaliacao"]["pbl"] = 0
    st.rerun()

#inputs
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

if "dados_clinicos" not in st.session_state:
    st.session_state["dados_clinicos"] = {
        "peso": None,
        "altura": None,
        "cintura": None,
        "imc": None
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

    else:
        imc = round(
            peso_digitado / (altura_digitada ** 2),
            2
        )

        st.session_state["dados_clinicos"]["peso"] = peso_digitado
        st.session_state["dados_clinicos"]["altura"] = altura_digitada
        st.session_state["dados_clinicos"]["cintura"] = cintura_digitada
        st.session_state["dados_clinicos"]["imc"] = imc

        st.success("Dados clínicos salvos.")


st.write(
    "Dados clínicos salvos:",
    st.session_state["dados_clinicos"]
)