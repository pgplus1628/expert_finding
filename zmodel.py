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
EXT_TRAIN_A_SIZE = 100


def reform_vector(fv):
  size = len(fv)
  ret = []
  for i in xrange(size) :
    ret.append( (i + 1, fv[i]) )
  return ret
    

def init_train_data(fnames, topics):
  print ('[ init_train_data ] =================')
  # amap  
  # key : aid 
  # value : attr[0] preferance, attr[1] aid , attr[2] aname

  train_rank = []
  for QID in range(len(topics)):
    fname = fnames[QID]
    topic = topics[QID]

    amap = filter_data(fname)
    fea = Feature(topic)

    ext_aids = ZC.get_raw_rank(topic, EXT_TRAIN_A_SIZE)
    print '[ init_train_data ] amap_1 size = %d ' %(len(amap))

    for tid in ext_aids : 
      if not (tid in amap)  : 
        amap[tid] = (0, tid, '')

    print '[ init_train_data ] amap_2 size = %d ' %(len(amap))
    
    for tid in amap : 
      fv = fea.get_feature_vector(tid)
      #print ('[ init_train_data ] %d get feature vector ok.' %(tid))
      train_rank.append( (int(amap[tid][0]), reform_vector(fv), QID) )

    print '[ init_train_data ]  topic : %s ok , train_rank_size = %d' %(topic, len(train_rank))
    ZC.dump_cache()

  with open('train_rank.dat' , 'w') as f :
    pprint.pprint(train_rank, f)

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


def train(fnames, topics):

  training_data = init_train_data(fnames, topics)
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
  fname_dir = './data/'
#  fname_names = ['data mining.txt', 'high performance computing.txt', 'multimedia.txt', 'human computer interaction.txt']
#  topics = ['data mining', 'high performance computing', 'multimedia', 'human computer interaction']
  fname_names = ['multimedia.txt']
  topics = ['multimedia']
  fnames = [ fname_dir + x for x in fname_names]

  fmodel_name = 'ef_model.dat'

  train(fnames, topics)
  #test(test_rank, fmodel_name)
  #zrank(test_rank, fmodel_name)


