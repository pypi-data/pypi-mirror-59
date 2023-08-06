import json

from config_file.parsers.base_parser import BaseParser, ParsingError
from config_file.parsers.parse_value import parse_value


class JsonParser(BaseParser):

    def __init__(self, file_contents: str):
        """Reads in the file contents into the parser."""
        super().__init__(file_contents)

    def parse(self, file_contents: str):
        try:
            return json.loads(file_contents)
        except json.decoder.JSONDecodeError as error:
            raise ParsingError(error)

    def get(self, section_key, parse_type=True):
        pass

    def set(self, section_key, value):
        pass

    def delete(self, section_key):
        pass

    def stringify(self) -> str:
        return json.dumps(self.parsed_content)

    def has(self, search_key: str) -> bool:
        return self._search(self.parsed_content, search_key)

    def _search(self, data: dict, match: str):
        for key, value in data.items():
            if key == match:
                return True
            elif isinstance(value, dict):
                self._search(value, match)

        return False
