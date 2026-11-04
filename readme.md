# SPERIO

Aplicação de apoio à decisão clínica em Periodontia, desenvolvida em Python com Streamlit. Integra classificação periodontal AAP/EFP, FINDRISC, INTERHEART e análise radiográfica de perda óssea periodontal.

## Funcionalidades

- Avaliação periodontal e integração de fatores de risco.
- Questionários FINDRISC e INTERHEART.
- Integração com modelo radiográfico externo, revisão visual dos keypoints e cálculo da perda óssea radiográfica (%PBL).
- Geração de relatório e importação/exportação de planilhas de casos.

## Executar localmente

Use Python 3.11. No PowerShell, dentro da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run main.py
```

Se o ambiente `.venv` já existir, utilize-o diretamente.

## Modelo e dados externos

Este repositório publica o código da aplicação. **Os pesos do modelo de IA dos autores e a planilha de simulações não são distribuídos.** O modelo radiográfico é um recurso externo de terceiros; este projeto contém a integração com ele, sem reivindicar sua autoria.

A integração radiográfica utiliza o modelo externo Perio-KPT, associado ao trabalho de Banks et al. (2025), [*Periodontal Bone Loss Analysis via Keypoint Detection With Heuristic Post-Processing*](https://arxiv.org/abs/2503.13477). A autoria do modelo e da pesquisa original pertence aos respectivos autores.

**Para utilizar o modelo radiográfico, acesse o [repositório original do Perio-KPT](https://github.com/Banksylel/Bone-Loss-Keypoint-Detection-Code) e siga as orientações e os links disponibilizados pelos autores para obter os pesos**, respeitando as condições de uso aplicáveis. O SPERIO não fornece nem baixa automaticamente esses arquivos.

Após obter os pesos compatíveis, coloque o arquivo em `models/perio_kpt_oficial_fold0_best.pt`. Veja também [models/README.md](models/README.md). Sem esse arquivo, a interface informa sua ausência; os demais módulos não dependem desses pesos.

As planilhas locais, os pesos, ambientes e backups são excluídos do versionamento pelo `.gitignore`.

## Estrutura

```text
main.py                     Entrada e navegação da aplicação
state.py                    Estado da sessão
modulo_periodontal.py       Avaliação periodontal
modulo_findrisc.py          Questionário FINDRISC
modulo_interheart.py        Questionário INTERHEART
modulo_radiografico.py      Integração radiográfica e cálculo de %PBL
editor_keypoints.py         Comunicação Python com o editor visual
componentes/                JavaScript e CSS do editor
planilhas.py                Importação, exportação e comparação de casos
relatorio.py                Geração e apresentação do relatório
interface.css               Estilos da aplicação
relatorio_impressao.css      Estilos de impressão
models/README.md            Orientações para o modelo externo
.streamlit/config.toml      Tema do Streamlit
scripts/                    Verificação dos arquivos para publicação
docs/                       Documentação de desenvolvimento
```

Detalhes do editor estão em [docs/DESENVOLVIMENTO.md](docs/DESENVOLVIMENTO.md).

## Antes de publicar

```powershell
.\.venv\Scripts\python.exe scripts/verificar_publicacao.py
git status
```

O verificador confere nomes de arquivos versionados, arquivos novos não ignorados e objetos no histórico Git local, procurando modelos, planilhas e arquivos privados. Não substitui a revisão do conteúdo do código.

## Contexto de uso

Projeto de pesquisa e desenvolvimento. A concordância com simulações internas não constitui validação clínica independente. A aplicação não substitui a avaliação de um profissional de saúde.
