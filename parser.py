import re
from bs4 import BeautifulSoup
from models import MenuItem, RestaurantData


def parse_swiggy_html(html_content: str, url: str) -> RestaurantData:
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Restaurant Name extraction with URL slug fallback
    restaurant_name = "Unknown Restaurant"
    h1_tag = soup.find("h1")

    if (
        h1_tag
        and h1_tag.text.strip()
        and "Order Food Online" not in h1_tag.text
    ):
        restaurant_name = h1_tag.text.strip()
    else:
        # URL se clean name nikalo agar title blank/generic aaye
        try:
            slug = url.split("/city/ahmedabad/")[1].split("-rest")[0]
            restaurant_name = slug.replace("-", " ").title()
        except Exception:
            restaurant_name = "Swiggy Restaurant"

    # 2. Dish cards extraction
    menu_items = []
    dish_cards = soup.find_all("div", {"data-testid": "normal-dish-item"})

    if not dish_cards:
        dish_cards = soup.find_all(
            "div", {"class": lambda c: c and "styles_container" in str(c)}
        )

    for card in dish_cards:
        # Item Name
        name_node = card.find("h3") or card.find(
            "div",
            {
                "class": lambda c: c
                and ("name" in str(c).lower() or "title" in str(c).lower())
            },
        )
        name = name_node.text.strip() if name_node else None

        if not name:
            continue

        # Item Price
        price_text = "N/A"
        price_nodes = card.find_all(["span", "div", "p"])
        for p_node in price_nodes:
            text = p_node.text.strip().replace("₹", "").strip()
            if text.isdigit() and len(text) <= 5 and int(text) > 10:
                price_text = text
                break

        # Description Fix
        description = "No description available"
        desc_node = card.find(
            "p",
            {
                "class": lambda c: c
                and ("desc" in str(c).lower() or "styles_itemDesc" in str(c))
            },
        )
        if not desc_node:
            desc_node = card.find(
                "div", class_=lambda c: c and "itemDesc" in str(c)
            )

        if desc_node and desc_node.text.strip():
            description = desc_node.text.strip()

        menu_items.append(
            MenuItem(name=name, price=price_text, description=description)
        )

    return RestaurantData(
        restaurant_name=restaurant_name,
        url=url,
        total_items=len(menu_items),
        menu=menu_items,
    )