from node import Node
import math

def ID3(examples, default, attributesChosen = []):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  if not examples:
    return Node(default)
  elif checkSameClassification(examples) or not chooseAttribute(examples):
    return Node(MODE(examples))
  else:
    bestAttribute = chooseAttribute(examples)
    attributesChosen.append(bestAttribute)
    myTree = Node()
    myTree.name = bestAttribute
    dictOfExamples = separateExamples(examples, bestAttribute)
    for key, exampleList in dictOfExamples.items():
        subtree = ID3(exampleList, MODE(examples), attributesChosen)
        myTree.children[key] = subtree
    return myTree

def checkSameClassification(examples):
  '''
  Takes in an array of examples and checks whether all of them have the same classification.
  Returns boolean True/False
  '''
  myClass = examples[0]['Class']
  for example in examples:
    if example['Class'] != myClass:
      return False
  return True

def MODE(examples):
  '''
  Takes in an array of examples and find the MODE of their classification.
  Returns string
  '''
  classCountList = {}
  for example in examples:
    if example['Class'] not in classCountList.keys():
      classCountList[example['Class']] = 0
    classCountList[example['Class']] += 1
  modeCount = 0
  modeValue = None
  for classValue, classCount in classCountList.items():
    if classCount > modeCount:
      modeCount = classCount                  
      modeValue = classValue
  return modeValue


def separateExamples(examples, attribute):
  '''
  Takes in an array of examples and an attribute to separate these examples.
  The examples are split based on the value of attribute chosen.
  Returns a dictionary with key:value pair of attribute value: list of examples with the given attribute value.
  '''  
  setOfOutcome = set()
  seperatedExamples = {}
  for example in examples:
    if example[attribute] not in seperatedExamples.keys():
      seperatedExamples[example[attribute]] = []
    seperatedExamples[example[attribute]].append(example)
  return seperatedExamples


def entropyOfABranch(examples):
  '''
  Takes in an array of examples and find the entropy of these examples based on their classification.
  Returns a floating number
  '''  
  if not examples:
    return 0
  countOfClasses = {}
  for example in examples:
    if example['Class'] not in countOfClasses.keys():
      countOfClasses[example['Class']] = 0
    countOfClasses[example['Class']] += 1
  return calEntropy(list(countOfClasses.values()))


def calEntropy(listOfCounts):
  '''
  Takes in a list that contains the number of each classification.
  Calculates the entropy and returns it
  Returns a floating number.
  '''  
  totalCount = 0
  entropy = 0
  for count in listOfCounts:
    totalCount += count
  for count in listOfCounts:
    p = count / totalCount
    entropyP = - p * math.log(p,2) if p else 0
    entropy += entropyP
  return entropy


def chooseAttribute(examples, attributesChosen = []):
  '''
  Takes in an array of examples and find the best attribute to split them based on information gain.
  Returns string
  '''  
  bestEntropy = None
  bestAttribute = None
  for attribute in examples[0].keys():
    if attribute == 'Class':
      continue
    if attribute in attributesChosen:
      continue
    dictOfExamples = separateExamples(examples, attribute)
    if len(dictOfExamples) <= 1:
      continue
    entropy = 0
    for value in dictOfExamples.values():
      p = len(value) / len(examples)
      entropy += entropyOfABranch(value)

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
      if childNode.label is None:
        childNode.parent = currentNode
        childNode.pathFromParent = key
        if not currentNode.isVisited:
          nodestack.append(childNode)
        isLeaf = 0
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
            if not examplesLeftAtNode:
              currentNode.isVisited = 1
              continue
            parentNode.children[key] = Node(MODE(examplesLeftAtNode))
        prunedAccuracy = test(node, examples)
      else:
        prunedAccuracy = test(Node(MODE(examples)), examples)
      if currentAccuracy <= prunedAccuracy:
        if not parentNode:
          return Node(MODE(examples))
        continue
      if parentNode:
        parentNode.children[currentNode.pathFromParent] = currentNode
    elif currentNode.isVisited:
      nodestack.pop()
    currentNode.isVisited = 1          
  return node
    

def traceBack(node, nodePath = []):
  '''
  Takes in a leaf of a tree and find the path to reach the root.
  Each vertice of the path is labelled by the attribute value
  Returns a list containing the path from leaf to root
  '''  
  if node.parent is None:
    return nodePath
  nodePath.append(node.pathFromParent)
  return traceBack(node.parent, nodePath)

def filterExampleFromPath(node, nodePath, examples):
  '''
  Takes in a tree, the path to a leaf, and a set of examples
  Run the examples through the path to determine which examples are left in the leaf of the tree
  Returns the truncated list of examples
  '''
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
  Takes in a tree and one example.  Returns the Classification that the tree
  assigns based on the attributes of the example.
  '''
  if node.label is not None:
    return node.label
  else:
    result = example[node.name]
    if result not in node.children.keys():
      return None
    subtree = node.children[result]
    return evaluate(subtree, example)
