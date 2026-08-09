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


    # INTERHEART
    texto_relatorio += (
        "\n"
        "INTERHEART\n"
        f"Pontuação: {resultado_interheart['pontos']}\n"
        f"Classificação: {resultado_interheart['classificacao']}\n"
        f"Relação cintura-quadril: "
        f"{resultado_interheart['rcq']}\n"
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


else:

    st.warning(
        "O relatório final só poderá ser preparado "
        "quando a avaliação estiver completa."
    )
