import streamlit as st
from html import escape
from datetime import datetime


def mostrar_relatorio():
    st.header("Relatório integrado")


    # Pegamos os dados principais já armazenados
    dados_caso = st.session_state["dados_caso"]

    resultado_periodontal = st.session_state["avaliacao"]["periodontal"]

    resultado_findrisc = st.session_state["avaliacao"]["findrisc"]

    resultado_interheart = st.session_state["avaliacao"]["interheart"]

    dados_radiograficos = st.session_state["dados_radiograficos"]

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


    # -------------------------
    # RESULTADO RADIOGRÁFICO
    # -------------------------

    pbl = st.session_state["avaliacao"]["pbl"]

    dente_determinante = dados_radiograficos[
        "dente_determinante"
    ]

    superficie_determinante = dados_radiograficos[
        "superficie_determinante"
]


    if pbl is not None:

        st.write(
            "Perda óssea radiográfica (%PBL):",
            pbl,
            "%"
        )

        st.write(
        "Objeto/dente determinante:",
        dente_determinante
        )

        st.write(
            "Superfície determinante:",
            superficie_determinante
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
        texto_relatorio += (
            "\n"
            "FINDRISC\n"
            f"Pontuação: {resultado_findrisc['pontos']}\n"
            f"Classificação: {resultado_findrisc['classificacao']}\n"
            f"Estimativa em 10 anos: "
            f"{resultado_findrisc['estimativa']}\n"
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

        if (
            dados_clinicos["tabagismo"]
            == "Fumante atual ou nos últimos 12 meses"
        ):

            texto_relatorio += (
                f"Média de cigarros por dia: "
                f"{dados_clinicos['cigarros_dia']}\n"
            )
        
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
            f"CAL máximo: {dados_periodontais['cal']} mm\n"
            f"%PBL: {pbl}%\n"
            f"Dentes perdidos por periodontite: "
            f"{dados_periodontais['dentes_perdidos']}\n"
            f"Profundidade máxima de sondagem: "
            f"{dados_periodontais['sondagem']} mm\n"
            f"Perda óssea vertical máxima: "
            f"{dados_periodontais['perda_vertical']} mm\n"
            f"Furca: {dados_periodontais['furca']}\n"
            f"Defeito do rebordo: "
            f"{dados_periodontais['defeito_rebordo']}\n"
            f"Disfunção mastigatória: "
            f"{dados_periodontais['disfuncao_mastigatoria']}\n"
            f"Mobilidade: {dados_periodontais['mobilidade']}\n"
            f"Dentes remanescentes: "
            f"{dados_periodontais['dentes_remanescentes']}\n"
            f"Colapso de mordida: "
            f"{dados_periodontais['colapso_mordida']}\n"
            f"Migração dentária: "
            f"{dados_periodontais['migracao_dentaria']}\n"
            f"Abertura em leque: "
            f"{dados_periodontais['abertura_leque']}\n"
            f"Percentual de dentes envolvidos: "
            f"{dados_periodontais['percentual_dentes_envolvidos']}%\n"
            f"Padrão molar/incisivo: "
            f"{dados_periodontais['padrao_molar_incisivo']}\n"
            f"Progressão em 5 anos: "
            f"{dados_periodontais['progressao_5_anos']} mm\n"
            f"Fenótipo: {dados_periodontais['fenotipo']}\n"
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
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 40px auto;
                    color: #222222;
                }}


                h1 {{
                    text-align: center;
                    margin-bottom: 30px;
                }}


                pre {{
                    font-family: Arial, sans-serif;
                    font-size: 15px;
                    line-height: 1.6;
                    white-space: pre-wrap;
                }}


                @media print {{

                    body {{
                        max-width: none;
                        margin: 0;
                    }}

                }}

            </style>

        </head>


        <body>

            <h1>Relatório Integrado</h1>

            <pre>{texto_seguro}</pre>

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
