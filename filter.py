


def filter_data(fname):
  fin = open(fname, 'r')
  fout = open(fname + '.pure', 'w')
  amap = {}
  for line in fin :
    attr = line.split(None, 2)
    if int(attr[1]) in amap : 
      pass
      #print attr
    else :
      amap[int(attr[1])] = attr
      fout.write(line)

  fout.close()
  fin.close()
  return amap

if __name__ == '__main__' :
  fname = './data/data mining.txt'
  filter_data(fname)

