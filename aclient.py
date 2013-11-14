import urllib2
import json
import pprint
from publication import APub
from conference import AConf

URL_SEARCH_PUB_BY_AID = "http://arnetminer.org/services/publication/byperson/%s?u=zorksylar"
URL_SEARCH_AID_BY_ANAME = "http://arnetminer.org/services/person/%s?u=zorksylar"
URL_SEARCH_CONF_BY_TOPIC = "http://arnetminer.org/services/search-conference?u=zorksylar&q=%s"
URL_SEARCH_CONF_BY_NAME = "http://arnetminer.org/services/jconf/%s?u=zorksylar"
URL_SEARCH_CONF_BY_ID = "http://arnetminer.org/services/jconf/%s?u=zorksylar"



pp = pprint.PrettyPrinter(indent=4)



class AClient:
  """arnetminer client
  """
  def __init__(self):
    pass 
  
  def get_aid_by_name(self, aname):
    resp = urllib2.urlopen((URL_SEARCH_AID_BY_ANAME % aname).
                           replace(" ", "%20")).read()
    data = json.loads(resp)
    return data[0]['Id']

  
  def get_pubs_by_aid(self, aid):
    """
    Returns : A list, each member is an APub object
    """
    resp = urllib2.urlopen((URL_SEARCH_PUB_BY_AID % aid).
                           replace(" ","%20")).read()
    data = json.loads(resp)
    ret = []
    for d in data : 
      apub = APub(d['Id'], d['Title'], d['Jconfname'], d['Citedby'])
      ret.append(apub)
    return ret


  def get_confs_num_by_topic(self, topic):
    resp = urllib2.urlopen((URL_SEARCH_CONF_BY_TOPIC % topic).
                           replace(" ","%20")).read()
    data = json.loads(resp)
    return data['TotalResultCount']


  def get_confs_by_topic(self, topic, num):
    resp = urllib2.urlopen((URL_SEARCH_CONF_BY_TOPIC % topic).
                           replace(" ","%20") + '&num=' + str(num)).read()
    data = json.loads(resp)
    ret = []
    for d in data['Results']:
      ret.append(self.get_conf_by_cid(d['Id']))
    return ret


  def get_conf_by_name(self, name):
    resp = urllib2.urlopen((URL_SEARCH_CONF_BY_NAME % name).
                           replace(" ","%20")).read()
    data = json.loads(resp)[0]
    return AConf(data['Id'], data['Name'], data['Score'])


  def get_conf_by_cid(self, cid):
    resp = urllib2.urlopen((URL_SEARCH_CONF_BY_ID % cid).
                           replace(" ","%20")).read()
    data = json.loads(resp)[0]
    return AConf(data['Id'], data['Name'], data['Score'])
    



if __name__ == '__main__' :
  c = AClient()
  
#aid = c.get_aid_by_name('Jie Tang')
#print(aid)
#apub_list = c.get_pubs_by_aid(aid)
#print(len(apub_list))

  confs_num = c.get_confs_num_by_topic('Distributed System')
  print confs_num
  if (confs_num > 20) :
    confs_num = 20
  confs = c.get_confs_by_topic('Distributed System', confs_num)
  pp.pprint(confs)




