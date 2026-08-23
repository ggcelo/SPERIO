import streamlit as st


def inicializar_session_state():
    #DICIONÁRIO DOS RESULTADOS

    if "avaliacao" not in st.session_state: 
        st.session_state["avaliacao"] = {
            "periodontal": None,
            "findrisc": None,
            "interheart": None,
            "pbl": None
        }

    # DICIONÁRIO DO MÓDULO RADIOGRÁFICO
    if "dados_radiograficos" not in st.session_state:
        st.session_state["dados_radiograficos"] = {
            "nome_arquivo": None,
            "imagem_bytes": None,
            "resultados_dentes": [],
            "pbl_maximo": None,
            "dente_determinante": None,
            "superficie_determinante": None,
            "confirmado": False,
            "imagem_anotada_bytes": None,
            "pbl_calculado": False
        }
    #DICIONÁRIO DOS DADOS DO CASO

    if "dados_caso" not in st.session_state: 
        st.session_state["dados_caso"] = {
            "codigo": None,
            "idade": None,
            "sexo": None
        }
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
    #DICIONARIO DOS DADOS ESPECIFICOS DO FINDRISC

    if "dados_findrisc" not in st.session_state:
        st.session_state["dados_findrisc"] = {
            "atividade_fisica": None,
            "frutas_vegetais": None,
            "medicacao_pressao": None,
            "glicemia_elevada": None,
            "historico_familiar": None
        }
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
