import urllib2
import json
import pickle
import pprint
from publication import APub
from conference import AConf

URL_SEARCH_PUB_BY_AID = "http://arnetminer.org/services/publication/byperson/%s?u=oyster"
URL_SEARCH_AID_BY_ANAME = "http://arnetminer.org/services/person/%s?u=oyster"
URL_SEARCH_CONF_BY_TOPIC = "http://arnetminer.org/services/search-conference?u=oyster&q=%s"
URL_SEARCH_CONF_BY_NAME = "http://arnetminer.org/services/jconf/%s?u=oyster"
URL_SEARCH_CONF_BY_ID = "http://arnetminer.org/services/jconf/%s?u=oyster"



pp = pprint.PrettyPrinter(indent=4)

#cmap_name_aid = dict()
#cmap_aid_pubs = dict()
#cmap_topic_confs_num = dict()
#cmap_topic_confs = dict()
#cmap_cname_conf = dict()
#cmap_cid_conf = dict()
 

NAME_ID = 'aname_aid.cache'
AID_PUBS = 'aid_pubs.cache'
TOPIC_CONFS_NUM = 'topic_confs_num.cache'
TOPIC_CONFS = 'topic_confs.cache'
CNAME_CONF = 'cname_conf.cache'
CID_CONF = 'cid_conf.cache'



class AClient:
  """arnetminer client
  """
  cmap_name_aid = dict()
  cmap_aid_pubs = dict()
  cmap_topic_confs_num = dict()
  cmap_topic_confs = dict()
  cmap_cname_conf = dict()
  cmap_cid_conf = dict()
 
  loaded = False

  def __init__(self):
    if not AClient.loaded : 
      self.load_cache()
      AClient.loaded = True


  def __load_single(self, fname):
    try : 
      fin = open(fname, 'r')
      cache = pickle.load(fin)
      print "[ load cache ] load %s ok ==>  %d" %(fname, len(cache))
      fin.close()
      return cache
    except Exception as e :
      print e
      return {}


  def load_cache(self):
    AClient.cmap_name_aid = self.__load_single(NAME_ID)
    AClient.cmap_aid_pubs = self.__load_single(AID_PUBS)
    AClient.cmap_topic_confs_num = self.__load_single(TOPIC_CONFS_NUM)
    AClient.cmap_topic_confs = self.__load_single(TOPIC_CONFS)
    AClient.cmap_cname_conf = self.__load_single(CNAME_CONF)
    AClient.cmap_cid_conf = self.__load_single(CID_CONF)


  def __dump_single(self, fname, cache):
    fout = open(fname, 'w')
    pickle.dump(cache, fout)
    print "[ dump cache ] dump %s ok ==>  %d" %(fname, len(cache))
    fout.close()

  def dump_cache(self):
    self.__dump_single(NAME_ID, AClient.cmap_name_aid)
    self.__dump_single(AID_PUBS, AClient.cmap_aid_pubs)
    self.__dump_single(TOPIC_CONFS_NUM, AClient.cmap_topic_confs_num)
    self.__dump_single(TOPIC_CONFS, AClient.cmap_topic_confs)
    self.__dump_single(CNAME_CONF, AClient.cmap_cname_conf)
    self.__dump_single(CID_CONF, AClient.cmap_cid_conf)

  
  def get_aid_by_name(self, aname):
    if aname in AClient.cmap_name_aid :
      return AClient.cmap_name_aid[aname]
    else :
      resp = urllib2.urlopen((URL_SEARCH_AID_BY_ANAME % aname).
                             replace(" ", "%20")).read()
      data = json.loads(resp)
      AClient.cmap_name_aid[aname] = data[0]['Id']
      return data[0]['Id']

  
  def get_pubs_by_aid(self, aid):
    """
    Returns : A list, each member is an APub object
    """
    if aid in AClient.cmap_aid_pubs : 
      return AClient.cmap_aid_pubs[aid]
    else :
      resp = urllib2.urlopen((URL_SEARCH_PUB_BY_AID % aid).
                             replace(" ","%20")).read()
      data = json.loads(resp)
      ret = []
      for d in data : 
        try : 
          tconf = self.get_conf_by_name(d['Jconfname'])
          apub = APub(d['Id'], d['Title'], tconf.cid, d['Citedby'])
          ret.append(apub)
        except Exception as e : 
          print e
          #pp.pprint(d)
  
      AClient.cmap_aid_pubs[aid] = ret
      return ret


  def get_confs_num_by_topic(self, topic):
    if topic in AClient.cmap_topic_confs_num : 
      return AClient.cmap_topic_confs_num[topic]
    else : 
      resp = urllib2.urlopen((URL_SEARCH_CONF_BY_TOPIC % topic).
                             replace(" ","%20")).read()
      data = json.loads(resp)
      AClient.cmap_topic_confs_num[topic] = data['TotalResultCount']
      return data['TotalResultCount']


  def get_confs_by_topic(self, topic, num):
    """
    Returns : A list, each member is AConf
    """
    key = topic + '|' + str(num)
    if key  in AClient.cmap_topic_confs : 
      return AClient.cmap_topic_confs[key]
    else :
      resp = urllib2.urlopen((URL_SEARCH_CONF_BY_TOPIC % topic).
                             replace(" ","%20") + '&num=' + str(num)).read()
      data = json.loads(resp)
      ret = []
      for d in data['Results']:
        ret.append(self.get_conf_by_cid(d['Id']))
  
      AClient.cmap_topic_confs[key] = ret
      return ret


  def get_conf_by_name(self, name):
    if name in AClient.cmap_cname_conf : 
      return AClient.cmap_cname_conf[name]
    else :
      resp = urllib2.urlopen((URL_SEARCH_CONF_BY_NAME % name).
                             replace(" ","%20")).read()
      data = json.loads(resp)[0]
      rconf = AConf(data['Id'], data['Name'], data['Score'])

      AClient.cmap_cname_conf[name] = rconf
      return rconf


  def get_conf_by_cid(self, cid):
    if cid in AClient.cmap_cid_conf : 
      #print "=============== hit =========="
      return AClient.cmap_cid_conf[cid]
    else : 
      resp = urllib2.urlopen((URL_SEARCH_CONF_BY_ID % cid).
                             replace(" ","%20")).read()
      data = json.loads(resp)[0]
      rconf = AConf(data['Id'], data['Name'], data['Score'])

      AClient.cmap_cid_conf[cid] = rconf
      return rconf


ZC = AClient()


if __name__ == '__main__' :
  
#aid = c.get_aid_by_name('Jie Tang')
#print(aid)
#apub_list = c.get_pubs_by_aid(aid)
#print(len(apub_list))

  confs_num = ZC.get_confs_num_by_topic('Distributed System')
  print confs_num
  if (confs_num > 20) :
    confs_num = 20
  confs = ZC.get_confs_by_topic('Distributed System', confs_num)
  pp.pprint(confs)

  ZC.dump_cache()

