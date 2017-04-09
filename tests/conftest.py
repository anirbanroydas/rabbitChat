import pytest
from rabbitChat.server import main as rabbitChat_app


@pytest.fixture(scope='session')
def app():
    return elastrabbitChat_apper_app
    