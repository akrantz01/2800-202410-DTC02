from veritasai.config import location


def test_pytest_is_always_test_environment():
    assert location.name == "test"
    assert not location.is_development
    assert not location.is_production
