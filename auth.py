from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import User

from ..schemas import (
    RegisterRequest,
    LoginRequest
)

from ..auth import (
    hash_password,
    verify_password,
    create_token
)


router = APIRouter(prefix="/auth")


@router.post("/register")
def register(
    p: RegisterRequest,
    db: Session = Depends(get_db)
):

    email = p.email.lower()

    existing = (
        db.query(User)
        .filter_by(email=email)
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        name=p.name.strip(),
        email=email,
        password_hash=hash_password(
            p.password
        )
    )

    db.add(user)

    db.commit()

    return {
        "ok": True,
        "message": "Registration successful"
    }


@router.post("/login")
def login(
    p: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter_by(
            email=p.email.lower()
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            p.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token(
        user.id
    )

    response.set_cookie(
        "access_token",
        "Bearer " + token,
        httponly=True,
        samesite="lax"
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    response: Response
):

    response.delete_cookie(
        "access_token"
    )

    return {
        "ok": True
    }