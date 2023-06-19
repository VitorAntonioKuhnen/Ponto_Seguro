var crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

$(document).ready(function (e) {
    $('#cadastroEscala').submit(function (e) {
        $('#loading').removeClass('disabled');
        e.preventDefault();
        let formulario = $(this).serializeArray();
        console.log(formulario);


        // Envie a solicitação AJAX para a View do Django
        $.ajax({
            url: '/cadastroEscala/', // Substitua pelo URL correto da sua View
            type: 'POST', // Ou 'GET', dependendo da configuração da sua View
            headers: { 'X-CSRFToken': crf_token },
            data: formulario,
            success: function (response) {
                // Verifique o JSON de resposta e atualize a página conforme necessário
                $('#retornoMsg').text(response.mensage); // Define a mensagem na tag HTML
                $('#mensage').addClass(response.tipo); // Define o tipo na classe
                $('#mensage').addClass('show'); // Define o tipo na classe
                if (response.sit == 'OK') {
                    console.log(response.escala)
                    adicionaLinha(response.escala.id, response.escala.nmEscala, 
                                  response.escala.horEnt1, response.escala.horSai2, 
                                  response.escala.horEnt3, response.escala.horSai4, 
                                  response.escala.segunda, response.escala.terca, 
                                  response.escala.quarta, response.escala.quinta, 
                                  response.escala.sexta, response.escala.sabado, 
                                  response.escala.domingo, response.escala.status, 
                                  response.escala.statusTab)
                    //Fecha o Modal
                    $('#btnCancelar').click();

                    //Limpa os Inputs
                    $('#inputCad').val('');
                    $('#ent1Cad').val('');
                    $('#sai1Cad').val('');
                    $('#ent2Cad').val('');
                    $('#sai2Cad').val('');

                    // Desmarca Dia da Semana 
                    $('#segCad').prop('checked', false);
                    $('#tercCad').prop('checked', false);
                    $('#quartCad').prop('checked', false);
                    $('#quintCad').prop('checked', false);
                    $('#sextCad').prop('checked', false);
                    $('#sabCad').prop('checked', false);
                    $('#dominCad').prop('checked', false);
                }
                $('#loading').addClass('disabled');
            },
            error: function (xhr, status, error) {
                console.log(error); // Lidar com erros de solicitação, se necessário
            }
        });

        // Remove o a tag de Show após mostrar    
        setTimeout(() => {
            $('#mensage').removeClass('show');
            $('#mensage').removeClass('text-bg-danger');
            $('#mensage').removeClass('text-bg-warning');
            $('#mensage').removeClass('text-bg-primary');
            $('#mensage').removeClass('text-bg-success');
            $('#mensage').removeClass('text-bg-info');
        }, 5000);
        return false; // Evita o envio do formulário tradicional
    });

    function adicionaLinha(id, nmEscala, horEnt1, horSai2, horEnt3, horSai4, segunda, terca, quarta, quinta, sexta, sabado, domingo, status, statusTab) {
        var linha = `
        <tr>
        <th scope="row">${id}</th>
        <td id="escala${id}">${nmEscala}</td>
        <td id="status${id}">
            ${statusTab}
        </td>
        <td class="d-flex justify-content-center" >
          
          <button class="btn-table" type="button" data-bs-toggle="modal" data-bs-target="#alterar${id}">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="btn-icon text-primary bi bi-pencil-square" viewBox="0 0 16 16">
              <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"></path>
              <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5v11z"></path>
            </svg>
          </button>


          <!-- Modal do Button Editar-->
          <div class="modal fade" id="alterar${id}" tabindex="-1" aria-labelledby="cadastrarEscalaModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg"> 
              <div class="modal-content">
                <!-- Modal Header -->
                <div class="modal-header pl-5">
                  <h5 class="modal-title fs-5" id="titleModalLabel">Alterar Escala</h5>
                  <button title="Fechar" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <!-- Modal body -->
                <div class="modal-body">
                  <div class="container-fluid">
                    <div class="row">
                      <div class="col-12">
                        <!-- Container -->
                        <div id="container" class="container col-12 col-sm-12">
                          <h4>Escala</h4>
                          <br />
                          <!-- Content -->
                          <div class="content-modal rounded">
                            <div class="modal-body">
                              <div>
                                <div class="mb-3">
                                  <div class="row mb-3">
                                    <label for="input${id}" class="col-sm-2 col-form-label">Descrição</label>
                                    <div class="col-sm-10">
                                      <input type="" name="nmEscala${id}" class="form-control" id="input${id}" value="${nmEscala}">
                                      <div class=" d-flex justify-content-between gap-2 times ml-5">
                                        <div>
                                          <label for="ent1${id}" class="col-form-label">1º Entrada</label>
                                          <input type="time" class="form-control" id="ent1${id}" name="ent1${id}" value="${horEnt1}">
                                        </div>
                                        <div>
                                          <label for="sai1${id}" class="col-form-label">1º Saida</label>
                                          <input type="time" class="form-control" id="sai1${id}" name="sai1${id}" value="${horSai2}">
                                        </div>
                                        <div>
                                          <label for="ent2${id}" class="col-form-label">2º Entrada</label>
                                          <input type="time" class="form-control" id="ent2${id}" name="ent2${id}" value="${horEnt3}">
                                        </div>
                                        <div>
                                          <label for="sai2${id}" class="col-form-label">2º Saída</label>
                                          <input type="time" class="form-control" id="sai2${id}" name="sai2${id}" value="${horSai4}">
                                        </div>
                                      </div>
                                    </div>
                                  </div>

                                </div>
                                <div class="row mb-3">
                                  <div class="col-sm-10 offset-sm-2">
                                    <b>Dias da Semana</b>
                                    <div class=" d-flex justify-content-center gap-3 times pb-2">
                                      <div>
                                        <label class="form-check-label" for="seg${id}">
                                          Segunda
                                        </label>
                                        <input name="seg${id}" class="form-check-input" type="checkbox" id="seg${id}" ${segunda}/>
                                      </div>
                                      <div>
                                        <label class="form-check-label" for="terc${id}">
                                          Terça
                                        </label>
                                        <input name="terc${id}" class="form-check-input" type="checkbox" id="terc${id}" ${terca}/>
                                      </div>
                                      <div>
                                        <label class="form-check-label" for="quart${id}">
                                          Quarta
                                        </label>
                                        <input name="quart${id}" class="form-check-input" type="checkbox" id="quart${id}"  ${quarta}/>
                                      </div>
                                      <div>
                                        <label class="form-check-label" for="quint${id}">
                                          Quinta
                                        </label>
                                        <input name="quint${id}" class="form-check-input" type="checkbox" id="quint${id}"  ${quinta}/>
                                      </div>
                                      <div>
                                        <label class="form-check-label" for="sext${id}">
                                          Sexta
                                        </label>
                                        <input name="sext${id}" class="form-check-input" type="checkbox" id="sext${id}"  ${sexta}/>
                                      </div>
                                      <div>
                                        <label class="form-check-label" for="sab${id}">
                                          Sábado
                                        </label>
                                        <input name="sab${id}" class="form-check-input" type="checkbox" id="sab${id}"   ${sabado}/>
                                      </div>
                                      <div>
                                        <label class="form-check-label" for="domin${id}">
                                          Domingo
                                        </label>
                                        <input name="domin${id}" class="form-check-input" type="checkbox" id="domin${id}"  ${domingo} />
                                      </div>
                                    </div>
                                    <b>Situação</b>
                                    <div class="form-check">
                                      <input name="sitEscala${id}" class="form-check-input" type="checkbox" id="sitEscala${id}"  ${status}/>
                                      <label class="form-check-label" for="sitEscala${id}">
                                        Ativar
                                      </label>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <!-- Modal footer -->
                              <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button name="btAlteraEscala" onclick="altEscala(event, ${id})" type="button" class="btn btn-success px-4">Alterar</button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
      </td>
    </tr>
        `
    $('#tabelaEscala tbody').append(linha)    
    }

    // Verifica se o botão clicado foi o de "Exportar"
    $('#btnExportar').click(function () {
        buttonAction = 'exportar';
        $('#loading').removeClass('disabled');
        $('#historicoExport').data('ajax-action', buttonAction);
    });

    // Verifica se o botão clicado foi o de "Buscar"
    $('#buscar').click(function () {
        buttonAction = 'buscar';
        $('#historicoExport').data('ajax-action', buttonAction);
    });

    $('#historicoExport').submit(function (e) {


        // Obtém o formulário
        var form = $(this);

        // Obtém o valor do atributo data-ajax-action do formulário
        var action = form.data('ajax-action');

        // Verifica a ação e executa o código correspondente
        if (action === 'exportar') {
            // Código para a ação de busca
            let formulario = form.serializeArray();
            formulario.push({ name: 'exportar' })
            console.log(formulario);

            // Envie a solicitação AJAX para a View do Django
            $.ajax({
                url: '/historico/', // URL da View
                type: 'GET', // 'POST' Ou 'GET', dependendo da configuração da View
                headers: { 'X-CSRFToken': crf_token },
                data: formulario,
                success: function (response) {
                    // Verifique o JSON de resposta e atualize a página conforme necessário
                    $('#retornoMsg').text(response.mensage); // Define a mensagem na tag HTML
                    $('#mensage').addClass(response.tipo); // Define o tipo na classe
                    $('#mensage').addClass('show'); // Define o tipo na classe
                    if (response.sit == 'OK') {

                        if (response.pdf_base64) {
                            // Converte o arquivo PDF de base64 para Blob
                            var pdfBlob = b64toBlob(response.pdf_base64, 'application/pdf');

                            // Cria uma URL para o Blob
                            var pdfUrl = URL.createObjectURL(pdfBlob);

                            // Cria um link para baixar o arquivo
                            var downloadLink = document.createElement('a');
                            downloadLink.href = pdfUrl;
                            downloadLink.download = 'CartaoPonto.pdf';

                            // Simula um clique no link para iniciar o download
                            downloadLink.click();

                            // Libera a URL e remove o link
                            URL.revokeObjectURL(pdfUrl);
                            downloadLink.remove();
                        }
                    }
                    $('#loading').addClass('disabled');
                },
                error: function (xhr, status, error) {
                    console.log(error); // Lidar com erros de solicitação, se necessário
                }

            });

            // Remove o a tag de Show após mostrar    
            setTimeout(() => {

                $('#mensage').removeClass('show');
                $('#mensage').removeClass('text-bg-danger');
                $('#mensage').removeClass('text-bg-warning');
                $('#mensage').removeClass('text-bg-primary');
                $('#mensage').removeClass('text-bg-success');
                $('#mensage').removeClass('text-bg-info');
            }, 5000);
            return false;
        }
    });
    function b64toBlob(b64Data, contentType) {
        contentType = contentType || '';
        var sliceSize = 512;
        var byteCharacters = atob(b64Data);
        var byteArrays = [];

        for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            var slice = byteCharacters.slice(offset, offset + sliceSize);

            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            var byteArray = new Uint8Array(byteNumbers);

            byteArrays.push(byteArray);
        }

        var blob = new Blob(byteArrays, { type: contentType });
        return blob;
    }


});

function altEscala(e, id) {
    $('#loading').removeClass('disabled');
    e.preventDefault();
    let formulario = $('#alteraEscala').serializeArray();
    console.log(formulario);

    // Envie a solicitação AJAX para a View do Django
    $.ajax({
        url: '/alteraEscala/' + id + '/', // Substitua pelo URL correto da sua View
        type: 'POST', // Ou 'GET', dependendo da configuração da sua View
        headers: { 'X-CSRFToken': crf_token },
        data: formulario,
        success: function (response) {
            // Verifique o JSON de resposta e atualize a página conforme necessário
            $('#retornoMsg').text(response.mensage); // Define a mensagem na tag HTML
            $('#mensage').addClass(response.tipo); // Define o tipo na classe
            $('#mensage').addClass('show'); // Define o tipo na classe
            $('#loading').addClass('disabled');
            if (response.sit == 'OK') {
                $('#escala' + id).text(response.escala);
                $('#status' + id).text(response.status);
            }
        },
        error: function (xhr, status, error) {
            console.log(error); // Lidar com erros de solicitação, se necessário
        }

    });

    // Remove o a tag de Show após mostrar
    setTimeout(() => {
        $('#mensage').removeClass('show');
        $('#mensage').removeClass('text-bg-danger');
        $('#mensage').removeClass('text-bg-warning');
        $('#mensage').removeClass('text-bg-primary');
        $('#mensage').removeClass('text-bg-success');
        $('#mensage').removeClass('text-bg-info');
    }, 5000);
    return false; // Evita o envio do formulário tradicional
    // });

};




function altUsuario(e, id) {
    $('#loading').removeClass('disabled');
    e.preventDefault();
    let formulario = $('#altUsuario').serializeArray();
    console.log(formulario);

    // Envie a solicitação AJAX para a View do Django
    $.ajax({
        url: '/altUsuario/' + id + '/', // Substitua pelo URL correto da sua View
        type: 'POST', // Ou 'GET', dependendo da configuração da sua View
        headers: { 'X-CSRFToken': crf_token },
        data: formulario,
        success: function (response) {
            // Verifique o JSON de resposta e atualize a página conforme necessário
            $('#retornoMsg').text(response.mensage); // Define a mensagem na tag HTML
            $('#mensage').addClass(response.tipo); // Define o tipo na classe
            $('#mensage').addClass('show'); // Define o tipo na classe
            $('#loading').addClass('disabled');
            if (response.sit == 'OK') {
                $('#nomeCompleto' + id).text(response.nomeComp);
                $('#escala' + id).text(response.escala);
                $('#email' + id).text(response.email);
                $('#cargo' + id).text(response.cargo);
            }
        },
        error: function (xhr, status, error) {
            console.log(error); // Lidar com erros de solicitação, se necessário
        }

    });

    // Remove o a tag de Show após mostrar
    setTimeout(() => {
        $('#mensage').removeClass('show');
        $('#mensage').removeClass('text-bg-danger');
        $('#mensage').removeClass('text-bg-warning');
        $('#mensage').removeClass('text-bg-primary');
        $('#mensage').removeClass('text-bg-success');
        $('#mensage').removeClass('text-bg-info');
    }, 5000);
    return false; // Evita o envio do formulário tradicional
    // });

};