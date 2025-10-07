class HTMLNode():
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def __eq__(self, other):
		return

	def __repr__(self):
    		return (
        		f"HTMLNode(\n"
        		f"  tag={self.tag!r},\n"
        		f"  value={self.value!r},\n"
        		f"  children={self.children!r},\n"
        		f"  props={self.props!r}\n"
        		f")"
    		)


	def to_html(self):
		raise NotImplementedError()

	def props_to_html(self):
		prop_string = ""
		for key, value in self.props.items():
			prop_string += f' {key}="{value}"'
		return prop_string
