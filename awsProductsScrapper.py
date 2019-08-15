import sys
import datetime
from requests import get
from bs4 import BeautifulSoup
from subprocess import Popen

class AwsProductsScraper:       

    # Holds the products in a dictionary format  where :
    # key   = Product Name
    # value = {
    #           "Categories":     "",    
    #           "Description":  "",
    #           "Link":         ""
    #         }
    productsMap = {}

    # constructor intializes the base url and the product path 
    def __init__(self, baseUrl, productsPath):
        self.baseUrl = baseUrl
        self.productsUrl = self.baseUrl + productsPath
    
    # scrapes the aws products page for aws services and stores them in the productsMap dictionary object 
    def ReadProducts(self):
        htmlresponse = get(self.productsUrl).content
        soup = BeautifulSoup(htmlresponse,"lxml")        
        for categoryNode in soup.find_all(class_="lb-item-wrapper"):            
            category =  (categoryNode.find("a").find("span").text)
            for productNode in categoryNode.find_all(class_="lb-content-item"):                
                for product in productNode.find_all("a"):                    
                    prodname = product.contents[0].strip()                    
                    if prodname in self.productsMap:
                        # add to existing categories if the product is already found
                        self.productsMap[prodname]["Categories"] += "," + category
                    else: 
                        self.productsMap[prodname] = {
                            "Categories":     category,                            
                            "Description":  product.span.text.strip(),
                            "Link":         self.baseUrl + product["href"].strip()
                        }

    #  reads the products from the productsMap dictionary object and writes to the given file in html format
    def WriteProducts(self,filename):
        file = open(filename,"w")
        file.write("<html><head>")
        # Include bootstrap
        file.write("<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\" integrity=\"sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T\" crossorigin=\"anonymous\">")
        file.write("</head><body>")        
        file.write("<table class=\"table table-dark table-striped table-hover\">")
        
        # Add header row
        file.write("<tr class=\"bg-warning\">")
       
        file.write("<th>")    
        file.write(str(len(self.productsMap)) + f" Services <i>as of {datetime.datetime.now():%Y-%m-%d}</i>")
        file.write("</th>")
    
        file.write("<th>")
        file.write("")
        file.write("</th>")
            
        file.write("</tr>")
            
        # add table rows
        for productName,productInfo in sorted(self.productsMap.items()):                    
    
            file.write("<td>")
            file.write("<a class=\"text-white\" href=\"" + productInfo["Link"] + "\">")
            file.write(productName)
            file.write("</a>")
            file.write("</td>")
    
            file.write("<td>")
            file.write(productInfo["Description"] + " (" + productInfo["Categories"] + ")" )
            file.write("</td>")
            file.write("</tr>")
            
            
        file.write("</table>")
        file.write("<script src=\"https://code.jquery.com/jquery-3.3.1.slim.min.js\" integrity=\"sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo\" crossorigin=\"anonymous\"></script>")
        file.write("<script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js\" integrity=\"sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1\" crossorigin=\"anonymous\"></script>")
        file.write("<script src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js\" integrity=\"sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM\" crossorigin=\"anonymous\"></script>")
        file.write("</body></html>")
        file.close()
         
# entry point
def main():   
    try: 
        awsFileName = "awsServices.html"
        scrapper = AwsProductsScraper(
            baseUrl = "https://aws.amazon.com",
            productsPath = "/products"
        )      
        scrapper.ReadProducts()    
        scrapper.WriteProducts(awsFileName)    
        Popen(awsFileName, shell=True)
    except:
        print("Unexpected error:", sys.exc_info())
    
if __name__ == "__main__":
    main()