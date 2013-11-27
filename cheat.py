import urllib2
import json
import pprint
import re


TOPIC_URL = "http://arnetminer.org/topic-browser"
ZSEARCH_URL = "http://166.111.131.95:5000/search/%s"

"""
<a href="/topic-detail/fuzzy-system-8.html">Fuzzy system</a>
<a href="/topic-detail/                    >            </a>
"""

def get_cheat_topics():
  resp = urllib2.urlopen(TOPIC_URL).read()
  pattern = "\<a href\=\"\/topic\-detail\/[a-zA-Z0-9\-]*\.html\"\>[A-Za-z0-9\-\ \/]*\<\/a\>"
  urls = re.findall(pattern, resp)
  topics = []
  for url in urls : 
    tt = url.split('>')[1].split('<')[0]
    for it in tt.split('/'):
      topics.append(it.strip())

  return topics


def cheat_search_cases():
  topics = get_cheat_topics()
  for it in topics : 
    resp = urllib2.urlopen((ZSEARCH_URL % (it)).replace(" ", "%20")).read()
    print json.loads(resp)
    print '[ cheat ] >>>>>>>>>>>>>>>>>>>>>>>  %s  ok <<<<<<<<<<<<<<<<<<<<<' % it
  


if __name__ == '__main__':
  cheat_search_cases()

