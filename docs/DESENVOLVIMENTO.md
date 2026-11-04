# Desenvolvimento

## Uma única pasta de trabalho

O código e o repositório Git ficam na raiz. Não é necessário manter uma
segunda cópia para publicação. Os arquivos privados permanecem localmente,
protegidos pelo `.gitignore`.

Antes de publicar, execute `scripts/verificar_publicacao.py` e revise
`git diff` e `git diff --cached`. O `.gitignore` não remove arquivos que já
tenham sido incluídos no histórico; o verificador também examina esse histórico.

## Editor de keypoints

Em **Análise radiográfica**, carregue a imagem, execute a análise e abra
**Correção dos keypoints**. Selecione o objeto e arraste um ponto.
O ajuste é registrado na sessão quando o mouse é solto. **Ampliar objeto**
facilita a correção. Para posicionar um ponto ausente, selecione seu nome
e clique na imagem. O número do objeto identifica a detecção, não a numeração FDI.

Os campos X/Y continuam disponíveis em **Ajuste preciso por coordenadas
(opcional)**. Um ponto ausente exige ambas as coordenadas; zero é válido.
Depois de corrigir, clique em **Calcular %PBL com os keypoints revisados**.
As correções invalidam o resultado radiográfico anterior e a classificação
que dependia dele.

As coordenadas usam os pixels da imagem original, inclusive na ampliação.
Trocar de objeto mantém os ajustes. Trocar de imagem ou executar nova análise
substitui as detecções. Os ajustes da sessão não são salvos permanentemente.

- `modulo_radiografico.py`: fluxo, cálculos e imagens do relatório.
- `editor_keypoints.py`: validação e comunicação com o componente Streamlit.
- `componentes/editor_keypoints.js`: seleção, ampliação e arraste em SVG.
- `componentes/editor_keypoints.css`: aparência do editor.

O componente usa a API v2 do Streamlit, sem exigir Node em produção.
Apenas o evento final do arraste é enviado ao Python.

## Verificação manual

Inicie o Streamlit e percorra os questionários e o relatório. Com um modelo
autorizado disponível, execute a análise radiográfica: arraste um ponto,
alterne entre objetos e confira as coordenadas; amplie e repita. Posicione
um ponto ausente, recalcule o %PBL e confira a imagem do relatório.
Teste também outra imagem com o mesmo nome de arquivo.

A planilha de simulações é um recurso local, não distribuído. Comparações
com esse gabarito avaliam regressões da lógica, sem constituir validação
clínica independente.
