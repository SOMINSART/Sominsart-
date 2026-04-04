def suggest_classes(activity_description: str) -> list[int]:
    text = activity_description.lower()
    mapping = {
        'software': 9,
        'clothing': 25,
        'food': 30,
        'education': 41,
        'finance': 36,
        'beauty': 3,
    }
    picks = [v for k, v in mapping.items() if k in text]
    return picks or [35]


def generate_recommendations(brand_name: str) -> dict:
    return {
        'alternatives': [f'{brand_name}ly', f'Neo{brand_name}', f'{brand_name}Nova'],
        'advice': 'Prioritize class precision and territory consistency before filing.',
    }
