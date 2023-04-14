from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Define a Pydantic model for the Restaurant
class Restaurant(BaseModel):
    city_name: str
    rest_name: str
    rest_url: str
    cuisine: str
    ratings: str
    cost_for_two: str
    discount: int = None
    coupon: str = None

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="swiggdb",
    user="postgres",
    password="root"
)

# Endpoint for retrieving all cities
@app.get("/cities")
async def get_cities():
    cur=conn.cursor()
    query= "SELECT * FROM citydat"
    cur.execute(query)
    rows = cur.fetchall()
    cities = []
    for row in rows:
        restaurant = {
            "city_id": row[0],
            "city_name": row[1],
            "city-url": row[2],
        }
        cities.append(restaurant)
    return {"restaurants": cities}

# Endpoint for retrieving all restaurants
@app.get("/restaurants")
async def get_restaurants():
    cur = conn.cursor()
    query = "SELECT * FROM restaurant_dat"
    cur.execute(query)
    rows = cur.fetchall()
    restaurants = []
    for row in rows:
        restaurant = {
            "rest_id": row[0],
            "city_name": row[1],
            "rest_name": row[2],
            "rest_url": row[3],
            "cuisine": row[4],
            "ratings": row[5],
            "cost_for_two": row[6],
            "discount": row[7],
            "coupon": row[8]
        }
        restaurants.append(restaurant)
    return {"restaurants": restaurants}

