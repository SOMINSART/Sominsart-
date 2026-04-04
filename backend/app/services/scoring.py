from difflib import SequenceMatcher


def _sim(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100


def compute_score(brand: str, candidate: str, classes_overlap: float, territory_overlap: float) -> dict:
    phonetic = _sim(brand[:4], candidate[:4])
    visual = _sim(brand, candidate)
    conceptual = 80.0 if brand.split()[0].lower() == candidate.split()[0].lower() else _sim(brand[::-1], candidate[::-1])
    class_prox = classes_overlap * 100
    terr = territory_overlap * 100

    weighted = (
        phonetic * 0.30
        + visual * 0.25
        + conceptual * 0.20
        + class_prox * 0.15
        + terr * 0.10
    )
    score = round(weighted, 2)
    level = 'green' if score <= 30 else 'orange' if score <= 65 else 'red'
    return {
        'score': score,
        'risk_level': level,
        'breakdown': {
            'phonetic': round(phonetic, 2),
            'visual': round(visual, 2),
            'conceptual': round(conceptual, 2),
            'class_proximity': round(class_prox, 2),
            'territory_overlap': round(terr, 2),
        },
    }
