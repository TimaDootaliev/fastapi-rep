from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blogs'])
def post_list(db: Session = Depends(get_db)):
    """ Просмотр всех записей """
    blogs = db.query(models.Blog).all()
    return blogs


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_post(request: schemas.Blog, db: Session = Depends(get_db)):
    """ Создание поста """
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
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


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_post(id, request: schemas.Blog, db: Session = Depends(get_db)):
    """ Изменение поста """
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    blog.update(request.dict())
    db.commit()
    return f'Post with id {id} updated'


@router.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog, tags=['blogs'])
def post_detail(id, response: Response, db: Session = Depends(get_db)):
    """ Функция для просмотра деталей поста """
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Post with the id {id} doesn\'t exist'
            )
    return blog