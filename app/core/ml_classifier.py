# Простой rule-based классификатор
CATEGORY_RULES = {
    "Еда": ["бургер", "kfc", "макдоналдс", "пятёрочка", "магнит", "обед", "продукты", "кафе", "ресторан", "вкусвилл"],
    "Транспорт": ["такси", "метро", "бензин", "автобус", "яндекс go", "заправка", "каршеринг"],
    "Развлечения": ["кино", "netflix", "игра", "steam", "концерт", "бар", "пиво"],
    "Здоровье": ["аптека", "врач", "больница", "лекарства", "спортзал", "фитнес"],
    "Жилье": ["аренда", "квартира", "коммуналка", "жкх", "интернет", "ремонт"]
}

def predict_category(description: str) -> str:
    """Определяет категорию расхода на основе описания."""
    if not description:
        return "Разное"
    
    description = description.lower()
    
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in description:
                return category
                
    return "Разное"