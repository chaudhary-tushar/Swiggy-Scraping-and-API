
# Swiggy Scraping and API

Description:

 Web scraping with Selenium to extract data from Swiggy.
- Storage of scraped data in MySQL, MongoDB, and PostgreSQL databases.
- Integration of MySQL with Django framework to create a RESTful API with the cities endpoint.
- Integration of MongoDB with Flask framework to create a RESTful API with the restaurants endpoint.
- Integration of PostgreSQL with FastAPI framework to create a RESTful API with the menu data endpoint.



## Screenshots

![App Screenshot](https://github.com/chaudhary-tushar/Swiggy-Scraping-and-API/blob/master/flowchart.jpg)


## Key Features:

1. Uses Selenium with Multiprocessing to gather data of 90,000 restaurants in 603 Cities across India in 70 minutes.
2. Main.py is the driver code which functions on swiggyscrape.py objects which are documented within the file in pep-8 standards.
3. To build the API's I have used Django with MySQL , Flask with MongoDb and Fast-API with PostgreSQL.
4. Build a standalone and integrated functionality to clean and fill data in the respective dbs.
5. The multiprocessing uses two modules for optimal output :
    - Pooling   (from multiprocessing import Pool)
    - Threading (from concurrent.futures import ThreadPoolExecutor)

## Endpoints

The project provides the following API endpoints to access the stored data:

- **Cities Endpoint**: Retrieves information about all the 603 cities including `id` , `Cityname`, `Citylink`
- **Restaurants Endpoint**: Retrieves restaurant data of a specific city including data about `rest_Id (primary key)`, `city_name`, `restaurant_name`, `restaurat_Url (Unique index)`, `cuisine`, `Ratings`, `Cost for two`, `Discount`, `Coupon`
- **Topres/<city-name>**: Retrives top 10 restaurant information in the city based on ratings.
- **Menu Data Endpoint**: Retrieves menu information of a specific restaurant including data about  `Item Id`, `City`, `Restaurant name`, `Restaurant url`, `Item name`, `Item type`, `Item section`, `Cost of item`, `Description`, `Customization`, `Bestseller`

## Installation

1. Clone the repository
2. Install the dependencies in Python virtual environment.
    - `python -m venv venv`
    - `.\Scripts\activate` 
    - `pip install -r requirements.txt`
3. Configure the database connections in the respective framework settings.
4. Run the application and access the API endpoints.

## 🛠 Skills
Python, Selenium, Django, Flask, Fast-API, MySQL, MongoDb, PostgreSQL, Rest_framework, Multiprocessing, MultiThreading, Pandas, Automation, Scraping, Data processing, Regex. 


## Feedback

If you have any feedback, please reach out to me at chaudharytushar014@.gmailcom

