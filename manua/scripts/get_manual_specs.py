import requests
from bs4 import BeautifulSoup
from manua.models import Manual, Product  # Import the Manual model from your app
import json
def remove_fragment_from_url(url):
    if url.endswith('/manual'):
        url = url.replace('/manual', '/specifications')
    return url

def scrape_manual_details(base_url, product, manual_name):
    try:
        cleaned_url = remove_fragment_from_url(base_url)
        response = requests.get(cleaned_url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find(class_='specs__title')
            
            if title:
                
                elements = soup.find_all(class_='d-flex flex-grow-1 flex-column specs')

                all_p_texts = []
                final_txt = ''

                for elem in elements:
                    p_elements = elem.find_all('p')
                    for p_elem in p_elements:
                        all_p_texts.append(p_elem.get_text(strip=True))

                for text in all_p_texts:
                    final_txt += text + "\n"
                
                card_sections = soup.find_all('div', class_='card')

                data = {}

                for index, card in enumerate(card_sections, start=1):
                    section_name = card.find('h5').text.strip()
                    section_data = {}
                    
                    table_rows = card.find_all('tr')
                    for row in table_rows:
                        key = row.find('td', class_='text-muted').text.strip()
                        value = row.find('td').text.strip()
                        section_data[key] = value
                    
                    data[f"{section_name}"] = section_data

                specs_data = json.dumps(data)
                
                manual = Manual.objects.create(
                    product=product,
                    title=manual_name, 
                    specs=specs_data, 
                    text=final_txt, 
                )
                
                manual.save()
                
                print(f'Manual & SPECs For {manual_name} are SAVED!')

    except Exception as e:
        print(f"Error scraping PDF: {e}")

def scrape_and_download_manuals():
    try:
        products = Product.objects.all()

        for product in products:
            try:
                response = requests.get(product.link)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    manual_links = soup.select('.d-flex.w-100.text-dark.text-decoration-none')
                    
                    for link_element in manual_links:
                        manual_link = link_element['href']
                        product_name_element = link_element.find('h5')
                        product_name = product_name_element.get_text().strip()
                        
                        if Manual.objects.filter(title=product_name).count() < 1:
                            scrape_manual_details('https://www.manua.ls'+manual_link, product, product_name)
                        else:
                            print(f"Manual '{product_name}' for product '{product}' already exists. Skipping.")
                else:
                    print(f"Failed to fetch URL: {product.link}")

            except Exception as e:
                print(f"Error downloading manuals for {product.title}: {e}")

    except Exception as e:
        print(f"Error initializing requests: {e}")

def run():
    scrape_and_download_manuals()

run()