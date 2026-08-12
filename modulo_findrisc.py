import streamlit as st


def mostrar_findrisc():
    st.subheader("FINDRISC")

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

            # Como os dados utilizados no cálculo mudaram,
            # o resultado anterior do FINDRISC deve ser recalculado
            st.session_state["avaliacao"]["findrisc"] = None

            st.success("Dados do FINDRISC salvos.")

    if st.button("Calcular FINDRISC"):

        idade = st.session_state["dados_caso"]["idade"]
        sexo = st.session_state["dados_caso"]["sexo"]

        imc = st.session_state["dados_clinicos"]["imc"]
        cintura = st.session_state["dados_clinicos"]["cintura"]
        diabetes = st.session_state["dados_clinicos"]["diabetes"]

        dados_findrisc = st.session_state["dados_findrisc"]

        if diabetes == "Sim":

            st.session_state["avaliacao"]["findrisc"] = None

            st.warning( 
                "O FINDRISC não é aplicado porque o caso possui "
                "diabetes já diagnosticado."
            )

        elif (
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

            elif imc <= 30:
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
