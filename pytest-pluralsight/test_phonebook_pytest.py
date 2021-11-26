import pytest
from phonebook import PhoneBook

# @pytest.fixture
# def phonebook():
#     # modifying fixture to clear external resources
#     phonebook = PhoneBook()
#     yield phonebook
#     phonebook.clear()


@pytest.fixture
def phonebook(tmpdir):
    # pytest provides tempdir which will be used as temp dir
    # and delete it after test is executed
    return PhoneBook(tmpdir)


def test_lookup_by_name(phonebook):
    phonebook.add("Bob", "12345")
    number = phonebook.lookup("Bob")
    assert "12345" == number


@pytest.mark.xfail(raises=AssertionError)
def test_phonebook_adds_name_and_number(phonebook):
    phonebook.add("Bob", "12345")
    assert set(phonebook.get_names()) == {"Bob", "Missing"}


def test_phonebook_contains_all_names(phonebook):
    phonebook.add("Bob", "12345")
    assert "Bob" in set(phonebook.get_names())


def test_missing_name_raises_error(phonebook):
    with pytest.raises(KeyError):
        phonebook.lookup("Bob")


@pytest.mark.xfail
def test_missing_name_raises_error2(phonebook):
    phonebook.add("Bob", "12345")
    with pytest.raises(KeyError):
        phonebook.lookup("Bob")


# class PhoneBookTest(unittest.TestCase):
#     def setUp(self) -> None:
#         self.phonebook = PhoneBook()
#         return super().setUp()

#     def tearDown(self) -> None:
#         return super().tearDown()

#     def test_lookup_by_name(self):
#         self.phonebook.add("Bob", "12345")
#         number = self.phonebook.lookup("Bob")
#         self.assertEqual("12345", number)

#     def test_missing_name(self):
#         with self.assertRaises(KeyError):
#             self.phonebook.lookup("missing")

#     @unittest.skip("WIP")
#     def test_empty_phonebook_is_consistent(self):
#         self.assertTrue(self.phonebook.is_consistent())

#     def test_is_consistent_with_different_entries(self):
#         self.phonebook.add("Bob", "12345")
#         self.phonebook.add("Ana", "012345")
#         self.assertTrue(self.phonebook.is_consistent())

#     def test_inconsistent_with_duplicate_entries(self):
#         self.phonebook.add("Bob", "12345")
#         self.phonebook.add("Sue", "12345")
#         self.assertFalse(self.phonebook.is_consistent())

#     def test_inconsistent_with_duplicate_prefix(self):
#         self.phonebook.add("Bob", "12345")
#         self.phonebook.add("Sue", "123")
#         self.assertFalse(self.phonebook.is_consistent())

#     def test_phonebook_adds_name_and_number(self):
#         self.phonebook.add("Bob", "12345")
#         self.assertIn("Bob", self.phonebook.get_names())
#         self.assertIn("12345", self.phonebook.get_numbers())
