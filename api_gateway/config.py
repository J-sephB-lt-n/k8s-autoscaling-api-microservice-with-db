"""Constants controlling project behaviour"""

from typing import Final

HEADERS_TO_FORWARD: Final[tuple[str, ...]] = tuple([word.lower() for word in ("Content-Type",)]) 

ORIGINS_ALLOW: Final[tuple[str|None, ...]] = (None,)
