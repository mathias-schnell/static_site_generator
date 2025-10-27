from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UL = "unordered list"
	OL = "ordered list"