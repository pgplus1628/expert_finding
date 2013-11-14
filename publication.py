import json


class APub : 
  """ arnetminer publication """
  pid = -1
  tit = ''
  cid = -1
  cit = 0

  def __init__(self, pid, tit, cid, cit):
    self.pid = pid
    self.tit = tit
    self.cid = cid
    self.cit = cit

  def __str__(self):
    return "<APub pid : %s, tit = %s, cid = %s, cit = %s>" %(self.pid, 
                                                              self.tit,
                                                              self.cid,
                                                              self.cit)

  def __repr__(self):
    return "<APub pid : %s, tit = %s, cid = %s, cit = %s>" %(self.pid, 
                                                              self.tit,
                                                              self.cid,
                                                              self.cit)


