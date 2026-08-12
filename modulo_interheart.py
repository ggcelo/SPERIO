import streamlit as st


def mostrar_interheart():
    st.subheader("INTERHEART")

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


            # Como os dados utilizados no cálculo mudaram,
            # o resultado anterior do INTERHEART deve ser recalculado
            st.session_state["avaliacao"]["interheart"] = None
            st.success("Dados do INTERHEART salvos.")

    
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
            or (
                    tabagismo in [
                        "Fumante atual",
                        "Ex-fumante há 12 meses ou menos"
                    ]
                    and cigarros_dia is None
                )
                or None in dados_interheart.values()
            ):
        
            st.error(
                "Preencha e salve todos os dados necessários "
                "antes de calcular o INTERHEART."
            )   
        else:

            # Calcula a relação cintura-quadril sem arredondar.
            # Esse valor será utilizado para determinar a pontuação.
            rcq_calculo = cintura / quadril


            # Cria uma versão arredondada somente para
            # apresentar o resultado ao usuário.
            rcq = round(rcq_calculo, 3)

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


            elif tabagismo in [
                "Fumante atual",
                "Ex-fumante há 12 meses ou menos"
            ]:

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
            # Utilizamos o valor sem arredondamento para
            # não alterar a classificação perto dos limites.
            if rcq_calculo < 0.873:
                pontos_itens["rcq"] = 0

            elif rcq_calculo < 0.964:
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
