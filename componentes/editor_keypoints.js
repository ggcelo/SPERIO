// JavaScript fica restrito à interação. Python é a fonte dos dados e dos cálculos.
export default function ({ parentElement, data, setTriggerValue }) {
    const raiz = parentElement.querySelector(".editor-keypoints");
    // Guarda somente preferências visuais entre reexecuções do mesmo objeto.
    const anterior = raiz.querySelector("select")?.value;
    const focoAnterior = raiz.querySelector("button")?.classList.contains("ativo");
    raiz.innerHTML = `
        <div class="barra">
            <label>Ponto: <select aria-label="Keypoint selecionado"></select></label>
            <button type="button" aria-pressed="false">Ampliar objeto</button>
        </div>
        <div class="quadro">
            <svg xmlns="http://www.w3.org/2000/svg" tabindex="0"
                 role="group" aria-label="Radiografia com keypoints editáveis"></svg>
        </div>
        <p class="situacao" role="status" aria-live="polite"></p>`;
    const seletor = raiz.querySelector("select");
    const botaoFoco = raiz.querySelector("button");
    const svg = raiz.querySelector("svg");
    const situacao = raiz.querySelector(".situacao");
    const ns = "http://www.w3.org/2000/svg";
    const pontos = structuredClone(data.pontos);
    const grupos = {};
    let arraste = null;
    let aguardando = false;
    let ampliado = Boolean(focoAnterior);

    function elemento(nome, atributos, pai = svg) {
        const item = document.createElementNS(ns, nome);
        for (const [chave, valor] of Object.entries(atributos)) item.setAttribute(chave, valor);
        pai.appendChild(item);
        return item;
    }

    elemento("image", { href: data.imagem, width: data.largura, height: data.altura });
    const [x1, y1, x2, y2] = data.caixa;
    elemento("rect", {
        x: x1, y: y1, width: x2 - x1, height: y2 - y1,
        fill: "none", stroke: "#e6c660", "stroke-width": 1.5,
        "vector-effect": "non-scaling-stroke", "pointer-events": "none",
    });

    for (const [nome, ponto] of Object.entries(pontos)) {
        const opcao = document.createElement("option");
        opcao.value = nome;
        opcao.textContent = nome + (ponto === null ? " — não detectado" : "");
        seletor.appendChild(opcao);
        const grupo = elemento("g", { class: "ponto", "data-nome": nome });
        elemento("circle", { class: "alvo", fill: "transparent" }, grupo);
        elemento("circle", { class: "marca", stroke: "white", "stroke-width": 2,
            "vector-effect": "non-scaling-stroke" }, grupo);
        const texto = elemento("text", {}, grupo);
        texto.textContent = nome;
        grupos[nome] = grupo;
    }
    if (anterior && anterior in pontos) seletor.value = anterior;

    // Mantém os alvos legíveis mesmo com a imagem reduzida ou o objeto ampliado.
    function desenhar() {
        const matriz = svg.getScreenCTM();
        if (!matriz || matriz.a <= 0) return;
        const unidade = 1 / matriz.a;
        for (const [nome, grupo] of Object.entries(grupos)) {
            const ponto = pontos[nome];
            grupo.style.display = ponto === null ? "none" : "";
            if (ponto === null) continue;
            grupo.setAttribute("transform", `translate(${ponto[0]} ${ponto[1]})`);
            grupo.querySelector(".alvo").setAttribute("r", 14 * unidade);
            const marca = grupo.querySelector(".marca");
            marca.setAttribute("r", (nome === seletor.value ? 7 : 5) * unidade);
            marca.setAttribute("fill", nome === seletor.value ? "#f3c851" : "#e15353");
            const texto = grupo.querySelector("text");
            texto.setAttribute("x", 10 * unidade);
            texto.setAttribute("y", -10 * unidade);
            texto.style.fontSize = `${13 * unidade}px`;
            texto.style.strokeWidth = `${3 * unidade}px`;
        }
        // Se dois pontos coincidirem, o escolhido no painel fica acessível.
        svg.appendChild(grupos[seletor.value]);
    }

    function orientar() {
        situacao.textContent = pontos[seletor.value] === null
            ? `${seletor.value}: clique na imagem para posicionar o ponto não detectado.`
            : `${seletor.value}: arraste o ponto. Ao soltar, o ajuste será registrado na sessão.`;
    }

    function ajustarVista() {
        const margem = Math.max(x2 - x1, y2 - y1) * .15;
        const esquerda = Math.max(0, x1 - margem);
        const topo = Math.max(0, y1 - margem);
        const direita = Math.min(data.largura, x2 + margem);
        const base = Math.min(data.altura, y2 + margem);
        const recorte = [esquerda, topo, direita - esquerda, base - topo];
        svg.setAttribute("viewBox", (ampliado && recorte[2] > 0 && recorte[3] > 0
            ? recorte : [0, 0, data.largura, data.altura]).join(" "));
        botaoFoco.classList.toggle("ativo", ampliado);
        botaoFoco.setAttribute("aria-pressed", String(ampliado));
        botaoFoco.textContent = ampliado ? "Mostrar imagem inteira" : "Ampliar objeto";
        desenhar();
    }

    // Converte a posição do mouse para pixels originais, incluindo escala e recorte.
    function coordenadas(evento) {
        const posicao = new DOMPoint(evento.clientX, evento.clientY)
            .matrixTransform(svg.getScreenCTM().inverse());
        return [
            Math.max(0, Math.min(data.largura - 1, posicao.x)),
            Math.max(0, Math.min(data.altura - 1, posicao.y)),
        ].map(valor => Math.round(valor * 100) / 100);
    }

    function enviar(nome) {
        aguardando = true;
        seletor.disabled = true;
        botaoFoco.disabled = true;
        situacao.textContent = "Registrando ajuste na sessão…";
        setTriggerValue("edicao", {
            versao: data.versao, objeto: data.objeto, nome,
            x: pontos[nome][0], y: pontos[nome][1],
        });
    }

    seletor.onchange = () => { desenhar(); orientar(); };
    botaoFoco.onclick = () => { ampliado = !ampliado; ajustarVista(); };

    svg.onpointerdown = evento => {
        if (aguardando || arraste || evento.button !== 0) return;
        const grupo = evento.target.closest(".ponto");
        const nome = grupo ? grupo.dataset.nome : seletor.value;
        if (!grupo && pontos[nome] !== null) return;
        // Ignora cliques nas faixas vazias ao redor da imagem.
        const posicao = new DOMPoint(evento.clientX, evento.clientY)
            .matrixTransform(svg.getScreenCTM().inverse());
        if (!grupo && (posicao.x < 0 || posicao.x >= data.largura ||
                       posicao.y < 0 || posicao.y >= data.altura)) return;
        evento.preventDefault();
        svg.focus({ preventScroll: true });
        seletor.value = nome;
        arraste = { nome, inicio: pontos[nome]?.slice() ?? null, ponteiro: evento.pointerId };
        grupos[nome].classList.add("arrastando");
        svg.setPointerCapture(evento.pointerId);
        if (!grupo) pontos[nome] = coordenadas(evento);
        desenhar();
    };
    svg.onpointermove = evento => {
        if (!arraste || evento.pointerId !== arraste.ponteiro) return;
        pontos[arraste.nome] = coordenadas(evento);
        desenhar();
    };
    svg.onpointerup = evento => {
        if (!arraste || evento.pointerId !== arraste.ponteiro) return;
        const { nome, inicio } = arraste;
        arraste = null;
        grupos[nome].classList.remove("arrastando");
        svg.releasePointerCapture(evento.pointerId);
        const ponto = pontos[nome];
        if (inicio === null || ponto[0] !== inicio[0] || ponto[1] !== inicio[1]) enviar(nome);
        else orientar();
    };
    function cancelar() {
        if (!arraste) return;
        const { nome, inicio, ponteiro } = arraste;
        arraste = null;
        pontos[nome] = inicio;
        grupos[nome].classList.remove("arrastando");
        if (svg.hasPointerCapture(ponteiro)) svg.releasePointerCapture(ponteiro);
        desenhar();
        orientar();
    }
    svg.onpointercancel = cancelar;
    svg.onlostpointercapture = cancelar;
    svg.onkeydown = evento => { if (evento.key === "Escape") cancelar(); };

    ajustarVista();
    orientar();
    const observador = new ResizeObserver(desenhar);
    observador.observe(svg);
    // O Streamlit chama esta limpeza antes de remontar o componente.
    return () => observador.disconnect();
}
