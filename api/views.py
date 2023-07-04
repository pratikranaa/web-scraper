from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import random
import requests


# Create your views here.
@csrf_exempt
def get_proxy():
    # Fetch a list of proxies from a proxy provider or your preferred source
    proxy_list = [
        'proxy1.example.com:8080',
        'proxy2.example.com:8080',
        'proxy3.example.com:8080'
    ]
    return random.choice(proxy_list)

@csrf_exempt
def scrape(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        search_term = request.POST.get('search_term')

        # Configure ChromeDriver options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Instantiate ChromeDriver with dynamic proxy
        proxy = get_proxy()
        options = {
            'proxy': {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
                'no_proxy': 'localhost,127.0.0.1'  # Exclude proxy for local addresses
            }
        }
        driver = webdriver.Chrome(executable_path=settings.CHROMEDRIVER_PATH, options=chrome_options, seleniumwire_options=options)

        # Perform web scraping
        driver.get(url)
        html = driver.page_source
        driver.quit()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find the elements matching the specified search term
        elements = soup.find_all(text=search_term)

        # Return the scraped data as JSON response
        response_data = {
            'url': url,
            'search_term': search_term,
            'scraped_data': [element.strip() for element in elements]
        }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'})
