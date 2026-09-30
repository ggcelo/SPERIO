from html import escape

import streamlit as st


def mostrar_modulo_periodontal():
    st.header("Classificação periodontal AAP/EFP")
    st.write(
        "Informe os critérios clínicos disponíveis. Uma única ação aplica, "
        "na ordem, severidade, complexidade, extensão, progressão e "
        "modificadores."
    )

    # O %PBL já vem da avaliação radiográfica
    pbl = st.session_state["avaliacao"]["pbl"]

    coluna_pbl, coluna_idade = st.columns(2)

    with coluna_pbl:
        if pbl is None:
            st.metric("%PBL radiográfico", "Não informado")

        else:
            st.metric("%PBL radiográfico", f"{pbl:.2f}%")

    # Dados que já foram preenchidos anteriormente
    idade = st.session_state["dados_caso"]["idade"]
    diabetes = st.session_state["dados_clinicos"]["diabetes"]
    tabagismo = st.session_state["dados_clinicos"]["tabagismo"]
    cigarros_dia = st.session_state["dados_clinicos"]["cigarros_dia"]

    with coluna_idade:
        st.metric("Idade", f"{idade} anos" if idade is not None else "Pendente")

    if diabetes is None and tabagismo is None:
        resumo_modificadores = "Não informados"

    else:
        resumo_modificadores = (
            f"Diabetes: {diabetes or '—'} · "
            f"Tabagismo: {tabagismo or '—'}"
        )

    st.metric("Modificadores compartilhados", resumo_modificadores)


    if pbl is None:
        st.info(
            "Nenhum %PBL foi informado. A classificação ainda pode usar "
            "CAL, perda dentária, progressão direta e fenótipo."
        )

    else:
        st.success(
            f"%PBL de {pbl:.2f}% recebido do módulo radiográfico e disponível "
            "para esta classificação."
        )

    dados_periodontais_anteriores = st.session_state["dados_periodontais"]

    def indice_opcao(chave, opcoes):
        valor = dados_periodontais_anteriores[chave]

        if valor in opcoes:
            return opcoes.index(valor)

        return None

    def rotulo_opcao(opcao):
        if opcao is None:
            return "Não informado"

        return opcao

    with st.form("form_classificacao_periodontal"):
        st.markdown("### Severidade")
        severidade_um, severidade_dois = st.columns(2)

        with severidade_um:
            cal = st.number_input(
                "CAL interproximal máximo (mm):",
                min_value=0.0,
                value=dados_periodontais_anteriores["cal"],
                step=0.1,
                placeholder="Não informado"
            )

        with severidade_dois:
            dentes_perdidos = st.number_input(
                "Número de dentes perdidos atribuíveis à periodontite:",
                min_value=0,
                max_value=32,
                value=dados_periodontais_anteriores["dentes_perdidos"],
                step=1,
                placeholder="Não informado"
            )

        st.markdown("### Complexidade")
        complexidade_um, complexidade_dois = st.columns(2)

        with complexidade_um:
            sondagem = st.number_input(
                "Profundidade máxima de sondagem (mm):",
                min_value=0.0,
                value=dados_periodontais_anteriores["sondagem"],
                step=0.1,
                placeholder="Não informado"
            )

            perda_vertical = st.number_input(
                "Perda óssea vertical máxima (mm):",
                min_value=0.0,
                value=dados_periodontais_anteriores["perda_vertical"],
                step=0.1,
                placeholder="Não informado"
            )

            opcoes_furca = [None, "Nenhuma", "I", "II", "III"]
            furca = st.selectbox(
                "Maior classe de furca:",
                opcoes_furca,
                index=indice_opcao("furca", opcoes_furca),
                format_func=rotulo_opcao
            )

            opcoes_rebordo = [None, "Nenhum", "Moderado", "Grave"]
            defeito_rebordo = st.selectbox(
                "Defeito do rebordo:",
                opcoes_rebordo,
                index=indice_opcao("defeito_rebordo", opcoes_rebordo),
                format_func=rotulo_opcao
            )

            opcoes_sim_nao = [None, "Não", "Sim"]
            disfuncao_mastigatoria = st.selectbox(
                "Há disfunção mastigatória?",
                opcoes_sim_nao,
                index=indice_opcao(
                    "disfuncao_mastigatoria",
                    opcoes_sim_nao
                ),
                format_func=rotulo_opcao
            )

        with complexidade_dois:
            opcoes_mobilidade = [None, "Nenhuma", "I", "II", "III"]
            mobilidade = st.selectbox(
                "Maior grau de mobilidade dentária:",
                opcoes_mobilidade,
                index=indice_opcao("mobilidade", opcoes_mobilidade),
                format_func=rotulo_opcao
            )

            dentes_remanescentes = st.number_input(
                "Número de dentes remanescentes:",
                min_value=0,
                max_value=32,
                value=dados_periodontais_anteriores["dentes_remanescentes"],
                step=1,
                placeholder="Não informado"
            )

            colapso_mordida = st.selectbox(
                "Há colapso de mordida?",
                opcoes_sim_nao,
                index=indice_opcao("colapso_mordida", opcoes_sim_nao),
                format_func=rotulo_opcao
            )

            migracao_dentaria = st.selectbox(
                "Há migração dentária?",
                opcoes_sim_nao,
                index=indice_opcao("migracao_dentaria", opcoes_sim_nao),
                format_func=rotulo_opcao
            )

            abertura_leque = st.selectbox(
                "Há abertura em leque?",
                opcoes_sim_nao,
                index=indice_opcao("abertura_leque", opcoes_sim_nao),
                format_func=rotulo_opcao
            )

        st.markdown("### Extensão e distribuição")
        extensao_um, extensao_dois = st.columns(2)

        with extensao_um:
            percentual_dentes_envolvidos = st.number_input(
                "Percentual de dentes envolvidos pela periodontite (%):",
                min_value=0.0,
                max_value=100.0,
                value=dados_periodontais_anteriores[
                    "percentual_dentes_envolvidos"
                ],
                step=0.1,
                placeholder="Não informado"
            )

        with extensao_dois:
            padrao_molar_incisivo = st.selectbox(
                "Há padrão molar/incisivo?",
                opcoes_sim_nao,
                index=indice_opcao("padrao_molar_incisivo", opcoes_sim_nao),
                format_func=rotulo_opcao
            )

        st.markdown("### Progressão e modificadores do grau")
        grau_um, grau_dois = st.columns(2)

        with grau_um:
            progressao_5_anos = st.number_input(
                "Progressão periodontal em 5 anos (mm):",
                min_value=0.0,
                value=dados_periodontais_anteriores["progressao_5_anos"],
                step=0.1,
                placeholder="Não informado"
            )

            opcoes_fenotipo = [
                None,
                "Biofilme abundante com baixa destruição",
                "Destruição proporcional ao biofilme",
                "Destruição superior à esperada"
            ]
            fenotipo = st.selectbox(
                "Fenótipo clínico em relação ao biofilme:",
                opcoes_fenotipo,
                index=indice_opcao("fenotipo", opcoes_fenotipo),
                format_func=rotulo_opcao
            )

        with grau_dois:
            hba1c = st.number_input(
                "HbA1c (%), quando disponível:",
                min_value=0.1,
                max_value=20.0,
                value=dados_periodontais_anteriores["hba1c"],
                step=0.1,
                placeholder="Não informado",
                help="Informe somente quando houver diabetes diagnosticado."
            )

            st.caption(
                f"Diabetes: {diabetes or 'não informado'}  ·  "
                f"Tabagismo: {tabagismo or 'não informado'}"
            )

            if cigarros_dia is not None:
                st.caption(f"Média informada: {cigarros_dia} cigarros/dia")

        classificar_periodontal = st.form_submit_button(
            "Calcular classificação periodontal",
            type="primary",
            width="stretch"
        )

    executar_classificacao = False

    if classificar_periodontal:
        st.session_state["dados_periodontais"]["cal"] = cal
        st.session_state["dados_periodontais"]["dentes_perdidos"] = (
            dentes_perdidos
        )
        st.session_state["dados_periodontais"]["sondagem"] = sondagem
        st.session_state["dados_periodontais"]["perda_vertical"] = (
            perda_vertical
        )
        st.session_state["dados_periodontais"]["furca"] = furca
        st.session_state["dados_periodontais"]["defeito_rebordo"] = (
            defeito_rebordo
        )
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
        st.session_state["dados_periodontais"][
            "percentual_dentes_envolvidos"
        ] = percentual_dentes_envolvidos
        st.session_state["dados_periodontais"]["padrao_molar_incisivo"] = (
            padrao_molar_incisivo
        )
        st.session_state["dados_periodontais"]["progressao_5_anos"] = (
            progressao_5_anos
        )
        st.session_state["dados_periodontais"]["fenotipo"] = fenotipo
        st.session_state["dados_periodontais"]["hba1c"] = hba1c

        # Como os dados usados na classificação mudaram,
        # o resultado periodontal anterior deve ser recalculado
        # Os fatores de complexidade mudaram.
        # A classificação anterior precisa ser recalculada
        # Os fatores de complexidade mudaram.
        # A classificação anterior precisa ser recalculada.
        # A extensão/distribuição foi alterada.
        # O resultado periodontal anterior deve ser recalculado.
        # Os dados utilizados na graduação mudaram.
        # O resultado periodontal anterior deve ser recalculado.
        st.session_state["avaliacao"]["periodontal"] = None
        executar_classificacao = True

        if hba1c is not None and diabetes != "Sim":
            st.error(
                "A HbA1c só deve ser informada quando "
                "o paciente possui diabetes diagnosticado. "
                "O valor foi salvo, mas não será aplicado como modificador."
            )


    #CALCULOS DE CLSSIFICAÇÃO DO ESTÁGIO - agora ficou pegado
    if executar_classificacao:

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
            dados_ausentes_estagio = []

            if cal is None:
                dados_ausentes_estagio.append("CAL interproximal máximo")

            if pbl is None:
                dados_ausentes_estagio.append("%PBL radiográfico")

            if dentes_perdidos is None:
                dados_ausentes_estagio.append(
                    "Dentes perdidos atribuíveis à periodontite"
                )

            st.session_state["avaliacao"]["periodontal"] = {
                "status": "dados_insuficientes",
                "dados_ausentes_estagio": dados_ausentes_estagio
            }

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

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    #APLICA FATORES DE COMPLEXIDADES
    if executar_classificacao:

        resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

        if (
            resultado_periodontal is None
            or "estagio_severidade" not in resultado_periodontal
        ):
            st.info(
                "O estágio depende de mais dados de severidade. "
                "Os demais componentes disponíveis continuarão sendo avaliados."
            )

        else:

            dados_periodontais = st.session_state["dados_periodontais"]

            # Verifica quais informações capazes de alterar
            # o estágio ainda não foram informadas
            campos_estagio = {
                "dentes_perdidos":
                    "Dentes perdidos atribuíveis à periodontite",

                "sondagem":
                    "Profundidade máxima de sondagem",

                "perda_vertical":
                    "Perda óssea vertical",

                "furca":
                    "Envolvimento de furca",

                "defeito_rebordo":
                    "Defeito de rebordo",

                "disfuncao_mastigatoria":
                    "Disfunção mastigatória",

                "mobilidade":
                    "Mobilidade dentária",

                "dentes_remanescentes":
                    "Número de dentes remanescentes",

                "colapso_mordida":
                    "Colapso de mordida",

                "migracao_dentaria":
                    "Migração dentária",

                "abertura_leque":
                    "Abertura em leque"
            }


            dados_ausentes_estagio = []

            cal = dados_periodontais["cal"]

            if cal is None:
                dados_ausentes_estagio.append("CAL interproximal máximo")

                if pbl is None:
                    dados_ausentes_estagio.append("%PBL radiográfico")


            for campo, nome_campo in campos_estagio.items():

                if dados_periodontais[campo] is None:

                    dados_ausentes_estagio.append(
                        nome_campo
                    )

            estagio_final = resultado_periodontal["estagio_severidade"]

            fatores_complexidade = []


            # Profundidade de sondagem
            sondagem = dados_periodontais["sondagem"]

            if sondagem is not None:

                if sondagem >= 6:

                    if estagio_final in ["I", "II"]:
                        estagio_final = "III"

                    fatores_complexidade.append("Profundidade de sondagem ≥ 6 mm")
                        
                   

                elif sondagem > 4:

                    if estagio_final == "I":
                        estagio_final = "II"

                    fatores_complexidade.append("Profundidade de sondagem > 4 mm")
                        
                    


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

            # Guarda quais critérios não foram informados
            resultado_periodontal["dados_ausentes_estagio"] = (
                dados_ausentes_estagio
            )


            # Se existe pelo menos um dado ausente,
            # o estágio deve ser considerado provisório
            resultado_periodontal["estagio_provisorio"] = (
                len(dados_ausentes_estagio) > 0
            )

            if len(dados_ausentes_estagio) > 0:

                st.warning(
                    "O estágio calculado é provisório, pois existem "
                    "fatores de complexidade não informados."
                )

            # CALCULA EXTENSÃO E DISTRIBUIÇÃO

    if executar_classificacao:

        dados_periodontais = st.session_state["dados_periodontais"]

        percentual = dados_periodontais["percentual_dentes_envolvidos"]

        padrao_molar_incisivo = dados_periodontais[
            "padrao_molar_incisivo"
        ]

        dados_ausentes_extensao = []

        if padrao_molar_incisivo is None:
            dados_ausentes_extensao.append("Padrão molar/incisivo")


        # O padrão molar/incisivo tem prioridade
        if padrao_molar_incisivo == "Sim":

            extensao_distribuicao = "Padrão molar/incisivo"


        # Se não houver padrão molar/incisivo,
        # precisamos do percentual de dentes envolvidos
        elif percentual is None:
            dados_ausentes_extensao.append(
                "Percentual de dentes envolvidos pela periodontite"
            )

            extensao_distribuicao = None

            st.info(
                "Extensão/distribuição não determinada com os dados "
                "disponíveis. Estágio e grau serão mantidos."
            )


        # Menos de 30% = localizada
        elif percentual < 30:

            extensao_distribuicao = "Localizada"


        # 30% ou mais = generalizada
        else:

            extensao_distribuicao = "Generalizada"


        if st.session_state["avaliacao"]["periodontal"] is None:
            st.session_state["avaliacao"]["periodontal"] = {}

        st.session_state["avaliacao"]["periodontal"][
            "extensao_distribuicao"
        ] = extensao_distribuicao

        st.session_state["avaliacao"]["periodontal"][
            "dados_ausentes_extensao"
        ] = dados_ausentes_extensao

        st.session_state["avaliacao"]["periodontal"][
            "extensao_provisoria"
        ] = len(dados_ausentes_extensao) > 0

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]
    # CALCULA O GRAU-BASE PELA PROGRESSÃO

    if executar_classificacao:

        dados_periodontais = st.session_state["dados_periodontais"]

        progressao = dados_periodontais["progressao_5_anos"]

        fenotipo = dados_periodontais["fenotipo"]

        idade = st.session_state["dados_caso"]["idade"]

        pbl = st.session_state["avaliacao"]["pbl"]


        grau_base = None

        criterio_grau_base = None

        razao_pbl_idade = None

        dados_ausentes_grau_base = []

        if progressao is None:
            dados_ausentes_grau_base.append("Progressão periodontal em 5 anos")


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

            razao_pbl_idade_calculo = pbl / idade
            razao_pbl_idade = round(razao_pbl_idade_calculo, 2)

            if razao_pbl_idade_calculo < 0.25:
                grau_base = "A"

            elif razao_pbl_idade_calculo <= 1:
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

            if fenotipo is None:
                dados_ausentes_grau_base.append(
                    "Fenótipo clínico em relação ao biofilme"
                )


        # 3. Se não houver progressão nem %PBL/idade,
        # tentamos usar apenas o fenótipo
        elif fenotipo is not None:

            if pbl is None:
                dados_ausentes_grau_base.append("%PBL radiográfico")

            if idade is None:
                dados_ausentes_grau_base.append("Idade")

            if fenotipo == "Biofilme abundante com baixa destruição":
                grau_base = "A"

            elif fenotipo == "Destruição proporcional ao biofilme":
                grau_base = "B"

            else:
                grau_base = "C"

            criterio_grau_base = "Fenótipo"


        # 4. Sem evidência de progressão, parte-se do grau B.
        if grau_base is None:

            if pbl is None:
                dados_ausentes_grau_base.append("%PBL radiográfico")

            if idade is None:
                dados_ausentes_grau_base.append("Idade")

            if fenotipo is None:
                dados_ausentes_grau_base.append(
                    "Fenótipo clínico em relação ao biofilme"
                )

            grau_base = "B"
            criterio_grau_base = (
                "Grau B inicial por ausência de evidência de progressão"
            )


        if grau_base is not None:

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

            st.session_state["avaliacao"]["periodontal"][
                "dados_ausentes_grau_base"
            ] = dados_ausentes_grau_base
            
            # Se o grau foi determinado apenas pelo fenótipo,
            # consideramos esse grau-base provisório,
            # pois faltaram evidências direta e indireta por %PBL/idade
            st.session_state["avaliacao"]["periodontal"][
                "grau_base_provisorio"
            ] = (
                len(dados_ausentes_grau_base) > 0
            )

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    # APLICA OS MODIFICADORES DO GRAU

    if executar_classificacao:

        resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


        # Primeiro precisamos ter um grau-base calculado
        if (
            resultado_periodontal is None
            or "grau_base" not in resultado_periodontal
        ):

            st.info(
                "O grau depende de mais dados de progressão. "
                "Os resultados periodontais disponíveis serão mantidos."
            )


        else:

            dados_periodontais = st.session_state["dados_periodontais"]

            tabagismo = st.session_state["dados_clinicos"]["tabagismo"]

            cigarros_dia = st.session_state["dados_clinicos"]["cigarros_dia"]

            diabetes = st.session_state["dados_clinicos"]["diabetes"]

            hba1c = dados_periodontais["hba1c"]

            # Lista das informações ausentes que podem
            # interferir na graduação final
            dados_ausentes_grau = list(
                resultado_periodontal.get("dados_ausentes_grau_base", [])
            )


            if tabagismo is None:

                dados_ausentes_grau.append(
                    "Situação de tabagismo"
                )


            if (
                tabagismo == "Fumante atual"
                and cigarros_dia is None
            ):

                dados_ausentes_grau.append(
                    "Média de cigarros por dia"
                )


            if diabetes is None:

                dados_ausentes_grau.append(
                    "Situação de diabetes"
                )


            elif diabetes == "Não sabe":

                dados_ausentes_grau.append(
                    "Situação de diabetes confirmada"
                )


            elif diabetes == "Sim" and hba1c is None:

                dados_ausentes_grau.append(
                    "HbA1c"
                )


            # Começamos pelo grau obtido na etapa anterior
            grau_final = resultado_periodontal["grau_base"]

            modificadores_grau = []


            # -------------------------
            # TABAGISMO
            # -------------------------

            if tabagismo == "Fumante atual":

                if cigarros_dia is None:

                    st.warning(
                        "A média de cigarros por dia não foi informada. "
                        "O tabagismo não modificou o grau."
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

            resultado_periodontal["dados_ausentes_grau"] = (
                dados_ausentes_grau
            )


            resultado_periodontal["grau_provisorio"] = (
                resultado_periodontal["grau_base_provisorio"]
                or len(dados_ausentes_grau) > 0
            )


            if resultado_periodontal["grau_provisorio"]:

                st.warning(
                    "O grau periodontal é provisório, pois existem "
                    "informações ausentes que podem alterar a graduação."
                )


            resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    # CONSOLIDA A CLASSIFICAÇÃO PERIODONTAL FINAL

    if executar_classificacao:

        resultado_periodontal = st.session_state["avaliacao"]["periodontal"]


        # Verifica se existe resultado periodontal
        if resultado_periodontal is None:

            st.info(
                "Ainda não há dados suficientes para produzir resultados "
                "periodontais."
            )


        # Verifica se o estágio final já foi calculado
        elif "estagio" not in resultado_periodontal:

            resultado_periodontal["status"] = "dados_insuficientes"

            st.warning(
                "Dados insuficientes para determinar o estágio periodontal."
            )

        # Verifica se o grau final já foi calculado
        elif "grau" not in resultado_periodontal:

            resultado_periodontal["status"] = "dados_insuficientes"

            st.warning(
                "Dados insuficientes para determinar o grau periodontal."
            )


        else:

            estagio = resultado_periodontal["estagio"]

            extensao = resultado_periodontal.get("extensao_distribuicao")

            if extensao is None:
                extensao_texto = "Extensão/distribuição não determinada"

            else:
                extensao_texto = extensao

            grau = resultado_periodontal["grau"]

            # Verifica se o estágio ou o grau
            # foram calculados com informações ausentes
            estagio_provisorio = resultado_periodontal.get(
                "estagio_provisorio",
                False
            )

            grau_provisorio = resultado_periodontal.get(
                "grau_provisorio",
                False
            )

            extensao_provisoria = resultado_periodontal.get(
                "extensao_provisoria",
                False
            )


            # Se qualquer uma das duas partes for provisória,
            # a classificação periodontal completa também será
            classificacao_provisoria = (
                estagio_provisorio
                or grau_provisorio
                or extensao_provisoria
            )

            classificacao_final = (
                f"Periodontite Estágio {estagio}, "
                f"{extensao_texto}, "
                f"Grau {grau}"
            )


            resultado_periodontal[
                "classificacao_final"
            ] = classificacao_final

            resultado_periodontal[
                "classificacao_provisoria"
            ] = classificacao_provisoria

            dados_ausentes = []

            for chave in [
                "dados_ausentes_estagio",
                "dados_ausentes_extensao",
                "dados_ausentes_grau"
            ]:
                for dado in resultado_periodontal.get(chave, []):
                    if dado not in dados_ausentes:
                        dados_ausentes.append(dado)

            resultado_periodontal["dados_ausentes"] = dados_ausentes

            if classificacao_provisoria:
                resultado_periodontal["status"] = "provisorio"

            else:
                resultado_periodontal["status"] = "concluido"

            if classificacao_provisoria:

                st.warning(
                    "Classificação periodontal gerada, mas considerada "
                    "provisória devido à ausência de informações."
                )

            else:

                st.success(
                    "Classificação periodontal final gerada com sucesso."
                )
            resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    if (
        resultado_periodontal is not None
        and "classificacao_final" not in resultado_periodontal
    ):
        dados_ausentes = []

        for chave in [
            "dados_ausentes_estagio",
            "dados_ausentes_extensao",
            "dados_ausentes_grau"
        ]:
            for dado in resultado_periodontal.get(chave, []):
                if dado not in dados_ausentes:
                    dados_ausentes.append(dado)

        resultado_periodontal["dados_ausentes"] = dados_ausentes
        resultado_periodontal["status"] = "dados_insuficientes"


    if (
        resultado_periodontal is not None
        and "classificacao_final" in resultado_periodontal
    ):
        classificacao_provisoria = resultado_periodontal.get(
            "classificacao_provisoria",
            False
        )

        estado_classificacao = "Classificação provisória"
        classe_estado = "perio-result-card is-warning"

        if not classificacao_provisoria:
            estado_classificacao = "Classificação definitiva"
            classe_estado = "perio-result-card"

        extensao_exibicao = (
            resultado_periodontal.get("extensao_distribuicao")
            or "Não determinada"
        )

        st.markdown(
            f"""
            <section class="perio-result">
                <div class="perio-result__eyebrow">
                    Resultado periodontal final
                </div>
                <div class="perio-result__title">
                    {escape(resultado_periodontal['classificacao_final'])}
                </div>
                <div class="perio-result__grid">
                    <div class="perio-result-card">
                        <div class="perio-result-card__label">Estágio</div>
                        <div class="perio-result-card__value">
                            {escape(resultado_periodontal['estagio'])}
                        </div>
                    </div>
                    <div class="perio-result-card">
                        <div class="perio-result-card__label">
                            Extensão / distribuição
                        </div>
                        <div class="perio-result-card__value">
                            {escape(extensao_exibicao)}
                        </div>
                    </div>
                    <div class="perio-result-card">
                        <div class="perio-result-card__label">Grau</div>
                        <div class="perio-result-card__value">
                            {escape(resultado_periodontal['grau'])}
                        </div>
                    </div>
                    <div class="{classe_estado}">
                        <div class="perio-result-card__label">Situação</div>
                        <div class="perio-result-card__value">
                            {estado_classificacao}
                        </div>
                    </div>
                </div>
            </section>
            """,
            unsafe_allow_html=True
        )

        with st.expander("Ver critérios determinantes e detalhes"):
            st.write(
                "**Critério de severidade:**",
                resultado_periodontal["criterio_severidade"]
            )

            st.write(
                "**Critério utilizado para o grau-base:**",
                resultado_periodontal["criterio_grau_base"]
            )

            if resultado_periodontal["razao_pbl_idade"] is not None:
                st.write(
                    "**Relação %PBL / idade:**",
                    resultado_periodontal["razao_pbl_idade"]
                )

            fatores_complexidade = resultado_periodontal[
                "fatores_complexidade"
            ]
            st.markdown("**Fatores de complexidade identificados**")

            if len(fatores_complexidade) > 0:
                for fator in fatores_complexidade:
                    st.write("-", fator)

            else:
                st.write("Nenhum.")

            modificadores_grau = resultado_periodontal["modificadores_grau"]
            st.markdown("**Modificadores do grau identificados**")

            if len(modificadores_grau) > 0:
                for modificador in modificadores_grau:
                    st.write("-", modificador)

            else:
                st.write("Nenhum.")

            if classificacao_provisoria:
                dados_ausentes_estagio = resultado_periodontal.get(
                    "dados_ausentes_estagio",
                    []
                )
                dados_ausentes_grau = resultado_periodontal.get(
                    "dados_ausentes_grau",
                    []
                )
                dados_ausentes_extensao = resultado_periodontal.get(
                    "dados_ausentes_extensao",
                    []
                )

                if len(dados_ausentes_estagio) > 0:
                    st.markdown("**Dados ausentes relacionados ao estágio**")

                    for dado in dados_ausentes_estagio:
                        st.write("-", dado)

                if len(dados_ausentes_grau) > 0:
                    st.markdown("**Dados ausentes relacionados ao grau**")

                    for dado in dados_ausentes_grau:
                        st.write("-", dado)

                if len(dados_ausentes_extensao) > 0:
                    st.markdown(
                        "**Dados ausentes relacionados à extensão/distribuição**"
                    )

                    for dado in dados_ausentes_extensao:
                        st.write("-", dado)

    elif (
        resultado_periodontal is not None
        and resultado_periodontal.get("status") == "dados_insuficientes"
    ):
        st.warning("Dados insuficientes para concluir a classificação periodontal.")

        resultados_parciais = []

        if resultado_periodontal.get("estagio") is not None:
            resultados_parciais.append(
                ("Estágio", resultado_periodontal["estagio"])
            )

        if resultado_periodontal.get("grau") is not None:
            resultados_parciais.append(("Grau", resultado_periodontal["grau"]))

        if resultado_periodontal.get("extensao_distribuicao") is not None:
            resultados_parciais.append(
                (
                    "Extensão / distribuição",
                    resultado_periodontal["extensao_distribuicao"]
                )
            )

        if len(resultados_parciais) > 0:
            colunas_parciais = st.columns(len(resultados_parciais))

            for coluna, (rotulo, valor) in zip(
                colunas_parciais,
                resultados_parciais
            ):
                with coluna:
                    st.metric(rotulo, valor)

        dados_ausentes = resultado_periodontal.get("dados_ausentes", [])

        if len(dados_ausentes) > 0:
            st.markdown("**Informações ausentes:**")

            for dado in dados_ausentes:
                st.write("-", dado)
