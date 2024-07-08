from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

Product_name = []
Product_url = []
Prices = []
Image = []
Brand = []

for i in range(1, 11):
    url = "https://priceoye.pk/mobiles/samsung?page="+str(i)
    driver = webdriver.Chrome() 
    driver.get(url)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    items = soup.find_all("div", class_="productBox b-productBox")

    for item in items:
        brand_tag = item.get('data-brand')
        Brand.append(brand_tag)

        anchor_tag = item.find('a')
        href = anchor_tag.get('href') if anchor_tag else None
        Product_url.append(href)

        img_tag = item.find('img' , class_="img-responsive imgcent")
        discontinued_img = item.find('amp-img' , class_="product-thumbnail i-amphtml-layout-flex-item i-amphtml-layout-size-defined i-amphtml-element i-amphtml-built i-amphtml-layout")
        if img_tag or discontinued_img :                             
            img_src = img_tag['src'] 
            Image.append(img_src)

        title_element= item.find('div', class_='p-title bold h5')   
        if title_element:
            title = title_element.text.strip()
            Product_name.append(title)

        price = item.find('div', class_='price-box p1')
        target_text = price.text.strip() 
        Prices.append(target_text)

    driver.quit()
# assert len(Product_name) == len(Product_url) == len(Prices) == len(Image) == len(Brand)

# Create a DataFrame
data = {
    'PRODUCT_Title': Product_name,
    'PRODUCT_URL': Product_url,
    'CATEGORY': 'Mobile',
    'Price': Prices,
    'Image': Image,
    'BRAND_NAME': Brand,
    'Store_Name': 'Priceoye'

}
# print("Length of Product_name:", len(Product_name))
# print("Length of Product_url:", len(Product_url))
# print("Length of Prices:", len(Prices))
# print("Length of Image:", len(Image))
# print("Length of Brand:", len(Brand))
df = pd.DataFrame(data)

df.to_excel('Samsung_data.xlsx', index=False)