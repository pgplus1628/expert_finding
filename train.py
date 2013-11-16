import svmlight
from aclient import AClient
from aclient import ZC
from publication import APub
from conference import AConf
from feature import Feature
from filter import filter_data

def reform_vector(fv):
  size = len(fv)
  ret = []
  for i in xrange(size) :
    ret.append( (i + 1, fv[i]) )
  return ret
    

def init_data(fname, topic):
  print ('[ init_data ] =================')
  QID = 1
  # amap , key : aid 
  # value : attr[0] preferance, attr[1] aid , attr[2] aname
  amap = filter_data(fname)
  fea = Feature(topic)
  train_rank = []
  for tid in amap : 
    aid = int(tid)
    fv = fea.get_feature_vector(aid)
    print ('[ init_data ] %d get feature vector ok.' %(aid))
    train_rank.append( (int(amap[tid][0]), reform_vector(fv), QID) )
    #ZC.dump_cache()

  return train_rank


def train(training_data):
  print ('[ train ] ===================')

  # train a model based on the data
  model = svmlight.learn(training_data, type='ranking', verbosity=0)
  
  # model data can be stored in the same format SVM-Light uses, for interoperability
  # with the binaries.
  svmlight.write_model(model, 'ef_model.dat')
  


def test(test_data, fmodel_name):

  print ('[ test ] ===================')
  model = svmlight.read_model(fmodel_name)

  # classify the test data. this function returns a list of numbers, which represent
  # the classifications.
  predictions = svmlight.classify(model, test_data)
  for p in predictions:
      print '%.8f' % p



  

if __name__ == '__main__' : 
  fname = './data/data mining.txt'
  topic = 'data mining'
  fmodel_name = 'ef_model.dat'
  train_rank = init_data(fname, topic)
  test_rank = train_rank

  #train(train_rank)
  test(test_rank, fmodel_name)



