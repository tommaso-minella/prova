from unstructured.cleaners.core import (
    replace_unicode_quotes,
    clean_bullets,
    clean_dashes,
    clean_trailing_punctuation,
    clean_non_ascii_chars,
    clean_extra_whitespace,
    clean_ordered_bullets,
    group_broken_paragraphs,
)
from unstructured.documents.elements import Text


def clean_content(elements):
    cleaned_elements = []
    for element in elements:
        if isinstance(element, Text):
            if element.text:  # Ensure the text is not empty
                element.apply(replace_unicode_quotes)
                element.apply(clean_bullets)
                element.apply(clean_dashes)
                element.apply(clean_trailing_punctuation)
                element.apply(clean_non_ascii_chars)
                element.apply(clean_extra_whitespace)
                element.apply(group_broken_paragraphs)
                if element.text:
                    element.apply(clean_ordered_bullets)
        cleaned_elements.append(element)
    return cleaned_elements