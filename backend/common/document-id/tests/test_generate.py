from document_id import generate


def test_empty_content():
    result = generate("")
    assert result == "7uL4nSE_CEOnSJufwAJYzR2I3JULGmDbEiaOi82Qch8="


def test_content_only():
    result = generate("Hello, world!")
    assert result == "O4zSymKk7nPkQPdq3VRRHlXho0-HbQe0YU1rEIUDxMQ="


def test_content_and_author():
    result = generate("Hello, world!", "Alice")
    assert result == "gddVl_z1153y3qEqvF3O6u0fjeo-ghpPD-T0W6RqgZ0="


def test_content_and_source():
    result = generate("Hello, world!", source="Twitter")
    assert result == "XSceRAmkngNM9NVuL9FeDricbCrrPkw8SgvFF9uIVFQ="


def test_content_author_and_source():
    result = generate("Hello, world!", "Alice", "Twitter")
    assert result == "5tJzOBEpdq0udVD1pAu0V_pn58pvAdaisOlpojBWg2k="


def test_cannot_cause_collision_with_author():
    just_content = generate("Hello there")
    with_author = generate("Hello", " there")
    assert just_content != with_author


def test_cannot_cause_collision_with_source():
    just_content = generate("Hello there")
    with_source = generate("Hello", source=" there")
    assert just_content != with_source


def test_cannot_cause_collision_with_author_and_source():
    just_content = generate("Hello there")
    with_author_and_source = generate("Hello", " ", " there")
    assert just_content != with_author_and_source


def test_whitespace_surrounding_content_is_ignored():
    without_whitespace = generate("Hello, world!")
    with_whitespace = generate(" \t Hello, world!\r\n ")
    assert without_whitespace == with_whitespace


def test_whitespace_surrounding_author_is_ignored():
    without_whitespace = generate("Hello, world!", "Alice")
    with_whitespace = generate("Hello, world!", " \t Alice\r\n ")
    assert without_whitespace == with_whitespace


def test_whitespace_surrounding_source_is_ignored():
    without_whitespace = generate("Hello, world!", source="Twitter")
    with_whitespace = generate("Hello, world!", source=" \t Twitter\r\n ")
    assert without_whitespace == with_whitespace


def test_all_surrounding_whitespace_is_ignored():
    without_whitespace = generate("Hello, world!", "Alice", "Twitter")
    with_whitespace = generate("\t \nHello, world!\r\n", " \t Alice\r\n ", " \t Twitter\r\n ")
    assert without_whitespace == with_whitespace
