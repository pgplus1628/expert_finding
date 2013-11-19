from aclient import AClient
from publication import APub
from conference import AConf
from aclient import ZC

import math


CONFS_SIZE = 200
RANK_SIZE = 5

class Feature:
  
  prank = [0.0] * RANK_SIZE
  crank = [0.0] * RANK_SIZE

  topic = ''
  aname = ''
  
  conf_map = {}
  
  def __init__(self, topic):
    self.topic = topic
    self.__get_related_confs()


  def __get_related_confs(self):
    confs_size = ZC.get_confs_num_by_topic(self.topic)
    if confs_size > CONFS_SIZE :
      confs_size = CONFS_SIZE
    confs = ZC.get_confs_by_topic(self.topic, confs_size)

    for tc in confs:
      self.conf_map[tc.cid] = tc


  def __pull_feature(self, aid):
    # I. Get all pubs
    pubs = ZC.get_pubs_by_aid(aid)
    
    # II. Diff pubs and confs, get valid pubs
    valid_pubs = []
    for tp in pubs : 
      if tp.cid in self.conf_map :
        valid_pubs.append((tp, self.conf_map[tp.cid].score))
  
    # III. sort valid pubs ,and cal the feature
    valid_pubs.sort(key = lambda tup : tup[1])

    for it in valid_pubs : 
      v = int(math.floor(it[1] / 0.5))
      if (v < RANK_SIZE) : 
        self.prank[v] += 1.0
        self.crank[v] += it[0].cit
      else : 
        self.prank[RANK_SIZE-1] += 1.0
        self.crank[v] += it[0].cit


  def get_feature_vector(self, aid) :
    self.prank = [0.0] * RANK_SIZE
    self.crank = [0.0] * RANK_SIZE
    self.__pull_feature(aid)
    return self.prank + self.crank



if __name__ == '__main__' :
  aname = 'Jie Tang'
  topic = 'Data Mining'

  aid = ZC.get_aid_by_name(aname)
  print aid
  fea = Feature(topic)
  flist = fea.get_feature_vector(aid)
  print flist

  ZC.dump_cache()
  
