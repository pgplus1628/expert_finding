import svmlight
from aclient import AClient
from aclient import ZC
from publication import APub
from conference import AConf
from feature import Feature
from filter import filter_data
import pprint

TRAINING_DATA = 'training_data.dat'
RERANK_RESULT = 'rerank_result.dat'
FMODEL_NAME = 'ef_model.dat'


def reform_vector(fv):
  size = len(fv)
  ret = []
  for i in xrange(size) :
    ret.append( (i + 1, fv[i]) )
  return ret
    

def init_train_data(fname, topic):
  print ('[ init_train_data ] =================')
  QID = 1
  # amap , key : aid 
  # value : attr[0] preferance, attr[1] aid , attr[2] aname
  amap = filter_data(fname)
  fea = Feature(topic)
  train_rank = []
  for tid in amap : 
    aid = int(tid)
    fv = fea.get_feature_vector(aid)
    print ('[ init_train_data ] %d get feature vector ok.' %(aid))
    train_rank.append( (int(amap[tid][0]), reform_vector(fv), QID) )
    #ZC.dump_cache()

  return train_rank

def init_test_data(fname, topic):
  print ('[ init_train_data ] =================')
  QID = 1
  # amap , key : aid 
  # value : attr[0] preferance, attr[1] aid , attr[2] aname
  amap = filter_data(fname)
  fea = Feature(topic)
  train_rank = []
  for tid in amap : 
    aid = int(tid)
    fv = fea.get_feature_vector(aid)
    print ('[ init_train_data ] %d get feature vector ok.' %(aid))
    train_rank.append( (aid, reform_vector(fv), QID) )
    #ZC.dump_cache()

  return train_rank


def init_rerank_data(aids , topic):
  QID = 1
  fea = Feature(topic)
  rerank_data = []
  for tid in aids : 
    fv = fea.get_feature_vector(tid)
    print ('[ init_rerank_data ] %d get feature vector ok.' %(tid))
    rerank_data.append( (tid, reform_vector(fv), QID) ) 

  return rerank_data


def train(training_data):
  print ('[ train ] ===================')

  with open(TRAINING_DATA, 'w') as f :
    pprint.pprint(training_data, f)
  # train a model based on the data
  model = svmlight.learn(training_data, type='ranking', kernel = 'linear',  verbosity=0)
  
  # model data can be stored in the same format SVM-Light uses, for interoperability
  # with the binaries.
  svmlight.write_model(model, 'ef_model.dat')
  ZC.dump_cache()
  


def test(test_data, fmodel_name):

  print ('[ test ] ===================')
  model = svmlight.read_model(fmodel_name)

  # classify the test data. this function returns a list of numbers, which represent
  # the classifications.
  predictions = svmlight.classify(model, test_data)
  for p in predictions:
      print '%.8f' % p


def zrank(aids, topic, fmodel_name):

  rerank_data = init_rerank_data(aids, topic)

  print ('[ zrank ] ===================')
  model = svmlight.read_model(fmodel_name)

  predictions = svmlight.classify(model, rerank_data)

  aid_score = zip( [x[0] for x in rerank_data ], predictions)
  aid_score.sort(key = lambda tup : tup[1], reverse=True)
  
  with open(RERANK_RESULT + '_' + topic, 'w') as f :
    pprint.pprint(aid_score, f)

  ZC.dump_cache()


  return [x[0] for x in aid_score]


if __name__ == '__main__' : 
  fname = './data/data mining.txt'
  topic = 'data mining'
  fmodel_name = 'ef_model.dat'
  train_rank = init_train_data(fname, topic)
  test_rank = init_test_data(fname, topic)

  train(train_rank)
  #test(test_rank, fmodel_name)
  zrank(test_rank, fmodel_name)


