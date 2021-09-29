#!/usr/bin/env python3
 
import pytest
from .context import Phonebook


@pytest.fixture
def phonebook(tmpdir):
    "Provides an empty phonebook"
    return Phonebook(tmpdir)

def test_lookup_by_name(phonebook):
    phonebook.add("Bob", "1234")
    assert "1234" == phonebook.lookup("Bob")

def test_phonebook_contains_all_names(phonebook):
    phonebook.add("Bob", "1234")
    assert"Bob" in phonebook.names()

def test_missing_key_raises_error(phonebook):
    with pytest.raises(KeyError):
        phonebook.lookup("Bob")