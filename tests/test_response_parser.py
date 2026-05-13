"""Tests for response parser."""
import pytest
from src.inference.response_parser import ResponseParser


@pytest.mark.unit
def test_parse_json_valid():
    """Test parsing valid JSON."""
    response = '{"name": "test", "value": 123}'

    result = ResponseParser.parse_json(response)

    assert result == {"name": "test", "value": 123}


@pytest.mark.unit
def test_parse_json_embedded():
    """Test parsing JSON embedded in text."""
    response = 'Here is the data: {"name": "test", "value": 123} and more text'

    result = ResponseParser.parse_json(response)

    assert result == {"name": "test", "value": 123}


@pytest.mark.unit
def test_parse_json_invalid():
    """Test parsing invalid JSON."""
    response = "This is not JSON"

    result = ResponseParser.parse_json(response)

    assert result is None


@pytest.mark.unit
def test_parse_list_bullets():
    """Test parsing bulleted list."""
    response = """
    - Item 1
    - Item 2
    - Item 3
    """

    result = ResponseParser.parse_list(response)

    assert len(result) == 3
    assert "Item 1" in result


@pytest.mark.unit
def test_parse_list_numbered():
    """Test parsing numbered list."""
    response = """
    1. First item
    2. Second item
    3. Third item
    """

    result = ResponseParser.parse_list(response)

    assert len(result) == 3
    assert "First item" in result


@pytest.mark.unit
def test_extract_code_blocks():
    """Test extracting code blocks."""
    response = """
    Here is some code:
    ```python
    def hello():
        print("Hello")
    ```
    And more:
    ```javascript
    console.log("Hi");
    ```
    """

    result = ResponseParser.extract_code_blocks(response)

    assert len(result) == 2
    assert result[0]["language"] == "python"
    assert "def hello()" in result[0]["code"]
    assert result[1]["language"] == "javascript"


@pytest.mark.unit
def test_clean_response():
    """Test response cleaning."""
    response = "  Text   with   extra   \n\n\n\n   whitespace  "

    result = ResponseParser.clean_response(response)

    assert result == "Text   with   extra\n\nwhitespace"
