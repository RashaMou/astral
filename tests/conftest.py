import pytest
from astral.api import API
from webtest import TestApp

@pytest.fixture
def api():
    return API()

@pytest.fixture
def client(api):
    return TestApp(api)
