function add_carro(){
    container = document.getElementById('form-carro')

    html = "<br> <div class='row'> \
                <div class='col-md'> \
                    <input type='text' placeholder='Modelo' class='form-control' name='carro'> \
                </div> \
                <div class='col-md'> \
                    <input type='text' placeholder='Placa' class='form-control' name='placa'> \
                </div> \
                <div class='col-md'> \
                    <input type='number' placeholder='Ano' class='form-control' name='ano'> \
                </div> \
            </div>"

    container.innerHTML += html
}


function exibir_form(tipo){
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if(tipo == "1"){
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"
    }else if(tipo == "2"){
        add_cliente.style.display = "none"
        att_cliente.style.display = "block"
    }
}


// ── Auto preenche endereço pelo CEP via ViaCEP ──────────────────────────────
function buscar_cep(modo){
    // modo 'add' = formulário de adicionar | modo 'att' = formulário de atualizar
    const id_cep = modo === 'add' ? 'cep-add' : 'cep'
    const sufixo = modo === 'add' ? '-add' : ''

    const cep = document.getElementById(id_cep).value.replace(/\D/g, '')
    if(cep.length !== 8) return

    fetch(`https://viacep.com.br/ws/${cep}/json/`)
    .then(r => r.json())
    .then(data => {
        if(data.erro) return alert('CEP não encontrado.')
        document.getElementById('rua'    + sufixo).value = data.logradouro
        document.getElementById('bairro' + sufixo).value = data.bairro
        document.getElementById('cidade' + sufixo).value = data.localidade
        document.getElementById('estado' + sufixo).value = data.uf
    })
}


// ── Busca dados do cliente selecionado ──────────────────────────────────────
function dados_cliente(){
    cliente    = document.getElementById('cliente-select')
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data

    }).then(function(result){
        return result.json()
    }).then(function(data){
        document.getElementById('form-att-cliente').style.display = 'block'

        // Dados pessoais
        document.getElementById('id').value        = data['cliente_id']
        document.getElementById('nome').value      = data['cliente']['nome']
        document.getElementById('sobrenome').value = data['cliente']['sobrenome']
        document.getElementById('cpf').value       = data['cliente']['cpf']
        document.getElementById('email').value     = data['cliente']['email']
        document.getElementById('telefone').value  = data['cliente']['telefone'] || ''

        // Endereço
        document.getElementById('cep').value    = data['cliente']['cep']    || ''
        document.getElementById('rua').value    = data['cliente']['rua']    || ''
        document.getElementById('numero').value = data['cliente']['numero'] || ''
        document.getElementById('bairro').value = data['cliente']['bairro'] || ''
        document.getElementById('cidade').value = data['cliente']['cidade'] || ''
        document.getElementById('estado').value = data['cliente']['estado'] || ''

        // Carros — limpa antes de renderizar para não duplicar
        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ''

        for(i = 0; i < data['carros'].length; i++){
            div_carros.innerHTML += "\
                <form action='/clientes/update_carro/" + data['carros'][i]['id'] + "' method='POST'>\
                    <div class='row'>\
                        <div class='col-md'>\
                            <input class='form-control' name='carro' type='text' value='" + data['carros'][i]['fields']['carro'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' name='placa' type='text' value='" + data['carros'][i]['fields']['placa'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='ano' value='" + data['carros'][i]['fields']['ano'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='btn btn-lg btn-success' type='submit'>\
                        </div>\
                    </form>\
                    <div class='col-md'>\
                        <a href='/clientes/excluir_carro/" + data['carros'][i]['id'] + "' class='btn btn-lg btn-danger'>EXCLUIR</a>\
                    </div>\
                </div><br>"
        }
    })
}


// ── Atualiza dados do cliente ────────────────────────────────────────────────
function update_cliente(){
    const id        = document.getElementById('id').value
    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

    // Dados pessoais
    const nome      = document.getElementById('nome').value
    const sobrenome = document.getElementById('sobrenome').value
    const email     = document.getElementById('email').value
    const cpf       = document.getElementById('cpf').value
    const telefone  = document.getElementById('telefone').value

    // Endereço
    const cep    = document.getElementById('cep').value
    const rua    = document.getElementById('rua').value
    const numero = document.getElementById('numero').value
    const bairro = document.getElementById('bairro').value
    const cidade = document.getElementById('cidade').value
    const estado = document.getElementById('estado').value

    fetch('/clientes/update_cliente/' + id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            nome, sobrenome, email, cpf, telefone,
            cep, rua, numero, bairro, cidade, estado
        })

    }).then(function(result){
        return result.json()
    }).then(function(data){
        if(data['status'] == '200'){
            console.log('Dados alterados com sucesso')
        }else{
            console.log('Ocorreu algum erro')
        }
    })
}

$(document).ready(function(){
    $('.cpf-mask').mask('000.000.000-00');
});