from fastapi import FastAPI
from routes import UsersRoute, MoviesRoute, RentsRoute

app = FastAPI(title='API-RENTAL-CD', description='Admin | Customer')

app.include_router(UsersRoute.users_router)
app.include_router(MoviesRoute.movies_router)
app.include_router(RentsRoute.rents_router)


@app.get("/")
def read_root():
    return {"WELCOME TO MANAGEMENT API RENTAL MOVIE"}
