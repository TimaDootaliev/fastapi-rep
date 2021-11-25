from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog
from blog.ouath2 import get_current_user

router = APIRouter(
    tags=['posts'],
    prefix='/api/v^1/blog'
)


@router.get('/', response_model=List[schemas.ShowBlog])
def post_list(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """ Просмотр всех записей """
    return blog.post_list(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """ Создание поста """
    return blog.create(request, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy_post(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """ Удаление записей """
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """ Изменение поста """
    return blog.alter(id, request, db)


@router.get('/{id}', status_code=200, response_model=schemas.ShowBlog)
def post_detail(id, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """ Функция для просмотра деталей поста """
    return blog.details(id, db)
