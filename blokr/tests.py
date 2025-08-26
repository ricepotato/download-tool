from pathlib import Path
from django.test import TestCase
from .cleaner import clean_content


# Create your tests here.
class AnimalTestCase(TestCase):
    def setUp(self):
        pass

    def test_cleaner1(self):
        origin1 = Path(
            "blokr_data/5445a6e1-99b2-4035-822a-06191669bcb8/index_origin.html"
        )
        output = Path("blokr_data/5445a6e1-99b2-4035-822a-06191669bcb8/index.html")

        clean_content(origin1, output)

    def test_cleaner2(self):
        origin1 = Path(
            "blokr_data/4eece747-706f-4e42-8ea2-6644b0fc5118/index_origin.html"
        )
        output = Path("blokr_data/4eece747-706f-4e42-8ea2-6644b0fc5118/index.html")

        clean_content(origin1, output)

    def test_cleaner3(self):
        origin1 = Path(
            "blokr_data/3e3975ff-0772-4919-a015-8e0137ddeb8f/index_origin.html"
        )
        output = Path("blokr_data/3e3975ff-0772-4919-a015-8e0137ddeb8f/index.html")

        clean_content(origin1, output)
