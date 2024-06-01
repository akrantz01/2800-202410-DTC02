MINIMUM_SCAN_SIZE = 15


def chunk_sentence(sentence: str) -> list[str]:
    """
    Chunk a sentence into smaller parts.

    :param sentence: a string of text
    :return: a list of strings
    """
    if len(sentence) < MINIMUM_SCAN_SIZE:
        return [sentence]

    tokens = sentence.split(" ")
    segments_to_scan = []
    current_segment = ""
    for token in tokens:
        if len(current_segment) < MINIMUM_SCAN_SIZE:
            current_segment += " "
        else:
            segments_to_scan.append(current_segment)
            current_segment = ""

        current_segment += token
    if segments_to_scan:
        segments_to_scan[-1] = segments_to_scan[-1] + " " + current_segment

    return segments_to_scan
