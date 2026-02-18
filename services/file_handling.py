import logging

logger = logging.getLogger(__name__)


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    delimiters = [",", ".", "!", ":", ";", "?"]
    page_text = text[start:start + size]
    if len(text) > start + size:
        if text[start + size] in delimiters:
            while page_text and page_text[-1] in delimiters:
                page_text = page_text[:-1]
    elif len(text) < start + size:
        page_text = text[start:]

    last_delimiter_pos = -1
    for i, c in enumerate(page_text):
        if c in delimiters:
            last_delimiter_pos = i

    if last_delimiter_pos == -1:
        return page_text, len(page_text)

    page_text = page_text[:last_delimiter_pos + 1]

    return page_text, len(page_text)


def prepare_book(path: str, size: int = 1050) -> dict[int, str]:
    book={}
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        start = 0
        current_page = 1
        while start < len(text):
            page_text, page_size = _get_part_text(text, start, size)

            if not page_text.strip():
                break

            book[current_page] = page_text.lstrip()
            start += page_size
            current_page += 1

    return book