from django.http import HttpRequest


def user_data(request: HttpRequest):
    return {  'username': request.user.username } 
