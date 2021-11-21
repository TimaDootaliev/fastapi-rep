from typing import Optional
from fastapi import FastAPI
import uvicorn
from blog.models import Blog


app = FastAPI()


@app.get('/blog')
def index(limit = 10, published: bool = True, sort: Optional[str] = None):
    # only get 10 published posts
    if published:
        return {'data': f'{limit} published posts from database'}
    return {'data': f'{limit} posts from database'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    return {'data': {'1', '2'}}



@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f'Blog is created {blog.title}'}


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8080)