import json


class APub : 
  """ arnetminer publication """
  pid = -1
  tit = ''
  conf = ''
  cit = 0

  def __init__(self, pid, tit, conf, cit):
    self.pid = pid
    self.tit = tit
    self.conf = conf
    self.cit = cit

  def get_pid(self):
    return self.pid

  def get_tit(self):
    return self.tit
  
  def get_conf(self):
    return self.conf

  def get_cit(self):
    return self.cit

  def __str__(self):
    return "<APub pid : %s, tit = %s, conf = %s, cit = %s>" %(self.pid, 
                                                              self.tit,
                                                              self.conf,
                                                              self.cit)

  def __repr__(self):
    return "<APub pid : %s, tit = %s, conf = %s, cit = %s>" %(self.pid, 
                                                              self.tit,
                                                              self.conf
                                                              self.cit)


