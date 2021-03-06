from ID3 import *
import unittest

class ID3test(unittest.TestCase):
  def test_checkSameClassificationT(self):
    examplesTrue = [dict(a=1, b=1, Class=1), dict(a=1, b=0, Class=1)]
    self.assertTrue(checkSameClassification(examplesTrue), )

  def test_checkSameClassificationF(self):
    examplesFalse = [dict(a=1, b=1, Class=1), dict(a=1, b=0, Class=0)]
    self.assertFalse(checkSameClassification(examplesFalse),)

  def test_MODE(self):
    examples = [dict(a=1, b=1, Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=0)]
    self.assertEqual(MODE(examples), 1)

  def test_separateExamples(self):
    examples = [dict(a=1, b=1, Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=0),]
    separatedExamples = {1:[dict(a=1, b=1, Class=1)], 0:[dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=0)],}
    self.assertEqual(separateExamples(examples, 'b'), separatedExamples)

  def test_separateExamplesWithUndefined(self):
    examples = [dict(a=1, b='?', Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=0),]
    separatedExamples = { 0:[dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=0)], '?':[dict(a=1, b='?', Class=1)]}
    self.assertEqual(separateExamples(examples, 'b'), separatedExamples)

  def test_calEntropy(self):
    counts = [5, 10]
    entropy = 0.9182958
    self.assertEqual(round(calEntropy(counts), 7), entropy)

  def test_calEntropyWithZero(self):
    counts = [0, 10]    
    entropy = 0
    self.assertEqual(round(calEntropy(counts), 7), entropy)

  def test_entropyOfABranch(self):
    print('entropy of a branch')
    examples = [dict(a=1, b='?', Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=0),]
    entropy = 0.9182958
    self.assertEqual(round(entropyOfABranch(examples), 7), entropy)

  def test_chooseAttribute(self):
    examples = [dict(a=1, b='?', Class=1), dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=0),]
    self.assertEqual(chooseAttribute(examples), 'b')

  def test_chooseAttribute(self):
    examples = [dict(a=1, b='?', Class=1), dict(a=1, b=0, Class=1), dict(a=0, b=0, Class=0),]
    self.assertEqual(chooseAttribute(examples), 'a')

  def test_ID3(self):
    examples = [dict(a=1, b='?', Class=1), dict(a=1, b=0, Class=1), dict(a=0, b=0, Class=0),]
    nodeClass1 = Node(1)
    nodeClass0 = Node(0)
    node = Node()
    node.name = 'a'
    node.children = {1:nodeClass1, 0:nodeClass0}
    self.assertEqual(ID3(examples, 1), node)

  def test_ID3_2(self):
  data = [dict(a=1, b=0, Class=2), dict(a=1, b=1, Class=1),
          dict(a=2, b=0, Class=2), dict(a=2, b=1, Class=3),
          dict(a=3, b=0, Class=1), dict(a=3, b=1, Class=3)]



  def aTree(self):
    

  def smallTree(self):
    nodeZero = Node(0)
    node = Node()
    node.name = 'a'
    nodeChild = Node()
    nodeChild.name = 'b'
    nodeChild.children[0] = nodeZero
    nodeZero.parent = nodeChild
    nodeZero.pathFromParent = 0
    node.children[1] = nodeChild
    node.children[0] = Node(0)
    nodeChild.parent = node
    nodeChild.pathFromParent = 1
    return node, nodeZero

  def test_traceBack(self):
    (root, leaf) = self.smallTree()
    nodePath = [0, 1]
    self.assertEqual(traceBack(leaf), nodePath)

  def test_filterExampleFromPath(self):
    (root, leaf) = self.smallTree()
    examples = [dict(a=0, b='?', Class=1), dict(a=1, b=0, Class=1), dict(a=0, b=0, Class=0),]
    nodePath = [0, 1]
    exampleAfterFiltered = [dict(a=1, b=0, Class=1),]
    self.assertEqual(filterExampleFromPath(root, nodePath, examples), exampleAfterFiltered)

  def test_prune(self):
    (root, leaf) = self.smallTree()
    examples = [dict(a=1, b=0, Class=1), dict(a=1, b=0, Class=1), dict(a=0, b=1, Class=0),]
    expectedNode = Node()
    expectedNode.name = 'a'
    expectedNode.isVisited = 1
    expectedNode.children[1] = Node(1)
    expectedNode.children[0] = Node(0)
    pruned = prune(root, examples)
    self.assertEqual(pruned, expectedNode)

  def test_evaluate(self):
    example = dict( a=1, b=0, Class=1)
    (root, leaf) = self.smallTree()
    self.assertEqual(evaluate(root, example), 0)



if __name__ == '__main__':
  unittest.main()