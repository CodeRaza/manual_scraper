import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from dbapp.models import Brand, Category

base_url = 'https://www.manualslib.com'

def get_brand_elements_with_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        target_elements = soup.find_all('div', class_='row tabled')

        if target_elements:
            for target_element in target_elements:
                a_elements = target_element.find_all('a')
                brand_name = None
                for index, a in enumerate(a_elements):
                    link_text = a.text
                    link_href = a['href']
                    if index == 0:
                        brand, brand_created = Brand.objects.get_or_create(name=link_text, link=base_url+link_href)
                        if brand_created:
                            brand.save()
                            print(f"Created Brand: {brand}")
                            brand_name = brand
                        else:
                            print(f"Brand already exists: {brand}")
                    elif brand_name:
                        category, category_created = Category.objects.get_or_create(brand=brand_name, name=link_text, link=base_url+link_href)
                        if category_created:
                            category.save()
                        else:
                            print("Category Already Exists")
        else:
            print("No elements with class 'row tabled' found on the page.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
def run():
    url = 'https://www.manualslib.com/brand/'
    get_brand_elements_with_links(url)

run()