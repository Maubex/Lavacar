function add_carro(){
    container = document.getElementById('form-carro')

    html = `<br>
    <div class='row'>
        <div class='col-md'>
            <input type='text' placeholder='Modelo (Ex: Honda Civic)' class='form-control' name='carro'>
        </div>
        <div class='col-md'>
            <input type='text' placeholder='Placa (ABC1D23)' class='form-control placa-mask' name='placa' style='text-transform: uppercase;'>
        </div>
        <div class='col-md'>
            <input type='number' placeholder='Ano' class='form-control' name='ano'>
        </div>
        <div class='col-md'>
            <select class='form-control select2' name='tipo'>
                <option value=''>Tipo</option>
                <option value='hatch'>Hatch</option>
                <option value='sedan'>Sedan</option>
                <option value='suv'>SUV</option>
                <option value='caminhonete'>Caminhonete</option>
                <option value='moto'>Moto</option>
                <option value='van'>Van</option>
                <option value='pickup'>Pickup</option>
                <option value='esportivo'>Esportivo</option>
                <option value='outro'>Outro</option>
            </select>
        </div>
        <div class='col-md'>
            <select class='form-control select2' name='cor'>
                <option value=''>Cor</option>
                <option value='preto'>Preto</option>
                <option value='branco'>Branco</option>
                <option value='prata'>Prata</option>
                <option value='cinza'>Cinza</option>
                <option value='vermelho'>Vermelho</option>
                <option value='azul'>Azul</option>
                <option value='verde'>Verde</option>
                <option value='amarelo'>Amarelo</option>
                <option value='outro'>Outro</option>
            </select>
        </div>
    </div>`

    container.innerHTML += html

    // Ajuste: Aplica as máscaras nos novos campos
    $('.placa-mask').mask('AAA0A00');

    // Ativa o Select2 nos novos selects
    $('.select2').select2({
        placeholder: 'Pesquisar...',
        allowClear: true
    })
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

        // Ajuste: Aplica máscaras nos campos carregados
        $('.cpf-mask').mask('000.000.000-00');
        $('.tel-mask').mask('(00) 00000-0000');
        $('.cep-mask').mask('00000-000');

        // Carros — limpa antes de renderizar para não duplicar
        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ''

        for(i = 0; i < data['carros'].length; i++){
            div_carros.innerHTML += `
                <form action='/clientes/update_carro/${data['carros'][i]['id']}' method='POST'>
                    <div class='row'>
                        <div class='col-md'>
                            <input class='form-control' name='carro' type='text' value='${data['carros'][i]['fields']['carro']}'>
                        </div>
                        <div class='col-md'>
                            <input class='form-control placa-mask' name='placa' type='text' value='${data['carros'][i]['fields']['placa']}' style='text-transform: uppercase;'>
                        </div>
                        <div class='col-md'>
                            <input class='form-control' type='number' name='ano' value='${data['carros'][i]['fields']['ano']}'>
                        </div>
                        <div class='col-md'>
                            <select class='form-control select2' name='tipo'>
                                <option value=''>Tipo</option>
                                <option value='hatch'       ${data['carros'][i]['fields']['tipo'] == 'hatch'       ? 'selected' : ''}>Hatch</option>
                                <option value='sedan'       ${data['carros'][i]['fields']['tipo'] == 'sedan'       ? 'selected' : ''}>Sedan</option>
                                <option value='suv'         ${data['carros'][i]['fields']['tipo'] == 'suv'         ? 'selected' : ''}>SUV</option>
                                <option value='caminhonete' ${data['carros'][i]['fields']['tipo'] == 'caminhonete' ? 'selected' : ''}>Caminhonete</option>
                                <option value='moto'        ${data['carros'][i]['fields']['tipo'] == 'moto'        ? 'selected' : ''}>Moto</option>
                                <option value='van'         ${data['carros'][i]['fields']['tipo'] == 'van'         ? 'selected' : ''}>Van</option>
                                <option value='pickup'      ${data['carros'][i]['fields']['tipo'] == 'pickup'      ? 'selected' : ''}>Pickup</option>
                                <option value='esportivo'   ${data['carros'][i]['fields']['tipo'] == 'esportivo'   ? 'selected' : ''}>Esportivo</option>
                                <option value='outro'       ${data['carros'][i]['fields']['tipo'] == 'outro'       ? 'selected' : ''}>Outro</option>
                            </select>
                        </div>
                        <div class='col-md'>
                            <select class='form-control select2' name='cor'>
                                <option value=''>Cor</option>
                                <option value='preto'    ${data['carros'][i]['fields']['cor'] == 'preto'    ? 'selected' : ''}>Preto</option>
                                <option value='branco'   ${data['carros'][i]['fields']['cor'] == 'branco'   ? 'selected' : ''}>Branco</option>
                                <option value='prata'    ${data['carros'][i]['fields']['cor'] == 'prata'    ? 'selected' : ''}>Prata</option>
                                <option value='cinza'    ${data['carros'][i]['fields']['cor'] == 'cinza'    ? 'selected' : ''}>Cinza</option>
                                <option value='vermelho' ${data['carros'][i]['fields']['cor'] == 'vermelho' ? 'selected' : ''}>Vermelho</option>
                                <option value='azul'     ${data['carros'][i]['fields']['cor'] == 'azul'     ? 'selected' : ''}>Azul</option>
                                <option value='verde'    ${data['carros'][i]['fields']['cor'] == 'verde'    ? 'selected' : ''}>Verde</option>
                                <option value='amarelo'  ${data['carros'][i]['fields']['cor'] == 'amarelo'  ? 'selected' : ''}>Amarelo</option>
                                <option value='outro'    ${data['carros'][i]['fields']['cor'] == 'outro'    ? 'selected' : ''}>Outro</option>
                            </select>
                        </div>
                        <div class='col-md'>
                            <input class='btn btn-lg btn-success' type='submit'>
                        </div>
                    </div>
                </form>
                <div class='row'>
                    <div class='col-md'>
                        <a href='/clientes/excluir_carro/${data['carros'][i]['id']}' class='btn btn-lg btn-danger'>EXCLUIR</a>
                    </div>
                </div><br>`
        }

        // Ajuste: Aplica máscara nas placas dos carros carregados
        $('.placa-mask').mask('AAA0A00');

        // Ativa Select2 nos selects dos carros
        $('.select2').select2({
            placeholder: 'Pesquisar...',
            allowClear: true
        })
    })
}


// ── Atualiza dados do cliente ────────────────────────────────────────────────
function update_cliente(){
    const id         = document.getElementById('id').value
    const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value

    // Ajuste: Captura os dados limpando as máscaras antes de enviar para o Django
    const nome      = document.getElementById('nome').value
    const sobrenome = document.getElementById('sobrenome').value
    const email     = document.getElementById('email').value
    const cpf       = document.getElementById('cpf').value.replace(/\D/g, '')
    const telefone  = document.getElementById('telefone').value.replace(/\D/g, '')

    // Endereço
    const cep    = document.getElementById('cep').value.replace(/\D/g, '')
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
            alert('Dados alterados com sucesso')
            location.reload() // Ajuste: recarrega para atualizar a tela
        }else{
            // Ajuste: exibe o erro real vindo da View do Django
            alert('Erro: ' + data['erro'])
        }
    })
}

// Inicialização das máscaras ao carregar a página
$(document).ready(function(){
    $('.cpf-mask').mask('000.000.000-00');
    $('.tel-mask').mask('(00) 00000-0000');
    $('.cep-mask').mask('00000-000');
    $('.placa-mask').mask('AAA0A00');

    // Ajuste: Limpa máscaras no formulário de cadastro antes de enviar
    $('#adicionar-cliente form').on('submit', function() {
        $('.cpf-mask, .tel-mask, .cep-mask').each(function() {
            $(this).val($(this).val().replace(/\D/g, ''));
        });
    });
});