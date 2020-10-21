from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
from django.utils import timezone


BASE_CRAIGSLIST_URL = 'https://indore.craigslist.org/search/sss?query={}'
BASE_IMG_URL = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search, created=timezone.now())
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class':'result-row'})
    final_posting = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price').text
        if post.find(class_='result-image').get('data-ids'):
            a = post.find(class_='result-image').get('data-ids').split(':', 1)
            post_image = BASE_IMG_URL.format(quote_plus(a[1]))
        else:
            post_image = 'https://craigslist.org/images/peace.jpg'
        final_posting.append((post_title, post_url, post_price, post_image))


    frontend = {
        'search': search,
        'final_posting': final_posting,
    }
    return render(request, 'my_app/new_search.html', frontend)
