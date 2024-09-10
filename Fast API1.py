# importing modules
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# creating an instance of the FastAPI application
app = FastAPI()

# instead of using a database, i used in-memory data storage
users_db = {}
logged_in_users = set()

# using pydantic models to structure data
class User(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# registers a new user
@app.post("/register/")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists.")
    users_db[user.username] = user.password
    return {"message": "User registered successfully!"}

# the user login
@app.post("/login/")
def login(user: UserLogin):
    if user.username not in users_db or users_db[user.username] != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password.")
    logged_in_users.add(user.username)
    return {"message": f"Welcome {user.username}!"}

# a route that would require the user to be logged in to access its profile
@app.get("/profile/")
def profile(username: str):
    if username not in logged_in_users:
        raise HTTPException(status_code=403, detail="You must be logged in to access this.")
    return {"message": f"Hello, {username}! This is your profile."}

# the logout
@app.post("/logout/")
def logout(username: str):
    if username not in logged_in_users:
        raise HTTPException(status_code=400, detail="User is not logged in.")
    logged_in_users.remove(username)
    return {"message": f"{username} logged out successfully!"}