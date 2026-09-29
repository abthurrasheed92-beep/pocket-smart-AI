import json
import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..dependencies import current_user

from ..models import (
    User,
    RecommendationHistory
)

from ..schemas import (
    HomeRequest,
    PartyRequest
)

from ..services.gemini import generate


router = APIRouter()


UPLOAD_FOLDER = Path(
    "uploads"
)

UPLOAD_FOLDER.mkdir(
    exist_ok=True
)


def save_history(
    db,
    user,
    planner,
    payload,
    result
):

    row = RecommendationHistory(

        user_id=user.id,

        planner=planner,

        input_json=json.dumps(
            payload
        ),

        result_json=json.dumps(
            result
        )
    )

    db.add(row)

    db.commit()

    db.refresh(row)

    result["history_id"] = row.id

    return result


@router.post(
    "/generate-home"
)
async def generate_home(

    p: HomeRequest,

    user: User = Depends(
        current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    data = p.model_dump()

    result = await generate(
        "home",
        data
    )

    return save_history(
        db,
        user,
        "home",
        data,
        result
    )


@router.post(
    "/generate-party"
)
async def generate_party(

    p: PartyRequest,

    user: User = Depends(
        current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    data = p.model_dump()

    result = await generate(
        "party",
        data
    )

    return save_history(
        db,
        user,
        "party",
        data,
        result
    )


@router.post(
    "/generate-jewelry"
)
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form(
        "Elegant"
    ),

    outfit_color: str = Form(
        "Not specified"
    ),

    notes: str = Form(""),

    outfit_image:
        UploadFile | None = File(None),

    user: User = Depends(
        current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero"
        )

    image_path = None

    if (
        outfit_image
        and outfit_image.filename
    ):

        allowed = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if (
            outfit_image.content_type
            not in allowed
        ):

            raise HTTPException(
                status_code=415,
                detail="Only JPG, PNG and WEBP are allowed"
            )

        image_data = (
            await outfit_image.read()
        )

        if len(image_data) > (
            5 * 1024 * 1024
        ):

            raise HTTPException(
                status_code=413,
                detail="Image must be 5 MB or smaller"
            )

        filename = (
            uuid.uuid4().hex
            + Path(
                outfit_image.filename
            ).suffix.lower()
        )

        image_path = str(
            UPLOAD_FOLDER / filename
        )

        Path(
            image_path
        ).write_bytes(
            image_data
        )

    data = {

        "budget":
            budget,

        "occasion":
            occasion,

        "style":
            style,

        "outfit_color":
            outfit_color,

        "notes":
            notes,

        "has_outfit_image":
            bool(image_path)
    }

    result = await generate(
        "jewelry",
        data,
        image_path
    )

    return save_history(
        db,
        user,
        "jewelry",
        data,
        result
    )