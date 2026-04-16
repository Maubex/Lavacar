// ── Busca ao pressionar Enter ────────────────────
function busca_enter(event) {
    if (event.key === 'Enter') buscar_atendimento()
}


// ── Busca principal por placa, CPF ou ID ─────────
function buscar_atendimento() {
    const query      = document.getElementById('busca-input').value.trim()
    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]')
                       ? document.querySelector('[name=csrfmiddlewaretoken]').value
                       : getCookie('csrftoken')

    if (!query) return

    const data = new FormData()
    data.append('query', query)

    fetch('/servicos/buscar/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token },
        body: data
    })
    .then(r => r.json())
    .then(data => {
        if (data['status'] == '404') {
            exibir_nao_encontrado(query)
            return
        }
        if (data['tipo'] == 'placa') {
            exibir_card_carro(data['carro'])
        }
        if (data['tipo'] == 'cliente') {
            exibir_lista_carros(data['carros'], data['cliente'])
        }
    })
}


// ── Não encontrado — mostra botão de cadastrar ───
function exibir_nao_encontrado(query) {
    const div = document.getElementById('resultado-busca')
    div.innerHTML = `
        <div class="resultado-box nao-encontrado">
            <p>❌ Nenhum resultado encontrado para <strong>${query}</strong></p>
            <div class="row mt-3">
                <div class="col-md-6">
                    <a href="/servicos/cadastrar-carro/?placa=${query}" class="btn-principal w-100 text-center d-block">
                        + Cadastrar esse carro
                    </a>
                </div>
                <div class="col-md-6">
                    <a href="/clientes/" class="btn-secundario w-100 text-center d-block">
                        + Cadastrar cliente
                    </a>
                </div>
            </div>
        </div>`
}


// ── Card do carro com histórico e botões ─────────
function exibir_card_carro(carro) {
    const div = document.getElementById('resultado-busca')

    let historico_html = ''
    if (!carro.historico || carro.historico.length === 0) {
        historico_html = `
            <tr>
                <td colspan="5" class="text-center text-muted py-3">
                    Nenhum serviço registrado ainda.
                </td>
            </tr>`
    } else {
        carro.historico.forEach(h => {
            // Badge dinâmico baseado no tipo
            let badge = `<span class="badge-os">${h.tipo}</span>`
            if (h.tipo === 'Lavagem') {
                badge = `<span class="badge-lavagem">🚿 Lavagem</span>`
            } else if (h.tipo === 'Estética') {
                badge = `<span class="badge-estetica">✨ Estética</span>`
            } else if (h.tipo === 'OS') {
                badge = `<span class="badge-os">🧾 OS</span>`
            }

            // Status da OS se existir
            const status = h.status
                ? `<span class="badge-status">${h.status}</span>`
                : ''

            historico_html += `
                <tr>
                    <td>${badge}</td>
                    <td>${h.descricao}</td>
                    <td>R$ ${h.valor}</td>
                    <td>${h.data}</td>
                    <td>${status}</td>
                </tr>`
        })
    }

    div.innerHTML = `
        <div class="resultado-box">

            <!-- Info do carro -->
            <div class="carro-info">
                <div class="row">
                    <div class="col-md-8">
                        <h3 class="carro-placa">${carro.placa}</h3>
                        <p class="carro-detalhe">
                            ${carro.modelo || 'Modelo não informado'} &nbsp;•&nbsp;
                            ${carro.tipo  || ''}  &nbsp;•&nbsp;
                            ${carro.cor   || ''}  &nbsp;•&nbsp;
                            ${carro.ano   || 'Ano não informado'}
                        </p>
                        <p class="carro-cliente">👤 ${carro.cliente}</p>
                    </div>
                    <div class="col-md-4 text-right">
                        <a href="/servicos/carro/${carro.id}/nova/" class="btn-servico btn-lavagem">
                            🧾 Nova OS
                        </a>
                    </div>
                </div>
            </div>

            <!-- Histórico -->
            <hr>
            <h5>📋 Histórico de Serviços</h5>
            <div class="table-responsive">
                <table class="table table-sm historico-table">
                    <thead>
                        <tr>
                            <th>Tipo</th>
                            <th>Serviço</th>
                            <th>Valor</th>
                            <th>Data</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${historico_html}
                    </tbody>
                </table>
            </div>

        </div>`
}


// ── Lista de carros do cliente ───────────────────
function exibir_lista_carros(carros, cliente) {
    const div = document.getElementById('resultado-busca')

    let carros_html = ''
    carros.forEach(c => {
        carros_html += `
            <div onclick="selecionar_carro(${c.id})" class="col-md-4 card-carro-select">
                <p class="text-card">🚗 ${c.modelo || c.placa}</p>
                <small>${c.placa} &nbsp;•&nbsp; ${c.tipo || ''} &nbsp;•&nbsp; ${c.cor || ''}</small>
            </div>`
    })

    div.innerHTML = `
        <div class="resultado-box">
            <h5>👤 ${cliente.nome} ${cliente.sobrenome} — Selecione o carro:</h5>
            <br>
            <div class="row">
                ${carros_html}
            </div>
        </div>`
}


// ── Seleciona carro da lista do cliente ──────────
function selecionar_carro(carro_id) {
    fetch(`/servicos/carro/${carro_id}/json/`)
    .then(r => r.json())
    .then(data => exibir_card_carro(data['carro']))
}


// ── Helper: pega cookie CSRF ─────────────────────
function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim()
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.split('=')[1])
            }
        })
    }
    return cookieValue
}