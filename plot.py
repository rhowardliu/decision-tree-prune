import parse, ID3, random
# inFile - string location of the house data file
def testPruningOnHouseData(data, n):
  withPruning = []
  withoutPruning = []
  for i in range(100):
    random.shuffle(data)
    train = data[:n]
    valid = data[n:n*4//3]
    test = data[n*4//3:]
    tree = ID3.ID3(train, 'democrat')
    acc = ID3.test(tree, test)
  
    tree = ID3.prune(tree, valid)
    acc = ID3.test(tree, test)
    withPruning.append(acc)

    tree = ID3.ID3(train+valid, 'democrat')
    acc = ID3.test(tree, test)
    withoutPruning.append(acc)
  print("For training set of {}".format(n))
  print("average with pruning",sum(withPruning)/len(withPruning)," without: ",sum(withoutPruning)/len(withoutPruning))


if __name__ == '__main__':
  print('hi')
  data = parse.parse('house_votes_84.data')
  for x in range(15, 260, 15):
    testPruningOnHouseData(data, x)