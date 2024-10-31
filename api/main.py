from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import psycopg2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Model for User creation
class User(BaseModel):
    firstName: str
    lastName: str
    occupation: str
    age: int
    city: str

# Model for Search Request
class SearchRequest(BaseModel):
    query: str

# Initialize the BERT model for feature extraction
search_model = pipeline("feature-extraction", model="bert-base-uncased")

# Function to connect to PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost", database="helixfa3", user="fa", password="DitfaDitfa9821"
    )
    return conn

# Endpoint to create a user
@app.post("/users/")
async def create_user(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Insert new user into the User table
        cur.execute(
            'INSERT INTO public."User" (firstname, lastname, occupation, age, city) VALUES (%s, %s, %s, %s, %s)',
            (user.firstName, user.lastName, user.occupation, user.age, user.city)
        )
        conn.commit()  # Commit the transaction
        return {"message": "User created successfully."}
    except Exception as e:
        conn.rollback()  # Rollback in case of error
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cur.close()
        conn.close()

# Function to calculate cosine similarity
def calculate_similarity(query_embedding, user_embedding):
    query_embedding = np.array(query_embedding).reshape(1, -1)
    user_embedding = np.array(user_embedding).reshape(1, -1)
    return cosine_similarity(query_embedding, user_embedding)[0][0]

# Endpoint for semantic search
@app.post("/semantic-search")
async def semantic_search(request: SearchRequest):
    # Get embedding for the search query
    query_embedding = search_model(request.query)[0][0]

    # Fetch all users from the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT firstname, lastname, occupation, age, city FROM public."User"')
    users = cur.fetchall()
    cur.close()
    conn.close()

    # List to hold search results
    search_results = []

    # Compute embedding and similarity for each user
    for user in users:
        user_text = f"{user[0]} {user[1]} {user[2]}"  # Combine first name, last name, and occupation
        user_embedding = search_model(user_text)[0][0]
        similarity = calculate_similarity(query_embedding, user_embedding)

        search_results.append(
            {
                "firstName": user[0],
                "lastName": user[1],
                "occupation": user[2],
                "age": user[3],
                "city": user[4],
                "similarity": similarity,
            }
        )

    # Sort results based on similarity
    search_results = sorted(search_results, key=lambda x: x["similarity"], reverse=True)

    return {"users": search_results}
