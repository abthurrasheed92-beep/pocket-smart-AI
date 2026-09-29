import json
import os

from pathlib import Path

from dotenv import load_dotenv

from .recommendations import (
    fallback,
    link
)


load_dotenv()


RULES = """
You are PocketSmart AI.

Return ONLY JSON.

Required keys:

summary
allocations
recommendations

Every recommendation must contain:

category
name
estimated_price
platform
reason

Allowed platforms:

Amazon
Flipkart
IKEA
Swiggy
Zomato
OYO

Respect the user's total budget.

Prices are estimates, not live marketplace prices.

Do not claim live marketplace access.
"""


def clean_json(text):

    text = text.strip()

    if text.startswith("```"):

        text = text.split(
            "\n",
            1
        )[1]

        text = text.rsplit(
            "```",
            1
        )[0]

    start = text.find("{")

    end = text.rfind("}")

    return json.loads(
        text[start:end + 1]
    )


async def generate(
    planner,
    data,
    image_path=None
):

    demo = (
        os.getenv(
            "DEMO_MODE",
            "false"
        ).lower()
        == "true"
    )

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if demo or not api_key:

        return fallback(
            planner,
            data
        )

    try:

        from google import genai

        from google.genai import types

        client = genai.Client(
            api_key=api_key
        )

        prompt = (
            RULES
            + "\nPlanner: "
            + planner
            + "\nUser data:\n"
            + json.dumps(
                data,
                indent=2
            )
        )

        contents = [
            prompt
        ]

        if image_path:

            ext = Path(
                image_path
            ).suffix.lower()

            mime = {
                ".png": "image/png",
                ".webp": "image/webp"
            }.get(
                ext,
                "image/jpeg"
            )

            contents.append(
                types.Part.from_bytes(
                    data=Path(
                        image_path
                    ).read_bytes(),
                    mime_type=mime
                )
            )

        response = client.models.generate_content(

            model=os.getenv(
                "GEMINI_MODEL",
                "gemini-2.5-flash"
            ),

            contents=contents,

            config={
                "response_mime_type":
                    "application/json"
            }
        )

        raw = clean_json(
            response.text
        )

        budget = float(
            data["budget"]
        )

        items = []

        total = 0

        allowed = {
            "Amazon",
            "Flipkart",
            "IKEA",
            "Swiggy",
            "Zomato",
            "OYO"
        }

        for item in raw.get(
            "recommendations",
            []
        ):

            platform = item.get(
                "platform",
                "Amazon"
            )

            if platform not in allowed:

                platform = "Amazon"

            price = max(
                0,
                float(
                    item.get(
                        "estimated_price",
                        0
                    )
                )
            )

            if total + price <= budget:

                name = str(
                    item.get(
                        "name",
                        "Recommended item"
                    )
                )

                items.append({

                    "category":
                        str(
                            item.get(
                                "category",
                                "General"
                            )
                        ),

                    "name":
                        name,

                    "estimated_price":
                        price,

                    "platform":
                        platform,

                    "reason":
                        str(
                            item.get(
                                "reason",
                                "Matches your request."
                            )
                        ),

                    "search_url":
                        link(
                            platform,
                            name
                        )
                })

                total += price

        if not items:

            return fallback(
                planner,
                data
            )

        return {

            "planner":
                planner,

            "budget":
                budget,

            "budget_used":
                round(
                    total,
                    2
                ),

            "summary":
                raw.get(
                    "summary",
                    "AI-generated plan"
                ),

            "allocations":
                raw.get(
                    "allocations",
                    {}
                ),

            "recommendations":
                items[:10],

            "source":
                "gemini"
        }

    except Exception:

        return fallback(
            planner,
            data
        )