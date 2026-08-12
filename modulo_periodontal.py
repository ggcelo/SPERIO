import streamlit as st


def mostrar_modulo_periodontal():
    st.subheader("Classificação periodontal AAP/EFP")


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
