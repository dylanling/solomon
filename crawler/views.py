from django.shortcuts import render
from django.http import HttpResponse

from .forms import AuthorForm

def index(request):
    return HttpResponse("empty page")

def crawl_author(request):
    if request.method == 'POST':
        return HttpResponse("thx :)")  
    else:
        form = AuthorForm()
        return render(request, 'crawl_author.html', {'form': form})