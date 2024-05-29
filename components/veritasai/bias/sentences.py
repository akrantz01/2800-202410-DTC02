def chunk_sentence(sentence: str) -> list[str]:
    """
    Chunk a sentence into smaller parts.

    :param sentence: a string of text
    :return: a list of strings
    """
    minimum_scan_size = 15
    tokens = sentence.split(" ")
    segments_to_scan = []
    current_segment = ""
    for token in tokens:
        if len(current_segment) < minimum_scan_size:
            current_segment += " "
        else:
            segments_to_scan.append(current_segment)
            current_segment = ""

        current_segment += token
    segments_to_scan[-1] = segments_to_scan[-1] + " " + current_segment

    return segments_to_scan
