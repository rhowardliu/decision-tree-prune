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

def EntropyOfSplit(trueList, falseList, undefinedList):
  total


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
    if ( not bestEntropy ) or (entropy < bestEntropy):
      bestEntropy = entropy
      bestAttribute = attribute
  return bestAttribute

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  if node.label:
    return node.label
  else:
    result = example[node.name]
    subtree = node.children[result]
    return evaluate(subtree, example)
