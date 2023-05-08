from django.urls import reverse
from django.http import HttpResponse

class BloqueiaAcessoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o usuário está na tela específica
        if request.path == reverse('justificativas'):
            # Caso contrário, redireciona para outra página ou exibe uma mensagem de erro
            response = HttpResponse("Você não tem permissão para acessar esta página.")
            response.status_code = 403
        else:
            response = self.get_response(request) 
        return response