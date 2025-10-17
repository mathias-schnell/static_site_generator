from htmlnode import HTMLNode

class LeafNode(HTMLNode):
	def __init__(self, tag = None, value = None, props = None):
		super().__init__(tag, value, None, props or {})

	def __eq__(self, other):
		if not isinstance(other, LeafNode):
			return False
		return (
        	self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )

	def __repr__(self):
		return (
			f"LeafNode(\n"
			f"  tag={self.tag!r},\n"
			f"  value={self.value!r},\n"
			f"  props={self.props!r}\n"
			f")"
		)


	def to_html(self):
		if self.value is None and self.tag != "img":
			raise ValueError("LeafNode must have a value unless it is an <img> tag.")

		if self.tag is None:
			return self.value

		prop_str = self.props_to_html()

		# HTML void elements that should not have closing tags
		void_tags = {"img", "br", "hr", "input", "meta", "link"}

		if self.tag in void_tags:
			return f"<{self.tag}{prop_str}>"

		return f"<{self.tag}{prop_str}>{self.value}</{self.tag}>"
