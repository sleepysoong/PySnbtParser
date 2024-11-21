from tags.compound_tag import CompoundTag
from tags.list_tag import ListTag
from tags.byte_tag import ByteTag, ByteArrayTag
from tags.int_tag import IntTag, IntArrayTag
from tags.long_tag import LongTag, LongArrayTag
from tags.float_tag import FloatTag, DoubleTag
from tags.short_tag import ShortTag
from tags.string_tag import StringTag
from tags.tag import Tag


class Parser:
    def __init__(self, snbt: str):
        self.snbt = snbt.strip()
        self.index = 0

    def parse(self) -> Tag:
        return self.parse_value()

    def parse_value(self) -> Tag:
        self.skip_whitespace()
        if self.current_char() == '{':
            return self.parse_compound()
        elif self.current_char() == '[':
            return self.parse_list_or_array()
        elif self.current_char() == '"':
            return self.parse_string()
        else:
            return self.parse_primitive()

    def parse_compound(self) -> CompoundTag:
        self.expect_char('{')
        compound = {}
        while True:
            self.skip_whitespace()
            if self.current_char() == '}':
                self.index += 1
                break
            key = self.parse_key()
            self.expect_char(':')
            value = self.parse_value()
            compound[key] = value
            self.skip_whitespace()
            if self.current_char() == ',':
                self.index += 1
            elif self.current_char() == '}':
                continue
            else:
                raise ValueError(f"예상치 못한 문자: '{self.current_char()}' (인덱스 {self.index})")
        return CompoundTag(compound)

    def parse_list_or_array(self) -> Tag:
        self.expect_char('[')
        if self.peek_chars(2) in ('B;', 'I;', 'L;'):
            array_type = self.current_char()
            self.index += 2
            return self.parse_array(array_type)
        else:
            return self.parse_list()

    def parse_list(self) -> ListTag:
        items = []
        while True:
            self.skip_whitespace()
            if self.current_char() == ']':
                self.index += 1
                break
            item = self.parse_value()
            items.append(item)
            self.skip_whitespace()
            if self.current_char() == ',':
                self.index += 1
            elif self.current_char() == ']':
                continue
            else:
                raise ValueError(f"예상치 못한 문자: '{self.current_char()}' (인덱스 {self.index})")
        return ListTag(items)

    def parse_array(self, array_type: str) -> Tag:
        items = []
        while True:
            self.skip_whitespace()
            if self.current_char() == ']':
                self.index += 1
                break
            value = self.parse_primitive()
            items.append(value.value)
            self.skip_whitespace()
            if self.current_char() == ',':
                self.index += 1
            elif self.current_char() == ']':
                continue
            else:
                raise ValueError(f"예상치 못한 문자: '{self.current_char()}' (인덱스 {self.index})")

        if array_type == 'B':
            return ByteArrayTag(items)
        elif array_type == 'I':
            return IntArrayTag(items)
        elif array_type == 'L':
            return LongArrayTag(items)
        else:
            raise ValueError(f"알 수 없는 배열 타입: '{array_type}'")

    def parse_string(self) -> StringTag:
        self.expect_char('"')
        start = self.index
        while True:
            if self.current_char() == '"':
                value = self.snbt[start:self.index]
                self.index += 1
                return StringTag(value)
            elif self.current_char() == '\\':
                self.index += 2
            else:
                self.index += 1

    def parse_primitive(self) -> Tag:
        start = self.index
        while self.current_char() not in [',', '}', ']', ' ']:
            self.index += 1
            if self.index >= len(self.snbt):
                break
        value_str = self.snbt[start:self.index]
        return self.convert_to_tag(value_str)

    def parse_key(self) -> str:
        self.skip_whitespace()
        if self.current_char() == '"':
            self.expect_char('"')
            start = self.index
            while self.current_char() != '"':
                self.index += 1
            key = self.snbt[start:self.index]
            self.index += 1
            return key
        else:
            start = self.index
            while self.current_char() not in [':', ' ', '\n', '\r', '\t']:
                self.index += 1
            return self.snbt[start:self.index]

    def convert_to_tag(self, value_str: str) -> Tag:
        if value_str.endswith('b'):
            return ByteTag(int(value_str[:-1]))
        elif value_str.endswith('s'):
            return ShortTag(int(value_str[:-1]))
        elif value_str.endswith('l'):
            return LongTag(int(value_str[:-1]))
        elif value_str.endswith('f'):
            return FloatTag(float(value_str[:-1]))
        elif value_str.endswith('d'):
            return DoubleTag(float(value_str[:-1]))
        elif value_str.startswith('"') and value_str.endswith('"'):
            return StringTag(value_str[1:-1])
        elif value_str.isdigit() or (value_str.startswith('-') and value_str[1:].isdigit()):
            return IntTag(int(value_str))
        else:
            return StringTag(value_str)

    def skip_whitespace(self):
        while self.current_char() in [' ', '\n', '\r', '\t']:
            self.index += 1

    def expect_char(self, char: str):
        if self.current_char() != char:
            raise ValueError(f"예상한 문자 '{char}'가 아니라 '{self.current_char()}'를 발견했어요.")
        self.index += 1

    def current_char(self) -> str:
        if self.index >= len(self.snbt):
            return ''
        return self.snbt[self.index]

    def peek_chars(self, count: int) -> str:
        return self.snbt[self.index:self.index+count]