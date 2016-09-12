from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def add(request):
    context = {}
    context['result'] = 0

    # Retrieve attributes from request
    if 'username' in request.GET:
        context['result'] = request.GET['username']


    return render(request, 'add.html', context)

