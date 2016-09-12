from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    context = {}
    context['andrewid'] = ''
    context['firstname'] = ''
    context['lastname'] = ''

    # Retrieve attributes from request
    if 'andrewid' in request.GET:
        context['andrewid'] = request.GET['andrewid']
    if 'firstname' in request.GET:
        context['firstname'] = request.GET['firstname']
    if 'lastname' in request.GET:
        context['lastname'] = request.GET['lastname']

    return render(request, 'register.html', context)
