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
                // if (response.mensage) {
                $('#retornoMsg').text(response.mensage); // Define a mensagem na tag HTML
                // }
                // if (response.tipo) {
                $('#mensage').addClass(response.tipo); // Define o tipo na classe
                $('#mensage').addClass('show'); // Define o tipo na classe
                if (response.sit == 'OK'){

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
        // });





    });

    // $('#btExport').click(function(e) {
          // Evento de clique do botão "Exportar"
        $('#btnExportar').click(function() {
            buttonAction = 'exportar';
            $('#loading').removeClass('disabled');
            $('#historicoExport').data('ajax-action', buttonAction);
        });

        $('#buscar').click(function() {
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
                // e.preventDefault();
                let formulario = form.serializeArray();
                formulario.push({ name: 'exportar'})
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
                        if (response.sit == 'OK'){
                            
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
            // })
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
    // }); 

});

function altEscala(e, id) {
    $('#loading').removeClass('disabled');
    e.preventDefault();
    let formulario = $('#alteraEscala').serializeArray();
    console.log(formulario);

    // Envie a solicitação AJAX para a View do Django
    $.ajax({
        url:  '/alteraEscala/' + id + '/', // Substitua pelo URL correto da sua View
        type: 'POST', // Ou 'GET', dependendo da configuração da sua View
        headers: { 'X-CSRFToken': crf_token },
        data: formulario,
        success: function (response) {
            // Verifique o JSON de resposta e atualize a página conforme necessário
            $('#retornoMsg').text(response.mensage); // Define a mensagem na tag HTML
            $('#mensage').addClass(response.tipo); // Define o tipo na classe
            $('#mensage').addClass('show'); // Define o tipo na classe
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
    // });

};