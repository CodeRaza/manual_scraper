import requests
from bs4 import BeautifulSoup
from dbapp.models import Brand, Category, ProductModel, ProductModelDocumentTypeDocs, ProductType, Article
from dbapp.scripts.table_content import get_table_content
from dbapp.scripts.downloadPDF import get_pdf_text
import concurrent.futures

base_url = 'https://www.manualslib.com'

def get_manuals_models(url, brand):
    response = requests.get(url)
    print(brand.link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        target_models_headings = soup.find_all('div', class_='cathead')
        
        category_div = soup.find_all('div', class_='category')
        if category_div:
            for category in category_div:
                for i in target_models_headings:
                    category_name = i.text
                    if category_name:
                        product_type, created = ProductType.objects.get_or_create(brand=brand, name=category_name)

                        if created:
                            product_type.save()
                            print(f"Created ProductType: {product_type}")
                        else:
                            print(f"ProductType already exists: {product_type}")

                        row_elements = category.find_all('div', class_='row tabled')

                        for row_element in row_elements:
                            model_name_element = row_element.find('div', class_='col-xs-3 col-sm-2')
                            model_name = model_name_element.text.strip() if model_name_element else None

                            document_type = row_element.find_all('div', class_='col-xs-9 col-sm-10 manuals-col')

                            product_model, model_created = ProductModel.objects.get_or_create(product=product_type, model=model_name)

                            if model_created:
                                product_model.save()
                                print(f"Created ProductModel: {product_model}")
                            else:
                                print(f"ProductModel already exists: {product_model}")

                            print(model_name)
                            for doc in document_type:
                                document_type_links = doc.find_all('a')
                                for d in document_type_links:
                                    print(d.text)
                                    print(base_url+d['href'])
                                    name = d.text
                                    link = base_url+d['href']

                                    doc_type_model, doc_model_created = ProductModelDocumentTypeDocs.objects.get_or_create(model=product_model, name=name, doc_link=link)
                                    
                                    if doc_type_model:
                                            articles_count = Article.objects.filter(doc=doc_type_model).count()
                                            if articles_count > 0:
                                                table_content = get_table_content(url_=link)
                                                the_pdf = get_pdf_text(url_=link, title=table_content['title'])
                                                if the_pdf is not None and table_content is not None:
                                                    article, article_created = Article.objects.get_or_create(
                                                        doc=doc_type_model, 
                                                        title=table_content['title'], 
                                                        table_content=table_content['content_table'],
                                                        text=the_pdf['text'],
                                                        pdf_file=the_pdf['pdf']
                                                    )
                                                    
                                                    if article_created:
                                                        article.save()
                                                        print(f"Created Article: {article}")
                                                    else:
                                                        print(f"Article already exists: {article}")
                                            else:
                                                print("ARTICAL Exists")

                                    if doc_model_created:
                                        doc_type_model.save()
                                        
                                        table_content = get_table_content(url_=link)
                                        the_pdf = get_pdf_text(url_=link, title=table_content['title'])
                                        
                                        if the_pdf is not None and table_content is not None:
                                            article, article_created = Article.objects.get_or_create(
                                                doc=doc_type_model, 
                                                title=table_content['title'], 
                                                table_content=table_content['content_table'],
                                                text=the_pdf['text'],
                                                pdf_file=the_pdf['pdf']
                                            )
                                            
                                            if article_created:
                                                article.save()
                                                print(f"Created Article: {article}")
                                            else:
                                                print(f"Article already exists: {article}")
                                    else:
                                        print(f"DocumentType already exists: {doc_type_model}")

                            print('----------')

                        print('_____________')
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

def scrape_brand(brand):
    url = brand.link
    get_manuals_models(url, brand)

def run():
    brands = Brand.objects.all()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(scrape_brand, brands)
    
run()

