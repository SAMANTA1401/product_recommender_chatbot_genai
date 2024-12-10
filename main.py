from ecommercebot.data_converter import DataConverter




data_dir = 'artifacts/flipkart_product_review.csv'
columns = ['product_title', 'review']
meta_data = 'product_name'
page_content = 'review'
doc_converter = DataConverter(data_dir=data_dir, meta_data=meta_data, page_content=page_content, columns=columns)
documents = doc_converter.dataconverter()
print(documents[:5])