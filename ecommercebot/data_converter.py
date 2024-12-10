import pandas as pd
from langchain_core.documents import Document

class DataConverter():
    def __init__(self, data_dir, meta_data, page_content, columns):
        self.data_dir = data_dir
        self.meta_data = meta_data
        self.page_content = page_content
        self.columns = columns


    def dataconverter(self):
        product_data = pd.read_csv(self.data_dir)
        data =  product_data[self.columns]

        product_list = []
        # dataframe to document
        for index , row in data.iterrows():
            # create a dictionary for each row
            object = {
            self.meta_data : row[self.columns[0]],
            self.page_content: row[self.columns[1]]
        }

            ## Append the object to the product list
            product_list.append(object)

        docs = []
        for entry in product_list:
            metadata = {self.meta_data: entry[self.meta_data]}
            doc = Document(page_content= entry[self.page_content], metadata= metadata)
            docs.append(doc)    

        return docs


if __name__ == "__main__":

    data_dir = '../artifacts/flipkart_product_review.csv'
    columns = ['product_title', 'review']
    meta_data = 'product_name'
    page_content = 'review'
    doc_converter = DataConverter(data_dir=data_dir, meta_data=meta_data, page_content=page_content, columns=columns)
    documents = doc_converter.dataconverter()
    print(documents[:5])