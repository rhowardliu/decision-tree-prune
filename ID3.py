from node import Node
import math

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  if not examples:
    return Node(default)
  elif checkSameClassification(examples) or not chooseAttribute(examples):
    print('same classification/ all trivial!')
    return Node(MODE(examples))
  else:
    bestAttribute = chooseAttribute(examples)
    print('best attribute is ', bestAttribute)
    myTree = Node()
    myTree.name = bestAttribute
    seperatedLists = separateExamples(examples, bestAttribute)
    for exampleList in seperatedLists:
      if exampleList:
        value = exampleList[0][bestAttribute]
        subtree = ID3(exampleList, MODE(examples))
        myTree.children[value] = subtree
    return myTree

def checkSameClassification(examples):
  myClass = examples[0]['Class']
  for example in examples:
    if example['Class'] != myClass:
      return False
  return True

def MODE(examples):
  classCountList = {}
  for example in examples:
    exampleClassValue = example['Class']
    if exampleClassValue not in classCountList.keys():
      classCountList[exampleClassValue] = 1
    else:
      classCountList[exampleClassValue] += 1
  modeCount = 0
  modeValue = None
  for classValue, classCount in classCountList.items():
    if classCount > modeCount:
      modeCount = classCount
      modeValue = classValue
  return modeValue


def separateExamples(examples, attribute):
  trueList = []
  falseList = []
  undefinedList = []
  for example in examples:
    if example[attribute] == '?':
      undefinedList.append(example)
    elif example[attribute]:
      trueList.append(example)
    else:
      falseList.append(example)
  return [trueList, falseList, undefinedList]

def entropyOfABranch(examples):
  if not examples:
    return 0
  countA = 0
  countB = 0
  exampleClass = examples[0]['Class']
  for example in examples:
    if example['Class'] == exampleClass:
      countA += 1
    else:
      countB += 1
  return calEntropy(countA, countB)


def calEntropy(countA, countB):
  p = countA / (countA + countB)
  q = countB / (countA + countB) 
  entropyP = - p * math.log(p,2) if p else 0
  entropyQ = - q * math.log(q,2) if q else 0
  return entropyP + entropyQ



def chooseAttribute(examples):
  bestEntropy = None
  bestAttribute = None
  for attribute in examples[0].keys():
    if attribute == 'Class':
      continue
    [trueList, falseList, undefinedList] = separateExamples(examples, attribute)

    p = len(trueList) / len(examples)
    q = len(falseList) / len(examples)
    r = len(undefinedList) / len(examples)

    entropy = p * entropyOfABranch(trueList) + q * entropyOfABranch(falseList) + r * entropyOfABranch(undefinedList)
    print('entropy of splitting ', attribute, ' is ', entropy)
    if ( bestEntropy is None ) or (entropy < bestEntropy):
      bestEntropy = entropy
      bestAttribute = attribute
  return bestAttribute

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  nodestack = []
  nodestack.append(node)
  while nodestack:
    currentNode = nodestack[-1]
    isLeaf = 1
    for key, childNode in currentNode.children.items():
      print('accessing node ', currentNode.name)
      if childNode.label is None:
        childNode.parent = currentNode
        childNode.pathFromParent = key
        nodestack.append(childNode)
        isLeaf = 0
        print('oops not a leaf')
    if isLeaf:
      nodestack.pop()
      currentAccuracy = test(node, examples)
      parentNode = None
      if currentNode.parent:
        parentNode = currentNode.parent
        for key, value in parentNode.children.items():
          if value is currentNode:
            pathToCurrentNode = traceBack(currentNode)
            examplesLeftAtNode = filterExampleFromPath(node, pathToCurrentNode, list(examples))
            parentNode.children[key] = Node(MODE(examplesLeftAtNode))
        prunedAccuracy = test(node, examples)
      else:
        prunedAccuracy = test(Node(MODE(examples)), examples)
      if currentAccuracy <= prunedAccuracy:
        if not parentNode:
          return Node(MODE(examples))
        print('pruned', currentNode.name)
        continue
      if parentNode:
        parentNode.children[currentNode.pathFromParent] = currentNode
      print('keeping', currentNode.name)
  return node
    

def traceBack(node, nodePath = []):
  if node.parent is None:
    return nodePath
  nodePath.append(node.pathFromParent)
  return traceBack(node.parent, nodePath)

def filterExampleFromPath(node, nodePath, examples):
    if not nodePath:
      return examples
    toGo = nodePath.pop()
    for example in examples:
      if example[node.name] != toGo:
        examples.remove(example)
    return filterExampleFromPath(node.children[toGo], nodePath, examples)


def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  correctCount = 0
  for example in examples:
    if example['Class'] == evaluate(node, example):
      correctCount += 1
  return correctCount/len(examples)


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if node.label is not None:
    return node.label
  else:
    result = example[node.name]
    subtree = node.children[result]
    return evaluate(subtree, example)
