from html import escape

import streamlit as st


def mostrar_interheart():
    st.header("INTERHEART não laboratorial")
    st.write(
        "Organize os fatores associados ao risco cardiovascular usando os "
        "dados compartilhados e as perguntas específicas abaixo."
    )

    idade = st.session_state["dados_caso"]["idade"]
    sexo = st.session_state["dados_caso"]["sexo"]
    cintura = st.session_state["dados_clinicos"]["cintura"]
    quadril = st.session_state["dados_clinicos"]["quadril"]
    diabetes = st.session_state["dados_clinicos"]["diabetes"]
    tabagismo = st.session_state["dados_clinicos"]["tabagismo"]
    cigarros_dia = st.session_state["dados_clinicos"]["cigarros_dia"]

    st.markdown("#### Dados compartilhados utilizados")
    coluna_idade, coluna_tabagismo, coluna_rcq = st.columns(3)

    with coluna_idade:
        st.metric("Idade", f"{idade} anos" if idade is not None else "Pendente")

    with coluna_tabagismo:
        st.metric("Tabagismo", tabagismo or "Pendente")

    with coluna_rcq:
        if cintura is not None and quadril is not None:
            rcq_previa = cintura / quadril
            st.metric("Relação cintura-quadril", f"{rcq_previa:.3f}")

        else:
            st.metric("Relação cintura-quadril", "Pendente")

    dados_anteriores = st.session_state["dados_interheart"]
    opcoes_sim_nao = [None, "Sim", "Não"]

    with st.form("form_interheart"):
        st.markdown("#### Perguntas específicas do INTERHEART")
        coluna_um, coluna_dois = st.columns(2)

        with coluna_um:
            opcoes_resposta = [None, "Sim", "Não", "Não sabe"]
            indice_hipertensao = 0

            if dados_anteriores["hipertensao"] in opcoes_resposta:
                indice_hipertensao = opcoes_resposta.index(
                    dados_anteriores["hipertensao"]
                )

            hipertensao = st.selectbox(
                "Possui hipertensão/pressão alta diagnosticada?",
                opcoes_resposta,
                index=indice_hipertensao,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_historico = 0

            if dados_anteriores["historico_parental_infarto"] in opcoes_resposta:
                indice_historico = opcoes_resposta.index(
                    dados_anteriores["historico_parental_infarto"]
                )

            historico_parental_infarto = st.selectbox(
                "Pai ou mãe possui histórico de infarto?",
                opcoes_resposta,
                index=indice_historico,
                format_func=lambda opcao: opcao or "Não informado"
            )

            opcoes_estresse = [
                None,
                "Nunca ou em alguns períodos",
                "Vários períodos ou permanente"
            ]
            indice_estresse = 0

            if dados_anteriores["estresse"] in opcoes_estresse:
                indice_estresse = opcoes_estresse.index(
                    dados_anteriores["estresse"]
                )

            estresse = st.selectbox(
                "Estresse no trabalho ou em casa:",
                opcoes_estresse,
                index=indice_estresse,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_fumo_passivo = 0

            if dados_anteriores["fumo_passivo"] in opcoes_sim_nao:
                indice_fumo_passivo = opcoes_sim_nao.index(
                    dados_anteriores["fumo_passivo"]
                )

            fumo_passivo = st.radio(
                "Exposição ao fumo passivo por uma hora ou mais por semana?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_fumo_passivo,
                format_func=lambda opcao: opcao or "Não informado"
            )

            opcoes_atividade = [
                None,
                "Moderada ou intensa",
                "Sedentário ou esforço mínimo"
            ]
            indice_atividade = 0

            if dados_anteriores["atividade_lazer"] in opcoes_atividade:
                indice_atividade = opcoes_atividade.index(
                    dados_anteriores["atividade_lazer"]
                )

            atividade_lazer = st.selectbox(
                "Atividade física no lazer:",
                opcoes_atividade,
                index=indice_atividade,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_tristeza = 0

            if dados_anteriores["tristeza_depressao"] in opcoes_sim_nao:
                indice_tristeza = opcoes_sim_nao.index(
                    dados_anteriores["tristeza_depressao"]
                )

            tristeza_depressao = st.radio(
                "Tristeza ou depressão por duas semanas ou mais?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_tristeza,
                format_func=lambda opcao: opcao or "Não informado"
            )

        with coluna_dois:
            indice_salgado = 0

            if dados_anteriores["alimento_salgado"] in opcoes_sim_nao:
                indice_salgado = opcoes_sim_nao.index(
                    dados_anteriores["alimento_salgado"]
                )

            alimento_salgado = st.radio(
                "Consome alimentos salgados uma ou mais vezes ao dia?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_salgado,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_fritura = 0

            if dados_anteriores["fritura_fast_food"] in opcoes_sim_nao:
                indice_fritura = opcoes_sim_nao.index(
                    dados_anteriores["fritura_fast_food"]
                )

            fritura_fast_food = st.radio(
                "Consome fritura ou fast-food três ou mais vezes por semana?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_fritura,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_fruta = 0

            if dados_anteriores["fruta_diaria"] in opcoes_sim_nao:
                indice_fruta = opcoes_sim_nao.index(
                    dados_anteriores["fruta_diaria"]
                )

            fruta_diaria = st.radio(
                "Consome frutas diariamente?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_fruta,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_vegetais = 0

            if dados_anteriores["vegetais_diarios"] in opcoes_sim_nao:
                indice_vegetais = opcoes_sim_nao.index(
                    dados_anteriores["vegetais_diarios"]
                )

            vegetais_diarios = st.radio(
                "Consome vegetais diariamente?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_vegetais,
                format_func=lambda opcao: opcao or "Não informado"
            )

            indice_carne = 0

            if dados_anteriores["carne_aves"] in opcoes_sim_nao:
                indice_carne = opcoes_sim_nao.index(
                    dados_anteriores["carne_aves"]
                )

            carne_aves = st.radio(
                "Consome carne ou aves duas ou mais vezes ao dia?",
                opcoes_sim_nao,
                horizontal=True,
                index=indice_carne,
                format_func=lambda opcao: opcao or "Não informado"
            )

        calcular_interheart = st.form_submit_button(
            "Calcular INTERHEART",
            type="primary",
            width="stretch"
        )

    if calcular_interheart:
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

        dados_ausentes_interheart = []
        dados_invalidos_interheart = []

        campos_compartilhados = [
            (idade, "Idade"),
            (sexo, "Sexo"),
            (cintura, "Circunferência da cintura"),
            (quadril, "Circunferência do quadril"),
            (diabetes, "Situação de diabetes"),
            (tabagismo, "Situação de tabagismo")
        ]

        for valor, nome_campo in campos_compartilhados:
            if valor is None:
                dados_ausentes_interheart.append(nome_campo)

        if tabagismo in [
            "Fumante atual",
            "Ex-fumante há 12 meses ou menos"
        ]:
            if cigarros_dia is None:
                dados_ausentes_interheart.append("Média de cigarros por dia")

            elif cigarros_dia == 0:
                dados_invalidos_interheart.append(
                    "Média de cigarros por dia incompatível com o tabagismo"
                )

        campos_especificos = [
            (hipertensao, "Situação de hipertensão"),
            (historico_parental_infarto, "Histórico parental de infarto"),
            (estresse, "Situação de estresse"),
            (fumo_passivo, "Exposição ao fumo passivo"),
            (atividade_lazer, "Atividade física no lazer"),
            (tristeza_depressao, "Tristeza ou depressão"),
            (alimento_salgado, "Consumo de alimentos salgados"),
            (fritura_fast_food, "Consumo de fritura ou fast-food"),
            (fruta_diaria, "Consumo diário de frutas"),
            (vegetais_diarios, "Consumo diário de vegetais"),
            (carne_aves, "Consumo de carne ou aves")
        ]

        for valor, nome_campo in campos_especificos:
            if valor is None:
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

            st.warning(
                "Os dados informados foram salvos, mas ainda são "
                "insuficientes para calcular o INTERHEART."
            )

            if len(dados_invalidos_interheart) > 0:
                for dado in dados_invalidos_interheart:
                    st.error(dado + ".")

        else:
            dados_interheart = st.session_state["dados_interheart"]

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
                "status": "concluido",
                "pontos": pontos_total,
                "classificacao": classificacao,
                "rcq": rcq,
                "pontos_itens": pontos_itens
            }

            st.success("INTERHEART calculado com sucesso.")


    resultado_interheart = st.session_state["avaliacao"]["interheart"]


    if (
        resultado_interheart is not None
        and resultado_interheart.get("status") == "dados_insuficientes"
    ):
        st.warning("Dados insuficientes para cálculo.")

        dados_ausentes_interheart = resultado_interheart.get(
            "dados_ausentes",
            []
        )
        dados_invalidos_interheart = resultado_interheart.get(
            "dados_invalidos",
            []
        )

        if len(dados_ausentes_interheart) > 0:
            st.markdown("**Informações ausentes:**")

            for dado in dados_ausentes_interheart:
                st.write("-", dado)

        if len(dados_invalidos_interheart) > 0:
            st.markdown("**Informações incompatíveis:**")

            for dado in dados_invalidos_interheart:
                st.write("-", dado)

    elif resultado_interheart is not None and "pontos" in resultado_interheart:
        classe_resultado = "perio-result-card"

        if resultado_interheart["classificacao"] != "Baixo risco":
            classe_resultado = "perio-result-card is-warning"

        st.markdown(
            f"""
            <section class="perio-result">
                <div class="perio-result__eyebrow">Resultado INTERHEART</div>
                <div class="perio-result__title">
                    Organização não laboratorial do risco cardiovascular
                </div>
                <div class="perio-result__grid">
                    <div class="perio-result-card">
                        <div class="perio-result-card__label">Pontuação</div>
                        <div class="perio-result-card__value">
                            {resultado_interheart['pontos']} pontos
                        </div>
                    </div>
                    <div class="{classe_resultado}">
                        <div class="perio-result-card__label">Classificação</div>
                        <div class="perio-result-card__value">
                            {escape(resultado_interheart['classificacao'])}
                        </div>
                    </div>
                    <div class="perio-result-card">
                        <div class="perio-result-card__label">
                            Relação cintura-quadril
                        </div>
                        <div class="perio-result-card__value">
                            {resultado_interheart['rcq']}
                        </div>
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True
        )

        with st.expander("Ver composição da pontuação"):
            rotulos_itens = {
                "idade_sexo": "Idade e sexo",
                "tabagismo": "Tabagismo",
                "fumo_passivo": "Fumo passivo",
                "diabetes": "Diabetes",
                "hipertensao": "Hipertensão",
                "historico_parental_infarto": "Histórico parental de infarto",
                "rcq": "Relação cintura-quadril",
                "estresse": "Estresse",
                "tristeza_depressao": "Tristeza ou depressão",
                "alimento_salgado": "Alimentos salgados",
                "fritura_fast_food": "Fritura ou fast-food",
                "fruta_diaria": "Consumo de frutas",
                "vegetais_diarios": "Consumo de vegetais",
                "carne_aves": "Consumo de carne ou aves",
                "atividade_lazer": "Atividade física no lazer"
            }

            for chave, pontos in resultado_interheart["pontos_itens"].items():
                st.write(
                    f"**{rotulos_itens[chave]}:** {pontos} "
                    + ("ponto" if pontos == 1 else "pontos")
                )

        st.caption(
            "Instrumento de rastreamento de risco. O resultado não estabelece "
            "diagnóstico médico."
        )
