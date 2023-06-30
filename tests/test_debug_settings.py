# explicit import to override pytest switch automation
from kittygram_backend import settings


def test_debug_turn_off():
    assert not settings.DEBUG, (
        'Убедидесь, что для параметра `DEBUG` в файле настроек `settings.py` '
        'бекэнд части проекта `Kittygram` установлено значение `False`.'
    )
