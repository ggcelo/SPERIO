from html import escape

import streamlit as st


def mostrar_findrisc():
    st.header("FINDRISC")
    st.write(
        "Estime o risco de desenvolvimento de diabetes tipo 2 em 10 anos "
        "a partir dos dados compartilhados e das perguntas abaixo."
    )

    idade = st.session_state["dados_caso"]["idade"]
    sexo = st.session_state["dados_caso"]["sexo"]
    imc = st.session_state["dados_clinicos"]["imc"]
    cintura = st.session_state["dados_clinicos"]["cintura"]
    diabetes = st.session_state["dados_clinicos"]["diabetes"]

    if diabetes == "Sim":
        st.session_state["avaliacao"]["findrisc"] = None
        st.info(
            "FINDRISC não aplicável — diabetes já diagnosticado. "
            "O instrumento estima risco futuro de desenvolvimento de "
            "diabetes tipo 2."
        )
        return

    st.markdown("#### Dados compartilhados utilizados")
    coluna_idade, coluna_imc, coluna_cintura = st.columns(3)

    with coluna_idade:
        st.metric("Idade", f"{idade} anos" if idade is not None else "Pendente")

    with coluna_imc:
        st.metric("IMC", f"{imc} kg/m²" if imc is not None else "Pendente")

    with coluna_cintura:
        st.metric(
            "Cintura",
            f"{cintura} cm" if cintura is not None else "Pendente"
        )

    dados_anteriores = st.session_state["dados_findrisc"]
    opcoes_sim_nao = [None, "Sim", "Não"]

    with st.form("form_findrisc"):
        st.markdown("#### Perguntas específicas do FINDRISC")
        coluna_um, coluna_dois = st.columns(2)

        with coluna_um:
            indice_atividade = 0

            if dados_anteriores["atividade_fisica"] in opcoes_sim_nao:
                indice_atividade = opcoes_sim_nao.index(
                    dados_anteriores["atividade_fisica"]
                )

            atividade_fisica = st.radio(
                "Realiza pelo menos 30 minutos de atividade física por dia?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_atividade,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_frutas = 0

            if dados_anteriores["frutas_vegetais"] in opcoes_sim_nao:
                indice_frutas = opcoes_sim_nao.index(
                    dados_anteriores["frutas_vegetais"]
                )

            frutas_vegetais = st.radio(
                "Consome frutas ou vegetais diariamente?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_frutas,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_pressao = 0

            if dados_anteriores["medicacao_pressao"] in opcoes_sim_nao:
                indice_pressao = opcoes_sim_nao.index(
                    dados_anteriores["medicacao_pressao"]
                )

            medicacao_pressao = st.radio(
                "Já utilizou regularmente medicamento para pressão alta?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_pressao,
                format_func=lambda opcao: opcao or "Não informado"
            )

        with coluna_dois:
            indice_glicemia = 0

            if dados_anteriores["glicemia_elevada"] in opcoes_sim_nao:
                indice_glicemia = opcoes_sim_nao.index(
                    dados_anteriores["glicemia_elevada"]
                )

            glicemia_elevada = st.radio(
                "Alguma vez foi identificada glicemia elevada?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_glicemia,
                format_func=lambda opcao: opcao or "Não informado"
            )

            opcoes_historico = [
                None,
                "Nenhum familiar",
                "Avós, tios ou primos",
                "Pais, irmãos ou filhos"
            ]
            indice_historico = 0

            if dados_anteriores["historico_familiar"] in opcoes_historico:
                indice_historico = opcoes_historico.index(
                    dados_anteriores["historico_familiar"]
                )

            historico_familiar = st.selectbox(
                "Histórico familiar de diabetes:",
                opcoes_historico,
                index=indice_historico,
                format_func=lambda opcao: opcao or "Não informado"
            )

        calcular_findrisc = st.form_submit_button(
            "Calcular FINDRISC",
            type="primary",
            width="stretch"
        )

    if calcular_findrisc:
        st.session_state["dados_findrisc"]["atividade_fisica"] = atividade_fisica
        st.session_state["dados_findrisc"]["frutas_vegetais"] = frutas_vegetais
        st.session_state["dados_findrisc"]["medicacao_pressao"] = medicacao_pressao
        st.session_state["dados_findrisc"]["glicemia_elevada"] = glicemia_elevada
        st.session_state["dados_findrisc"]["historico_familiar"] = historico_familiar

        # Como os dados utilizados no cálculo mudaram,
        # o resultado anterior do FINDRISC deve ser recalculado
        st.session_state["avaliacao"]["findrisc"] = None

        dados_ausentes_findrisc = []

        if diabetes is None:
            dados_ausentes_findrisc.append("Situação de diabetes")

        if idade is None:
            dados_ausentes_findrisc.append("Idade")

        if sexo is None:
            dados_ausentes_findrisc.append("Sexo")

        if imc is None:
            dados_ausentes_findrisc.append("IMC")

        if cintura is None:
            dados_ausentes_findrisc.append("Circunferência da cintura")

        if atividade_fisica is None:
            dados_ausentes_findrisc.append("Atividade física")

        if frutas_vegetais is None:
            dados_ausentes_findrisc.append(
                "Consumo diário de frutas ou vegetais"
            )

        if medicacao_pressao is None:
            dados_ausentes_findrisc.append(
                "Uso de medicamento para pressão alta"
            )

        if glicemia_elevada is None:
            dados_ausentes_findrisc.append("Histórico de glicemia elevada")

        if historico_familiar is None:
            dados_ausentes_findrisc.append("Histórico familiar de diabetes")

        if len(dados_ausentes_findrisc) > 0:
            st.session_state["avaliacao"]["findrisc"] = {
                "status": "dados_insuficientes",
                "dados_ausentes": dados_ausentes_findrisc
            }

            st.warning(
                "Os dados informados foram salvos, mas ainda são "
                "insuficientes para calcular o FINDRISC."
            )

        else:
            dados_findrisc = st.session_state["dados_findrisc"]
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
                "status": "concluido",
                "pontos": pontos,
                "classificacao": classificacao,
                "estimativa": estimativa
            }

            st.success("FINDRISC calculado com sucesso.")

    resultado_findrisc = st.session_state["avaliacao"]["findrisc"]


    if (
        resultado_findrisc is not None
        and resultado_findrisc.get("status") == "dados_insuficientes"
    ):
        st.warning("Dados insuficientes para cálculo.")
        st.markdown("**Informações ausentes:**")

        for dado in resultado_findrisc.get("dados_ausentes", []):
            st.write("-", dado)

    elif resultado_findrisc is not None and "pontos" in resultado_findrisc:
        classe_resultado = "perio-result-card"

        if resultado_findrisc["classificacao"] in ["Alto", "Muito alto"]:
            classe_resultado = "perio-result-card is-warning"

        st.markdown(
            f"""
            <section class="perio-result">
                <div class="perio-result__eyebrow">Resultado FINDRISC</div>
                <div class="perio-result__title">Risco estimado em 10 anos</div>
                <div class="perio-result__grid">
                    <div class="perio-result-card">
                        <div class="perio-result-card__label">Pontuação</div>
                        <div class="perio-result-card__value">
                            {resultado_findrisc['pontos']} pontos
                        </div>
                    </div>
                    <div class="{classe_resultado}">
                        <div class="perio-result-card__label">Classificação</div>
                        <div class="perio-result-card__value">
                            {escape(resultado_findrisc['classificacao'])}
                        </div>
                    </div>
                    <div class="perio-result-card">
                        <div class="perio-result-card__label">Estimativa</div>
                        <div class="perio-result-card__value">
                            {escape(resultado_findrisc['estimativa'])}
                        </div>
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "Instrumento de rastreamento de risco. O resultado não estabelece "
            "diagnóstico médico."
        )
