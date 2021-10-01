import sys
from pathlib import Path


p = Path(__file__).parent.parent

sys.path.append(str(p / "hero-app"))
