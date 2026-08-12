import streamlit as st
from html import escape
from datetime import datetime


def mostrar_relatorio():
    st.header("Relatório integrado")

    def texto_valor(valor, unidade=""):
        if valor is None:
            return "Não informado"

        if unidade:
            return f"{valor} {unidade}"

        return str(valor)


    # Pegamos os dados principais já armazenados
    dados_caso = st.session_state["dados_caso"]

    dados_clinicos = st.session_state["dados_clinicos"]

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    resultado_findrisc = st.session_state["avaliacao"]["findrisc"]

    resultado_interheart = st.session_state["avaliacao"]["interheart"]

    dados_radiograficos = st.session_state["dados_radiograficos"]

    pbl = st.session_state["avaliacao"]["pbl"]

    dados_findrisc = st.session_state["dados_findrisc"]
    dados_interheart = st.session_state["dados_interheart"]
    dados_periodontais = st.session_state["dados_periodontais"]

    dente_determinante = dados_radiograficos["dente_determinante"]
    superficie_determinante = dados_radiograficos["superficie_determinante"]

    periodontal_concluido = (
        resultado_periodontal is not None
        and "classificacao_final" in resultado_periodontal
    )
    findrisc_nao_aplicavel = dados_clinicos["diabetes"] == "Sim"

    avaliacoes_concluidas = 0

    if periodontal_concluido:
        avaliacoes_concluidas += 1

    if resultado_findrisc is not None or findrisc_nao_aplicavel:
        avaliacoes_concluidas += 1

    if resultado_interheart is not None:
        avaliacoes_concluidas += 1

    codigo_relatorio = escape(str(dados_caso["codigo"] or "Caso não definido"))
    idade_relatorio = (
        f"{dados_caso['idade']} anos"
        if dados_caso["idade"] is not None
        else "Idade não informada"
    )
    sexo_relatorio = dados_caso["sexo"] or "Sexo não informado"

    st.markdown(
        f"""
        <section class="perio-report-header">
            <div>
                <div class="perio-report-header__label">
                    Relatório de avaliação integrada
                </div>
                <div class="perio-report-header__title">{codigo_relatorio}</div>
                <div class="perio-report-header__meta">
                    <span>{escape(idade_relatorio)}</span>
                    <span>{escape(sexo_relatorio)}</span>
                </div>
            </div>
            <div class="perio-report-header__count">
                {avaliacoes_concluidas}/3
                <span>avaliações concluídas</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Resumo principal")

    # CLASSIFICAÇÃO PERIODONTAL
    if periodontal_concluido:
        estado_periodontal = "Concluído"
        valor_periodontal = resultado_periodontal["classificacao_final"]
        classe_periodontal = "perio-status is-complete"

    else:
        estado_periodontal = "Pendente"
        valor_periodontal = "Classificação ainda não concluída."
        classe_periodontal = "perio-status"

    # ANÁLISE RADIOGRÁFICA
    if pbl is not None:
        estado_pbl = "Disponível"
        valor_pbl = f"{pbl:.2f}%"
        classe_pbl = "perio-status is-complete"

    else:
        estado_pbl = "Pendente"
        valor_pbl = "%PBL ainda não calculado."
        classe_pbl = "perio-status"

    # FINDRISC
    if resultado_findrisc is not None:
        estado_findrisc = "Concluído"
        valor_findrisc = (
            f"{resultado_findrisc['pontos']} pontos · "
            f"{resultado_findrisc['classificacao']}"
        )
        classe_findrisc = "perio-status is-complete"

    elif findrisc_nao_aplicavel:
        estado_findrisc = "Não aplicável"
        valor_findrisc = "Diabetes já diagnosticado."
        classe_findrisc = "perio-status is-na"

    else:
        estado_findrisc = "Pendente"
        valor_findrisc = "Resultado ainda não calculado."
        classe_findrisc = "perio-status"

    # INTERHEART
    if resultado_interheart is not None:
        estado_interheart = "Concluído"
        valor_interheart = (
            f"{resultado_interheart['pontos']} pontos · "
            f"{resultado_interheart['classificacao']}"
        )
        classe_interheart = "perio-status is-complete"

    else:
        estado_interheart = "Pendente"
        valor_interheart = "Resultado ainda não calculado."
        classe_interheart = "perio-status"

    colunas_resumo = st.columns(4)
    itens_resumo = [
        (
            classe_periodontal,
            estado_periodontal,
            "Periodontal",
            valor_periodontal
        ),
        (classe_pbl, estado_pbl, "%PBL", valor_pbl),
        (classe_findrisc, estado_findrisc, "FINDRISC", valor_findrisc),
        (
            classe_interheart,
            estado_interheart,
            "INTERHEART",
            valor_interheart
        )
    ]

    for coluna, item in zip(colunas_resumo, itens_resumo):
        classe, estado, titulo, valor = item

        with coluna:
            st.markdown(
                f"""
                <div class="{classe}">
                    <div class="perio-status__state">{escape(estado)}</div>
                    <div class="perio-status__title">{escape(titulo)}</div>
                    <div class="perio-status__value">
                        {escape(str(valor))}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # DETALHAMENTO DOS RESULTADOS

    # -------------------------
    # DETALHAMENTO PERIODONTAL
    # -------------------------
    with st.expander("Detalhamento periodontal", expanded=periodontal_concluido):
        if periodontal_concluido:
            coluna_estagio, coluna_extensao, coluna_grau = st.columns(3)

            with coluna_estagio:
                st.metric("Estágio", resultado_periodontal["estagio"])

            with coluna_extensao:
                st.metric(
                    "Extensão / distribuição",
                    resultado_periodontal["extensao_distribuicao"]
                )

            with coluna_grau:
                st.metric("Grau", resultado_periodontal["grau"])

            # Informa se a classificação é definitiva ou provisória
            if resultado_periodontal.get("classificacao_provisoria", False):
                st.warning("Classificação provisória.")

            else:
                st.success("Classificação definitiva.")

            # Critério que determinou a severidade
            st.write(
                "**Critério de severidade:**",
                resultado_periodontal["criterio_severidade"]
            )

            # Fatores de complexidade
            fatores = resultado_periodontal["fatores_complexidade"]
            st.markdown("**Fatores de complexidade identificados**")

            if len(fatores) > 0:
                for fator in fatores:
                    st.write("-", fator)

            else:
                st.write("Nenhum.")

            # Critério utilizado para definir o grau-base
            st.write(
                "**Critério utilizado para o grau-base:**",
                resultado_periodontal["criterio_grau_base"]
            )

            # Relação %PBL / idade
            if resultado_periodontal["razao_pbl_idade"] is not None:
                st.write(
                    "**Relação %PBL / idade:**",
                    resultado_periodontal["razao_pbl_idade"]
                )

            # Modificadores do grau
            modificadores = resultado_periodontal["modificadores_grau"]
            st.markdown("**Modificadores do grau identificados**")

            if len(modificadores) > 0:
                for modificador in modificadores:
                    st.write("-", modificador)

            else:
                st.write("Nenhum.")

            # Se a classificação for provisória,
            # mostramos quais informações estavam ausentes
            if resultado_periodontal.get("classificacao_provisoria", False):
                dados_ausentes_estagio = resultado_periodontal.get(
                    "dados_ausentes_estagio",
                    []
                )
                dados_ausentes_grau = resultado_periodontal.get(
                    "dados_ausentes_grau",
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

        else:
            st.info("Ainda não existem resultados periodontais completos.")

    # -------------------------
    # DETALHAMENTO RADIOGRÁFICO
    # -------------------------
    with st.expander("Detalhamento radiográfico"):
        if pbl is not None:
            coluna_pbl, coluna_dente, coluna_superficie = st.columns(3)

            with coluna_pbl:
                st.metric("%PBL máximo", f"{pbl:.2f}%")

            with coluna_dente:
                st.metric("Objeto/dente determinante", dente_determinante)

            with coluna_superficie:
                st.metric("Superfície determinante", superficie_determinante)

        else:
            st.info("Análise radiográfica ainda não concluída.")

    with st.expander("Detalhamento dos escores de risco"):
        coluna_findrisc, coluna_interheart = st.columns(2)

        # FINDRISC
        with coluna_findrisc:
            st.markdown("#### FINDRISC")

            if resultado_findrisc is not None:
                st.metric("Pontuação", resultado_findrisc["pontos"])
                st.write(
                    "**Classificação:**",
                    resultado_findrisc["classificacao"]
                )
                st.write(
                    "**Risco estimado em 10 anos:**",
                    resultado_findrisc["estimativa"]
                )

            elif findrisc_nao_aplicavel:
                st.info(
                    "FINDRISC não aplicável — diabetes já diagnosticado."
                )

            else:
                st.info("FINDRISC ainda não calculado.")

        # INTERHEART
        with coluna_interheart:
            st.markdown("#### INTERHEART")

            if resultado_interheart is not None:
                st.metric("Pontuação", resultado_interheart["pontos"])
                st.write(
                    "**Classificação:**",
                    resultado_interheart["classificacao"]
                )
                st.write(
                    "**Relação cintura-quadril:**",
                    resultado_interheart["rcq"]
                )

            else:
                st.info("INTERHEART ainda não calculado.")

    # DADOS UTILIZADOS NO RELATÓRIO
    st.subheader("Dados utilizados e rastreabilidade")

    with st.expander("Ver dados clínicos compartilhados"):
        coluna_um, coluna_dois = st.columns(2)

        with coluna_um:
            st.write("**Peso:**", texto_valor(dados_clinicos["peso"], "kg"))
            st.write("**Altura:**", texto_valor(dados_clinicos["altura"], "m"))
            st.write("**IMC:**", texto_valor(dados_clinicos["imc"], "kg/m²"))
            st.write("**Diabetes:**", texto_valor(dados_clinicos["diabetes"]))

        with coluna_dois:
            st.write("**Cintura:**", texto_valor(dados_clinicos["cintura"], "cm"))
            st.write("**Quadril:**", texto_valor(dados_clinicos["quadril"], "cm"))
            st.write("**Tabagismo:**", texto_valor(dados_clinicos["tabagismo"]))

            # Cigarros por dia só é relevante para fumantes
            if dados_clinicos["tabagismo"] in [
                "Fumante atual",
                "Ex-fumante há 12 meses ou menos"
            ]:
                st.write(
                    "**Média de cigarros por dia:**",
                    texto_valor(dados_clinicos["cigarros_dia"])
                )

    # DADOS ESPECÍFICOS DOS MÓDULOS

    # FINDRISC
    with st.expander("Ver dados utilizados no FINDRISC"):
        st.write(
            "**Atividade física:**",
            texto_valor(dados_findrisc["atividade_fisica"])
        )
        st.write(
            "**Consumo diário de frutas ou vegetais:**",
            texto_valor(dados_findrisc["frutas_vegetais"])
        )
        st.write(
            "**Uso de medicamento para pressão alta:**",
            texto_valor(dados_findrisc["medicacao_pressao"])
        )
        st.write(
            "**Histórico de glicemia elevada:**",
            texto_valor(dados_findrisc["glicemia_elevada"])
        )
        st.write(
            "**Histórico familiar de diabetes:**",
            texto_valor(dados_findrisc["historico_familiar"])
        )

    # INTERHEART
    with st.expander("Ver dados utilizados no INTERHEART"):
        campos_interheart = [
            ("Hipertensão", "hipertensao"),
            ("Histórico parental de infarto", "historico_parental_infarto"),
            ("Estresse", "estresse"),
            ("Exposição ao fumo passivo", "fumo_passivo"),
            ("Atividade física no lazer", "atividade_lazer"),
            ("Tristeza ou depressão", "tristeza_depressao"),
            ("Consumo de alimentos salgados", "alimento_salgado"),
            ("Consumo de fritura ou fast-food", "fritura_fast_food"),
            ("Consumo diário de frutas", "fruta_diaria"),
            ("Consumo diário de vegetais", "vegetais_diarios"),
            ("Consumo de carne ou aves", "carne_aves")
        ]

        for rotulo, chave in campos_interheart:
            st.write(
                f"**{rotulo}:**",
                texto_valor(dados_interheart[chave])
            )

    # CLASSIFICAÇÃO PERIODONTAL
    with st.expander("Ver dados utilizados na classificação periodontal"):
        campos_periodontais = [
            ("CAL interproximal máximo", "cal", "mm"),
            ("Dentes perdidos por periodontite", "dentes_perdidos", ""),
            ("Profundidade máxima de sondagem", "sondagem", "mm"),
            ("Perda óssea vertical máxima", "perda_vertical", "mm"),
            ("Furca", "furca", ""),
            ("Defeito do rebordo", "defeito_rebordo", ""),
            ("Disfunção mastigatória", "disfuncao_mastigatoria", ""),
            ("Mobilidade dentária", "mobilidade", ""),
            ("Dentes remanescentes", "dentes_remanescentes", ""),
            ("Colapso de mordida", "colapso_mordida", ""),
            ("Migração dentária", "migracao_dentaria", ""),
            ("Abertura em leque", "abertura_leque", ""),
            (
                "Percentual de dentes envolvidos",
                "percentual_dentes_envolvidos",
                "%"
            ),
            ("Padrão molar/incisivo", "padrao_molar_incisivo", ""),
            ("Progressão periodontal em 5 anos", "progressao_5_anos", "mm"),
            ("Fenótipo clínico", "fenotipo", "")
        ]

        for rotulo, chave, unidade in campos_periodontais:
            valor = dados_periodontais[chave]
            st.write(f"**{rotulo}:**", texto_valor(valor, unidade))

        if dados_periodontais["hba1c"] is not None:
            st.write(
                "**HbA1c:**",
                texto_valor(dados_periodontais["hba1c"], "%")
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

    if resultado_findrisc is None and not findrisc_nao_aplicavel:

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
    
        data_hora_relatorio = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )

        # Prepara os fatores de complexidade para o relatório
        fatores_complexidade = resultado_periodontal[
            "fatores_complexidade"
        ]

        if len(fatores_complexidade) > 0:

            fatores_texto = ", ".join(
                fatores_complexidade
            )

        else:

            fatores_texto = "Nenhum"


        # Prepara os modificadores do grau para o relatório
        modificadores_grau = resultado_periodontal[
            "modificadores_grau"
        ]

        if len(modificadores_grau) > 0:

            modificadores_texto = ", ".join(
                modificadores_grau
            )

        else:

            modificadores_texto = "Nenhum"

        if resultado_findrisc is not None:
            resumo_findrisc_relatorio = (
                f"{resultado_findrisc['pontos']} pontos - "
                f"{resultado_findrisc['classificacao']}"
            )

        else:
            resumo_findrisc_relatorio = (
                "Não aplicável — diabetes já diagnosticado"
            )

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
            f"FINDRISC: {resumo_findrisc_relatorio}\n"
            f"INTERHEART: {resultado_interheart['pontos']} pontos - "
            f"{resultado_interheart['classificacao']}\n"
            f"%PBL: {pbl}%\n"
        )

        texto_relatorio += (
            "\n"
            "ANÁLISE RADIOGRÁFICA\n"
            f"%PBL máximo: {pbl}%\n"
            f"Objeto/dente determinante: {dente_determinante}\n"
            f"Superfície determinante: {superficie_determinante}\n"
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
            f"Fatores de complexidade: {fatores_texto}\n"
            f"Modificadores do grau: {modificadores_texto}\n"
        )

        if resultado_periodontal["razao_pbl_idade"] is not None:

            texto_relatorio += (
                f"Relação %PBL / idade: "
                f"{resultado_periodontal['razao_pbl_idade']}\n"
            )


        # FINDRISC
        if resultado_findrisc is not None:
            texto_relatorio += (
                "\n"
                "FINDRISC\n"
                f"Pontuação: {resultado_findrisc['pontos']}\n"
                f"Classificação: {resultado_findrisc['classificacao']}\n"
                f"Estimativa em 10 anos: "
                f"{resultado_findrisc['estimativa']}\n"
            )

        else:
            texto_relatorio += (
                "\n"
                "FINDRISC\n"
                "Não aplicável — diabetes já diagnosticado.\n"
            )

        texto_relatorio += (
            "\n"
            "DADOS CLÍNICOS UTILIZADOS\n"
            f"Peso: {dados_clinicos['peso']} kg\n"
            f"Altura: {dados_clinicos['altura']} m\n"
            f"IMC: {dados_clinicos['imc']} kg/m²\n"
            f"Cintura: {dados_clinicos['cintura']} cm\n"
            f"Quadril: {dados_clinicos['quadril']} cm\n"
            f"Diabetes: {dados_clinicos['diabetes']}\n"
            f"Tabagismo: {dados_clinicos['tabagismo']}\n"
        )

        if dados_clinicos["tabagismo"] in [
            "Fumante atual",
            "Ex-fumante há 12 meses ou menos"
        ]:

            texto_relatorio += (
                f"Média de cigarros por dia: "
                f"{dados_clinicos['cigarros_dia']}\n"
            )
        
        if resultado_findrisc is not None:
            texto_relatorio += (
                "\n"
                "DADOS UTILIZADOS NO FINDRISC\n"
                f"Atividade física: "
                f"{dados_findrisc['atividade_fisica']}\n"
                f"Frutas ou vegetais diariamente: "
                f"{dados_findrisc['frutas_vegetais']}\n"
                f"Medicamento para pressão alta: "
                f"{dados_findrisc['medicacao_pressao']}\n"
                f"Glicemia elevada: "
                f"{dados_findrisc['glicemia_elevada']}\n"
                f"Histórico familiar de diabetes: "
                f"{dados_findrisc['historico_familiar']}\n"
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

        texto_relatorio += (
            "\n"
            "DADOS UTILIZADOS NA CLASSIFICAÇÃO PERIODONTAL\n"
            f"CAL máximo: {texto_valor(dados_periodontais['cal'], 'mm')}\n"
            f"%PBL: {pbl}%\n"
            f"Dentes perdidos por periodontite: "
            f"{texto_valor(dados_periodontais['dentes_perdidos'])}\n"
            f"Profundidade máxima de sondagem: "
            f"{texto_valor(dados_periodontais['sondagem'], 'mm')}\n"
            f"Perda óssea vertical máxima: "
            f"{texto_valor(dados_periodontais['perda_vertical'], 'mm')}\n"
            f"Furca: {texto_valor(dados_periodontais['furca'])}\n"
            f"Defeito do rebordo: "
            f"{texto_valor(dados_periodontais['defeito_rebordo'])}\n"
            f"Disfunção mastigatória: "
            f"{texto_valor(dados_periodontais['disfuncao_mastigatoria'])}\n"
            f"Mobilidade: {texto_valor(dados_periodontais['mobilidade'])}\n"
            f"Dentes remanescentes: "
            f"{texto_valor(dados_periodontais['dentes_remanescentes'])}\n"
            f"Colapso de mordida: "
            f"{texto_valor(dados_periodontais['colapso_mordida'])}\n"
            f"Migração dentária: "
            f"{texto_valor(dados_periodontais['migracao_dentaria'])}\n"
            f"Abertura em leque: "
            f"{texto_valor(dados_periodontais['abertura_leque'])}\n"
            f"Percentual de dentes envolvidos: "
            f"{texto_valor(dados_periodontais['percentual_dentes_envolvidos'], '%')}\n"
            f"Padrão molar/incisivo: "
            f"{texto_valor(dados_periodontais['padrao_molar_incisivo'])}\n"
            f"Progressão em 5 anos: "
            f"{texto_valor(dados_periodontais['progressao_5_anos'], 'mm')}\n"
            f"Fenótipo: {texto_valor(dados_periodontais['fenotipo'])}\n"
        )

        if dados_periodontais["hba1c"] is not None:

            texto_relatorio += (
                f"HbA1c: {dados_periodontais['hba1c']}%\n"
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

        texto_relatorio += (
        "\n"
        "IDENTIFICAÇÃO DO RELATÓRIO\n"
        f"Caso: {dados_caso['codigo']}\n"
        f"Gerado em: {data_hora_relatorio}\n"
        "Aplicação: Apoio à Decisão Clínica em Periodontia\n"
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

        # RELATÓRIO EM HTML


    
            # Retira o primeiro título do texto,
        # pois o HTML já terá seu próprio título
        texto_html = texto_relatorio.replace(
            "RELATÓRIO INTEGRADO\n\n",
            "",
            1
        )


        # Prepara o texto para ser usado com segurança no HTML
        texto_seguro = escape(texto_html)


        # Cria o HTML formatado
        html_relatorio = f"""
        <!DOCTYPE html>

        <html>

        <head>

            <meta charset="UTF-8">

            <title>Relatório integrado</title>

            <style>

                @page {{
                    size: A4;
                    margin: 20mm;
                }}


                body {{
                    background: #f5f7f5;
                    color: #334a45;
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 40px 20px;
                }}


                h1 {{
                    color: #17352f;
                    font-size: 30px;
                    margin: 8px 0 4px;
                }}


                .relatorio {{
                    background: #ffffff;
                    border: 1px solid #dce4e0;
                    border-radius: 16px;
                    box-shadow: 0 12px 34px rgba(23, 53, 47, 0.08);
                    margin: 0 auto;
                    max-width: 800px;
                    overflow: hidden;
                }}


                .cabecalho {{
                    background: #17352f;
                    color: #e8f1ed;
                    padding: 26px 30px;
                }}


                .cabecalho h1 {{
                    color: #ffffff;
                }}


                .etiqueta {{
                    color: #a9c9bc;
                    font-size: 12px;
                    font-weight: bold;
                    letter-spacing: 1.5px;
                    text-transform: uppercase;
                }}


                .caso {{
                    color: #bed2ca;
                    font-size: 13px;
                    margin: 6px 0 0;
                }}


                pre {{
                    font-family: Arial, sans-serif;
                    font-size: 15px;
                    line-height: 1.6;
                    margin: 0;
                    padding: 28px 30px 34px;
                    white-space: pre-wrap;
                }}


                @media print {{

                    body {{
                        background: #ffffff;
                        padding: 0;
                    }}

                    .relatorio {{
                        border: 0;
                        border-radius: 0;
                        box-shadow: none;
                        max-width: none;
                    }}

                }}

            </style>

        </head>


        <body>

            <main class="relatorio">

                <header class="cabecalho">

                    <div class="etiqueta">PerioDecision</div>

                    <h1>Relatório Integrado</h1>

                    <p class="caso">Caso {codigo_relatorio}</p>

                </header>

                <pre>{texto_seguro}</pre>

            </main>

        </body>

        </html>
        """


        # Nome do arquivo
        nome_arquivo_html = (
            f"relatorio_{dados_caso['codigo']}.html"
        )


        # Botão de download
        st.download_button(
            label="Baixar relatório para impressão",
            data=html_relatorio,
            file_name=nome_arquivo_html,
            mime="text/html"
        )


    else:

        st.warning(
            "O relatório final só poderá ser preparado "
            "quando a avaliação estiver completa."
        )
