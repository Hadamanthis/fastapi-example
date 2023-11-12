from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter()

#@router.get("/posts", response_model=List[schemas.PostVoteResponse])
@router.get("/posts", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).offset(skip).all()

    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostVoteResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #                (post.title, post.content, post.published))
    
    # saved_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/posts/latest", response_model=schemas.PostVoteResponse)
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute(f"SELECT * FROM posts e WHERE e.created_at = (SELECT max(created_at) FROM posts)")
    # post = cursor.fetchone()

    latest = db.query(func.max(models.Post.created_at)).scalar()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).filter(models.Post.created_at == latest).group_by(models.Post.id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"There is no posts!")

    return post

@router.get("/posts/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    #post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).filter(models.Post.id == id).group_by(models.Post.id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} not found")
    
    return post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    db.delete(post)
    db.commit()

@router.put("/posts/{id}", response_model=schemas.PostVoteResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    #cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", 
    #               (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"Post {id} not found")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()

    return post_query.first()
