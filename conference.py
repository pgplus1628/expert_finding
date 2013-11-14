import json


class AConf :
  cid = 0
  cname = ""
  
  def __init__(self, cid, cname):
    self.cid = cid
    self.cname = cname


  def get_cid(self):
    return self.cid

  def get_cname(self):
    return self.cname

  def __str__(self):
    return "<AConf cid : %s, cname : %s>" % (self.cid, self.cname)

  def __repr__(self):
    return "<AConf cid : %s, cname : %s>" % (self.cid, self.cname)

