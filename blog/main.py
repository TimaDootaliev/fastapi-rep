from fastapi import (FastAPI, Depends, status, Response, HTTPException)
from . import schemas, models
from .database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
async def create_post(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def post_list(db: Session = Depends(get_db)):
    """ Функция для просмотра всех записей """
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200)
def post_detail(
                id, 
                response: Response, 
                db: Session = Depends(get_db)
                ):
    """ Функция для просмотра деталей поста """
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Post with the id {id} doesn\'t exist'
            )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Post with the id {id} doesn\'t exist'}
    return blog
