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
    st.session_state["avaliacao"]["pbl"] = None
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

#dicionario dados clinicos
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

st.divider()

st.subheader("FINDRISC")


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