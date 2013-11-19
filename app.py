from flask import Flask, render_template
import urllib2
import json
import zmodel
import pprint

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
	return "hello world"

URL_SEARCH_EXPERT = "http://arnetminer.org/services/search-expert?u=oyster&start=0&num=100&q=%s"
URL_SEARCH_PUBLICATION = "http://arnetminer.org/services/search-publication?u=oyster&start=0&num=100&q=%s"
URL_SEARCH_CONFERENCE = "http://arnetminer.org/services/search-conference?u=oyster&start=0&num=100&q=%s"
URL_SEARCH_PUBLICATION_BY_AUTHOR = "http://arnetminer.org/services/publication/byperson/%s"

@app.route("/search/<query>")
def search(query):
	response = urllib2.urlopen((URL_SEARCH_EXPERT % query).replace(" ","%20")).read()
	data = json.loads(response)
	result = []
	try : 
		for item in data["Results"]:
			result.append(item["Id"])
	except Exception as e: 
		print e
		pprint.pprint(data)

	better_result = rerank(result, query)
	return json.dumps(better_result)	

def rerank(result, topic):
	rerank_data = zmodel.init_rerank_data(result, topic)
	better_result = zmodel.zrank(rerank_data, zmodel.FMODEL_NAME)
	return better_result

@app.route("/network/<query>")
def network(query):
	from collections import defaultdict
	response = urllib2.urlopen((URL_SEARCH_PUBLICATION % query).replace(" ","%20")).read()
	data = json.loads(response)
	# constructing coauthor network
	author_name = {}
	paper_count = defaultdict(int)
	edges = defaultdict(int)
	for item in data["Results"]:
		authors = item["Authors"].split(",")
		author_ids = item["AuthorIds"]
		for i in range(len(author_ids)):
			author_name[author_ids[i]] = authors[i]
			paper_count[author_ids[i]] += 1
			for j in range(i+1, len(author_ids)):
				key = (author_ids[i],author_ids[j])
				if key[0] > key[1]:
					key = (key[1], key[0])
				edges["%s-%s" % key] += 1
	index = 0
	author_index = {}
	result = {"nodes":[], "links":[]}
	for n in author_name:
		result["nodes"].append({"id":n, "name":author_name[n], "count":paper_count[n]})
		author_index[n] = index
		index += 1
	for e in edges:
		x = e.split("-")
		result["links"].append({"source":author_index[int(x[0])], "target":author_index[int(x[1])], "value":edges[e]})
	return json.dumps(result)

@app.route("/coauthor/")
def coauthor():
	return render_template("network.htm")


if __name__ == "__main__":
	#app.run()
  app.run(host='0.0.0.0')
