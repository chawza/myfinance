from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django import http
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def auth_login(req: HttpRequest):
    if req.method == 'GET':
        return render(req, 'auth/login.html')

    elif req.method == 'POST':
        username = req.POST.get('username', None)
        password = req.POST.get('password', None)

        if all([username, password]):
            user = authenticate(req, username=username, password=password)
            if user:
                login(req, user)
                return redirect(reverse('home')) 
        return http.HttpResponseBadRequest('Invalid username or password')

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
