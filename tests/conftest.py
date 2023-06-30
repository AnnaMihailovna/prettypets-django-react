import re
from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR_NAME = 'backend'
FRONTEND_DIR_NAME = 'frontend'
INFRA_DIR_NAME = 'infra'
DEPLOY_INFO_FILE_NAME = 'kittygram_site.txt'
KITTYGRAM_LINK_KEY = 'name_kittygram'
TASKI_LINK_KEY = 'name_taski'

for dir_name in (BACKEND_DIR_NAME, FRONTEND_DIR_NAME, INFRA_DIR_NAME):
    path_to_dir = BASE_DIR / dir_name
    if not path_to_dir.is_dir():
        raise AssertionError(
            f'В директории `{BASE_DIR}` не найдена папка проекта '
            f'`{dir_name}/`. Убедитесь, что у вас верная структура проекта.'
        )


@pytest.fixture(scope='session')
def infra_dir_info():
    return (BASE_DIR / INFRA_DIR_NAME, INFRA_DIR_NAME)


@pytest.fixture(scope='session')
def expected_infra_files():
    return {DEPLOY_INFO_FILE_NAME, 'default', 'gunicorn_kittygram.service'}


@pytest.fixture(scope='session')
def deploy_info_file_info(infra_dir_info):
    path, dir_name = infra_dir_info
    deploy_info_file = path / DEPLOY_INFO_FILE_NAME
    assert deploy_info_file.is_file(), (
        f'Убедитесь, что в директории `{dir_name}/` создан файл '
        f'`{DEPLOY_INFO_FILE_NAME}`'
    )
    return (deploy_info_file, f'{dir_name}/{DEPLOY_INFO_FILE_NAME}')


@pytest.fixture(scope='session')
def deploy_info_file_content(deploy_info_file_info):
    path, relative_path = deploy_info_file_info
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = {}
        line_pattern = re.compile(r'[\w_]+: ?[^;]+;')
        for line_num, line in enumerate(f.readlines(), 1):
            if not line.strip():
                continue
            assert line_pattern.match(line), (
                f'Убедитесь, что строка номер {line_num} файла '
                f'`{relative_path}` соответствует шаблону: '
                '`<ключ>: <значение>;`. В названии ключа '
                'допустимы буквы и нижнее подчеркивание.'
            )
            line = line.strip().strip(';')
            key, value = line.split(':', maxsplit=1)
            file_content[key.strip()] = value.strip()
    return file_content


@pytest.fixture(scope='session')
def expected_deploy_info_file_content():
    return {
        'IP': 'IP-адрес сервера',
        TASKI_LINK_KEY: 'ссылка для доступа к проекту `Taski`',
        KITTYGRAM_LINK_KEY: 'ссылка для доступа к проекту Kittygram',
        'login': 'логин',
        'password': 'пароль'
    }


@pytest.fixture(params=(TASKI_LINK_KEY, KITTYGRAM_LINK_KEY))
def link_key(request):
    return request.param
