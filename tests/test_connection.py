import re
from http import HTTPStatus

import pytest
import requests


def validate_link(
        path_to_deploy_info_file, deploy_info_file_content, link_key
        ) -> str:
    assert link_key in deploy_info_file_content, (
        f'Убедитесь, что файл `{path_to_deploy_info_file}` содержит ключ '
        f'`{link_key}`.'
    )
    link: str = deploy_info_file_content[link_key]
    assert link.startswith('https'), (
        f'Убедитесь, что cсылка ключ `{link_key}` в файле '
        f'`{path_to_deploy_info_file}` содержит ссылку, которая начинается с '
        'префикса `https`.'
    )
    link_pattern = re.compile(
        r'^https:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.'
        r'[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    )
    assert link_pattern.match(link), (
        f'Убедитесь, что ключ `{link_key}` в файле '
        f'`{path_to_deploy_info_file}` содержит корректную ссылку.'
    )
    return link


def test_link_connection(
        deploy_info_file_info, deploy_info_file_content, link_key
        ):
    _, relative_path = deploy_info_file_info
    link = validate_link(relative_path, deploy_info_file_content, link_key)
    try:
        response = requests.get(link)
    except requests.exceptions.SSLError:
        raise AssertionError(
            f'Убедитесь, что настроили шифрование для `{link}`.'
        )
    except requests.exceptions.ConnectionError:
        raise AssertionError(
            f'Убедитесь, что URL `{link}` доступен.'
        )
    expected_status = HTTPStatus.OK
    assert response.status_code == expected_status, (
        f'Убедитесь, что GET-запрос к `{link}` возвращает ответ со статусом '
        f'{int(expected_status)}.'
    )
    cats_project_name = 'Kittygram'
    assert_msg_template = (
        f'Убедитесь, что по ссылке `{link}` доступен проект '
        '`{project_name}`.'
    )
    if link_key == 'name_kittygram':
        assert cats_project_name in response.text, (
            assert_msg_template.format(project_name=cats_project_name)
        )
    else:
        assert cats_project_name not in response.text, (
            assert_msg_template.format(project_name='Taski')
        )


if __name__ == '__main__':
    pytest.main()
