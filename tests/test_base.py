"""
test for base python template
"""
from src import main


def test_base():
    assert hasattr(main, "main")
