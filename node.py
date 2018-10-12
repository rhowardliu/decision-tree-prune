class Node:
  def __init__(self, label=None):
    self.label = label
    self.children = {}
	# you may want to add additional fields here...
    self.name = None
    self.parent = None
    self.pathFromParent = None