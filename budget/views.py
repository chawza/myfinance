from django.shortcuts import render
from django.http.request import HttpRequest
from budget.models import BudgetItem

# Create your views here.

def index(request: HttpRequest):
    wishlist = BudgetItem.objects.filter(user=request.user, repeat=BudgetItem.Repetion.ONCE)
    context = {
        "wishlist": wishlist,
    }
    return render(request, 'budget/index.html', context)