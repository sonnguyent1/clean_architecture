import pytest

from clean_architecture.rest.app import create_app
from clean_architecture.rest.settings import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app
