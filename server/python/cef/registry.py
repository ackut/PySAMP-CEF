from typing import TYPE_CHECKING, Optional

from .exceptions import BrowserAlreadyExistsForPlayer

if TYPE_CHECKING:
    from .browser import Browser


class BrowserRegistry:
    _data: dict[int, 'Browser'] = {}  # player_id: Browser

    @classmethod
    def add(cls, browser: 'Browser') -> None:
        if browser.id in cls._data:
            raise BrowserAlreadyExistsForPlayer(
                f'{browser.id=} already exists'
            )
        cls._data[browser.id] = browser

    @classmethod
    def get(cls, player_id: int) -> Optional['Browser']:
        return cls._data.get(player_id)

    @classmethod
    def remove(cls, browser: 'Browser') -> bool:
        if browser.id in cls._data:
            del cls._data[browser.id]
            return True
        return False

    @classmethod
    def exists(cls, player_id: int, ) -> bool:
        return player_id in cls._data
