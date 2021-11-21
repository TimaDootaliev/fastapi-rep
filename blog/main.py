from typing import List
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
def create_post(request: schemas.Blog, db: Session = Depends(get_db)):
    """ Создание поста """
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', response_model=List[schemas.ShowBlog])
def post_list(db: Session = Depends(get_db)):
    """ Просмотр всех записей """
    blogs = db.query(models.Blog).all()
    return blogs


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_post(id, db: Session = Depends(get_db)):
    """ Удаление записей """
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with the id {id} doesn\'t exist'
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id, request: schemas.Blog, db: Session = Depends(get_db)):
    """ Изменение поста """
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    blog.update(request.dict())
    db.commit()
    return f'Post with id {id} updated'


@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog)
def post_detail(id, response: Response, db: Session = Depends(get_db)):
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



@app.post('/user')
def create_user(request: schemas.User, 
                db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# TODO: 2:23:40 password hashing