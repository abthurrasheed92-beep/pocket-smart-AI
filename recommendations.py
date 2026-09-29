def link(
    platform: str,
    name: str
) -> str:

    from urllib.parse import quote_plus

    query = quote_plus(name)

    urls = {

        "Amazon":
            f"https://www.amazon.in/s?k={query}",

        "Flipkart":
            f"https://www.flipkart.com/search?q={query}",

        "IKEA":
            f"https://www.ikea.com/in/en/search/?q={query}",

        "Swiggy":
            f"https://www.swiggy.com/search?query={query}",

        "Zomato":
            f"https://www.zomato.com/search?query={query}",

        "OYO":
            f"https://www.oyorooms.com/search?location={query}"
    }

    return urls.get(
        platform,
        urls["Amazon"]
    )


def fallback(
    planner: str,
    data: dict
):

    budget = float(
        data["budget"]
    )

    if planner == "home":

        recommendations = [

            {
                "category": "Furniture",
                "name": "Modern Accent Chair",
                "estimated_price": round(
                    budget * 0.20,
                    2
                ),
                "platform": "Amazon",
                "reason":
                    "A compact chair can improve the room's comfort and appearance."
            },

            {
                "category": "Lighting",
                "name": "Warm LED Floor Lamp",
                "estimated_price": round(
                    budget * 0.12,
                    2
                ),
                "platform": "IKEA",
                "reason":
                    "Warm lighting creates a comfortable modern atmosphere."
            },

            {
                "category": "Decor",
                "name": "Minimal Wall Decor Set",
                "estimated_price": round(
                    budget * 0.10,
                    2
                ),
                "platform": "Flipkart",
                "reason":
                    "Simple wall decor can add personality without using too much budget."
            },

            {
                "category": "Storage",
                "name": "Compact Storage Cabinet",
                "estimated_price": round(
                    budget * 0.18,
                    2
                ),
                "platform": "IKEA",
                "reason":
                    "Useful storage keeps the room organized."
            }
        ]

        summary = (
            f"Budget-friendly {data.get('style', 'Modern')} "
            f"plan for your {data.get('room_type', 'room')}."
        )

        allocations = {
            "Furniture": 40,
            "Lighting": 20,
            "Decor": 15,
            "Storage": 25
        }

    elif planner == "party":

        per_person = (
            budget /
            max(int(data["guests"]), 1)
        )

        recommendations = [

            {
                "category": "Food",
                "name": f"{data.get('event_type', 'Party')} Food Package",
                "estimated_price": round(
                    budget * 0.40,
                    2
                ),
                "platform": "Swiggy",
                "reason":
                    f"Food allocation is based on {data['guests']} guests."
            },

            {
                "category": "Decor",
                "name": "Party Decoration Package",
                "estimated_price": round(
                    budget * 0.15,
                    2
                ),
                "platform": "Amazon",
                "reason":
                    "Basic decorations provide a themed party setup."
            },

            {
                "category": "Venue",
                "name": "Event Venue Search",
                "estimated_price": round(
                    budget * 0.25,
                    2
                ),
                "platform": "OYO",
                "reason":
                    "Useful when you need a flexible venue or stay option."
            },

            {
                "category": "Dessert",
                "name": "Party Cake",
                "estimated_price": round(
                    budget * 0.10,
                    2
                ),
                "platform": "Zomato",
                "reason":
                    "Dessert can be adjusted based on guest count."
            }
        ]

        summary = (
            f"{data.get('event_type', 'Party')} plan "
            f"for {data['guests']} guests."
        )

        allocations = {
            "Food": 40,
            "Decor": 15,
            "Venue": 25,
            "Dessert": 10,
            "Buffer": 10
        }

    else:

        recommendations = [

            {
                "category": "Necklace",
                "name": f"{data.get('style', 'Elegant')} Necklace",
                "estimated_price": round(
                    budget * 0.35,
                    2
                ),
                "platform": "Amazon",
                "reason":
                    "A necklace is a versatile option for the selected occasion."
            },

            {
                "category": "Earrings",
                "name": "Matching Statement Earrings",
                "estimated_price": round(
                    budget * 0.20,
                    2
                ),
                "platform": "Flipkart",
                "reason":
                    "Earrings can complement the outfit without dominating it."
            },

            {
                "category": "Bangles",
                "name": "Elegant Bangle Set",
                "estimated_price": round(
                    budget * 0.15,
                    2
                ),
                "platform": "Amazon",
                "reason":
                    "A small bangle set adds coordinated detail."
            }
        ]

        summary = (
            f"{data.get('style', 'Elegant')} jewelry "
            f"recommendations for {data.get('occasion', 'your occasion')}."
        )

        allocations = {
            "Necklace": 40,
            "Earrings": 25,
            "Bangles": 20,
            "Buffer": 15
        }

    total = 0
    final_items = []

    for item in recommendations:

        price = float(
            item["estimated_price"]
        )

        if total + price <= budget:

            item["search_url"] = link(
                item["platform"],
                item["name"]
            )

            final_items.append(item)

            total += price

    return {
        "planner": planner,
        "budget": budget,
        "budget_used": round(
            total,
            2
        ),
        "summary": summary,
        "allocations": allocations,
        "recommendations": final_items,
        "source": "demo"
    }