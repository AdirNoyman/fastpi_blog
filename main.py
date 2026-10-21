from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Create a list of 5 blog posts with fields: id, author, title, content, date_posted
posts: list[dict] = [
    {
        "id": 1,
        "author": "Adirosss Gadolos",
        "title": "FastAPI Course",
        "content": "This is a simple FastAPI course.",
        "date_posted": "2023-01-01"
    },
    {
        "id": 2,
        "author": "Wako Lako",
        "title": "FastAPI Course Part 2",
        "content": "This is a simple FastAPI course part 2.",
        "date_posted": "2023-01-02"
    },
    {
        "id": 3,
        "author": "Mike Lako",
        "title": "FastAPI Course Part 3",
        "content": "This is a simple FastAPI course part 3.",
        "date_posted": "2023-01-03"
    },
    {
        "id": 4,
        "author": "Jake Bond",
        "title": "FastAPI Course Part 4",
        "content": "This is a simple FastAPI course part 4.",
        "date_posted": "2023-01-04"
    },
    {
        "id": 5,
        "author": "Samuel Bong",
        "title": "FastAPI Course Part 5",
        "content": "This is a simple FastAPI course part 5.",
        "date_posted": "2023-01-05"
    }
]

# HTML templates routes ####################################
@app.get("/", include_in_schema=False, name='home')
@app.get("/posts", include_in_schema=False, name='posts')
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", {"posts": posts, "title": "Home"})

@app.get("/posts/{post_id}", include_in_schema=False, name='post_page')
def post_page(request: Request, post_id: int):
    for post in posts:
        if post["id"]== post_id:
            post_title = post["title"][:50]
            return templates.TemplateResponse(request, "post.html", {"post": post, "title": post_title})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found") 


# API routes ###############################################
@app.get("/api/v1/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"posts": posts}

@app.get("/api/v1/posts/{post_id}", status_code=status.HTTP_200_OK)
def get_post(post_id: int):
    for post in posts:
        if post["id"]== post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# Errors handlers ############################################################
## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )