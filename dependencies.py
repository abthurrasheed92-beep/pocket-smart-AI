from fastapi import (
    Depends,
    HTTPException,
    Request
)

from sqlalchemy.orm import Session

from .auth import get_user_id

from .database import get_db

from .models import User


def current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:

    token = request.headers.get(
        "Authorization",
        ""
    )

    if token.lower().startswith(
        "bearer "
    ):

        token = token[7:]

    else:

        token = request.cookies.get(
            "access_token",
            ""
        )

    user_id = get_user_id(token)

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    user = db.get(
        User,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user