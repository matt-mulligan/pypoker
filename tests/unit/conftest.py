import sys
from pathlib import Path
from pytest import fixture

from pypoker.constructs import Card

here = Path(__file__).absolute()
tests_path = here.parent.parent
src_path = here.parent.parent.parent / "src"
fixtures_path = tests_path / "fixtures"

sys.path.insert(0, str(src_path))


@fixture
def get_test_cards():
    """
    test helper method to get card objects
    """

    def _get_test_cards(card_ids: str):
        card_ids = card_ids.split("|")
        return [Card(card_id) for card_id in card_ids]

    return _get_test_cards
