import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import current_user
from ..models import User, RecommendationHistory


router = APIRouter(prefix="/api")


@router.get("/history")
def history(
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):
    rows = (
        db.query(RecommendationHistory)
        .filter_by(user_id=user.id)
        .order_by(RecommendationHistory.created_at.desc())
        .limit(50)
        .all()
    )

    return [
        {
            "id": row.id,
            "planner": row.planner,
            "created_at": row.created_at.isoformat(),
            "input": json.loads(row.input_json),
            "result": json.loads(row.result_json)
        }
        for row in rows
    ]


@router.get("/recommendations-details/{rid}")
def recommendation_details(
    rid: int,
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):
    row = (
        db.query(RecommendationHistory)
        .filter_by(
            id=rid,
            user_id=user.id
        )
        .first()
    )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    return {
        "id": row.id,
        "planner": row.planner,
        "input": json.loads(row.input_json),
        "result": json.loads(row.result_json)
    }