from app.services.assistant import suggest_classes


def test_suggest_classes():
    out = suggest_classes('software and finance services')
    assert 9 in out and 36 in out
