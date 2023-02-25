from django.http import HttpRequest, HttpResponse
from django import http
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def auth_login(req: HttpRequest):
    if req.method == 'POST':
        username = req.GET.get('username', None)
        password = req.GET.get('password', None)
        user = authenticate(req, username=username, password=password)

        if user is None:
            return http.HttpResponseBadRequest('Invalid username or password')
        login(req, user)

        return HttpResponse(content='Logged in!')

    return http.HttpResponseForbidden(f'Invalid method: {req.method}')

@csrf_exempt
def auth_logout(req: HttpRequest):
    if req.method == 'POST':
        logout(req)
        return HttpResponse('Logged out!')
        # Client csrftoken cookie still persist even after logout
        # case:
        #  - using insomdia
        #  - post /auth/logout
        #  - then access csrf protected endpoint 

    return http.HttpResponseForbidden(f'Invalid method: {req.method}')
