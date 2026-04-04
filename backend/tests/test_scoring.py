from app.services.scoring import compute_score


def test_scoring_range_and_levels():
    res = compute_score('Depozio', 'Depozio Pro', 1.0, 1.0)
    assert 0 <= res['score'] <= 100
    assert res['risk_level'] in {'green', 'orange', 'red'}
