from django.apps import apps


def test_administration_app_is_installed():
    assert apps.is_installed("administration")
