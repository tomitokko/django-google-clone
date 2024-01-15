from django.shortcuts import render, redirect
import requests
from django.core.paginator import Paginator

# Create your views here.
def search_results(query):
    url = "https://google-search74.p.rapidapi.com/"

    querystring = {"query":query,"limit":"50","related_keywords":"true"}

    headers = {
        "X-RapidAPI-Key": "082e1babc4msh087e1333d34ef31p1c8f2cjsn7bfaaa543524",
        "X-RapidAPI-Host": "google-search74.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    extracted_data = []

    for result in data['results']:
        extracted_info = {
            'url': result['url'],
            'title': result['title'],
            'description': result['description'],
        }
        extracted_data.append(extracted_info)

    return extracted_data

def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method == 'POST':
        search_query = request.POST['search']
        request.session['search_query'] = search_query
    elif request.method =='GET' and 'page' in request.GET:
        search_query = request.session.get('search_query')
    else:
        return redirect('/')
    
    results = search_results(search_query)

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'search.html', context)