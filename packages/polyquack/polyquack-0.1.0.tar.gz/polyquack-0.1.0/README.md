# polyquack

## Preamble

`polyquack` is a utility (possibly part of a larger set in the future) for pluralizing words based on rules of varying complexity.

It has been inspired by the [*Localization and Plurals* page](https://developer.mozilla.org/en-US/docs/Mozilla/Localization/Localization_and_Plurals) from the MDN.

## Installation

Simply run `pip install polyquack`.

## Usage

First, define a list of forms. It is a simple `dict` with language codes as keys. For now, refer to the `tests/test_pluralization.py` file to see the form definitions by rule, and the `rules.py` file for a mapping of languages to rules. Not all languages have the same number of forms (for instance, slavic languages often have a genitive plural form).

    >>> song_forms = {
    ...     "en": ["song", "songs"],
    ...     "fr": ["chanson", "chansons"],
    ...     "pl": ["piosenka", "piosenki", "piosenek"],
    ... }

This package provides a handy `Pluralizable` class that you can use.

    >>> song = pluralization.Pluralizable(forms=song_forms)
    >>> print(f"4 {song.pluralize_by_language('pl', 4)}") # nominative plural
    4 piosenki
    >>> print(f"5 {song.pluralize_by_language('pl', 5)}") # genitive plural
    5 piosenek

## Todo

This project is barely a few days old. I will be adding proper documentation, and `tox` for testing.