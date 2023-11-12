from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(
    prefix='/vote',
    tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteResponse)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {vote.post_id} not found")

    found_vote = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id).first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {found_vote.user_id} has already voted on post {found_vote.post_id}")
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)

        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)

        return new_vote
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote from user {vote.user_id} on post {vote.post_id} does not exists")
        
        db.delete(found_vote)
        db.commit()