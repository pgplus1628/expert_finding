import json


class AConf :
  cid = 0
  cname = ""
  score = 0.0
  
  def __init__(self, cid, cname, score):
    self.cid = cid
    self.cname = cname
    self.score = score

  def __str__(self):
    return "<AConf cid : %s, cname : %s, score = %s>" % (self.cid, self.cname, self.score)

  def __repr__(self):
    return "<AConf cid : %s, cname : %s, score = %s>" % (self.cid, self.cname, self.score)

