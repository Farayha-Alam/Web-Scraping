from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

base_url="https://books.toscrape.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
data_lst=[]
product_link_lst=[]
for page_num in range(1,5):
    print(f'collection of url from page num {page_num} started')
    k = requests.get(f'https://books.toscrape.com/catalogue/category/books/fiction_10/page-{page_num}.html').text
    soup=BeautifulSoup(k,'html.parser')
    fictions=soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
    for index,fiction in enumerate(fictions):
        url=fiction.find("article", class_="product_pod").find("h3").find("a").get("href")
        url_elements=url.split("/")
        concatenated_url="/" + url_elements[3] + "/" + url_elements[-1]
        product_link=base_url+ "/catalogue" + concatenated_url
        product_link_lst.append(product_link)
    print(f'collection of url from page number {page_num} completed')

for index, product_link in enumerate(product_link_lst):    
    print(f"collection of data from product number {index+1} started")
    k = requests.get(product_link, headers=headers).text
    soup=BeautifulSoup(k,'html.parser')
    product=soup.find("div",class_="col-sm-6 product_main")
    type="Fiction"
    book_name=product.find("h1").text
    price=product.find("p").text
    instock_availability=product.find("p",class_="instock availability").text.strip()
    review=product.find_all("p")[-1]['class'][-1]
    description=soup.find("p", class_=None).text
    data={"type": type, "book name": book_name, "price": "£" + str(price[2:]), "instock availability": instock_availability, "review score" : review, "description": description}
    data_lst.append(data)
    print(f"collection of data from product number {index+1} completed")

print("storing the collected data in dataframe - started")
df=pd.DataFrame(data_lst)
df.to_csv(os.getcwd()+"/file.csv")
print("storing the collected data in dataframe - completed")
print("all processes successfully completed")

   