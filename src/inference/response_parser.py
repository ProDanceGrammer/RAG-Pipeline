import json
import re
from typing import Any, Dict, List, Optional


class ResponseParser:
    """Parse and format LLM outputs."""

    @staticmethod
    def parse_json(response: str) -> Optional[Dict[str, Any]]:
        """Extract and parse JSON from response."""
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    return None
        return None

    @staticmethod
    def parse_list(response: str) -> List[str]:
        """Extract list items from response."""
        lines = response.strip().split('\n')
        items = []

        for line in lines:
            line = line.strip()
            if line.startswith(('-', '*', '•')):
                items.append(line[1:].strip())
            elif re.match(r'^\d+\.', line):
                items.append(re.sub(r'^\d+\.\s*', '', line))
            elif line:
                items.append(line)

        return items

    @staticmethod
    def extract_code_blocks(response: str) -> List[Dict[str, str]]:
        """Extract code blocks from markdown response."""
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, response, re.DOTALL)

        code_blocks = []
        for language, code in matches:
            code_blocks.append({
                'language': language or 'text',
                'code': code.strip()
            })

        return code_blocks

    @staticmethod
    def clean_response(response: str) -> str:
        """Clean and normalize response text."""
        response = response.strip()
        response = re.sub(r'\n{3,}', '\n\n', response)
        return response

    @staticmethod
    def format_as_markdown(response: str) -> str:
        """Format response as markdown."""
        response = ResponseParser.clean_response(response)

        if not response.startswith('#'):
            response = f"# Response\n\n{response}"

        return response
