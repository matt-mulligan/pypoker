import sys
from pathlib import Path

here = Path(__file__).absolute()
tests_path = here.parent.parent
src_path = here.parent.parent.parent / "src"
fixtures_path = tests_path / "fixtures"

sys.path.insert(0, str(src_path))
