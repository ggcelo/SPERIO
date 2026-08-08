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

#DICIONÁRIO DOS RESULTADOS

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


        