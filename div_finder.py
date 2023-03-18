from selenium import webdriver
from bs4 import  BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# this function can print all the menu of A RESTAURANT by getting all the divs 
def perres(url):
    # Set up the Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.get(url) 

    # Get the HTML source code of the page using Selenium
    html = driver.page_source

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the divs on the page with class 'my-class'
    divs = soup.find_all('div')

    dids=[]
    # Loop through each div and print its text content
    for div in divs:
        div_id = div.get('id')
        if div_id:
            dids.append(div) 
            #print(div_id)
            

# Close the Selenium webdriver
    driver.quit()
    return dids