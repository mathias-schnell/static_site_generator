from htmlnode import HTMLNode

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children or [], props or {})

	def __eq__(self, other):
		if not isinstance(other, ParentNode):
			return False
		return (
        		self.tag == other.tag
            	and self.children == other.children
            	and self.props == other.props
        )

	def __repr__(self):
		return (
			f"ParentNode(\n"
			f"  tag={self.tag!r},\n"
			f"  children={self.children!r},\n"
			f"  props={self.props!r}\n"
			f")"
		)


	def to_html(self):
		if self.tag is None:
			raise ValueError("ParentNode must have a tag.")

		if not self.children:
			raise ValueError("ParentNode must have children.")

		prop_str = self.props_to_html()
		html_str = f"<{self.tag}{prop_str}>"

		for child in self.children:
			html_str += child.to_html()

		html_str += f"</{self.tag}>"
		return html_str
