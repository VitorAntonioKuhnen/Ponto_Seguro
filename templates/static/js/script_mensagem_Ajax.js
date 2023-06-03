var crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

$(document).ready(function (e) {
    $('#cadastroEscala').submit(function (e) {
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
                // $('#mensage').show();
                // }
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





    })

});

function altEscala(e, id) {
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
            // if (response.mensage) {
            $('#retornoMsg').text(response.mensage); // Define a mensagem na tag HTML
            // }
            // if (response.tipo) {
            $('#mensage').addClass(response.tipo); // Define o tipo na classe
            $('#mensage').addClass('show'); // Define o tipo na classe
            // $('#mensage').show();
            // }
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