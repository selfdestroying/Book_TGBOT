BOOK_PATH = './book/book.txt'
PAGE_SIZE = 1050

book = {}


# Returns page size and string with page text
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    word_verification = text.split()
    while 1:
        text_result = text[start:][:size]
        if text_result.split()[-1] not in word_verification or text_result[-1] not in '.,!?;:':
            size -= 1
        else:
            break
    return text_result, len(text_result)


# Create book dictionary
def prepare_book(path: str) -> None:
    page_number = 1
    with open(path, 'r', encoding='UTF-8') as f:
        file = f.read()
        while file != '':
            page = _get_part_text(file, 0, PAGE_SIZE)
            book[page_number] = page[0].lstrip()
            page_number += 1
            start = page[1]
            file = file[start:]


prepare_book(BOOK_PATH)
