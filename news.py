from eventregistry import *
import secrets

def get_trending_uris(er, amount=10):
  retInfo = ReturnInfo(conceptInfo = ConceptInfoFlags(trendingHistory = True))
  q = GetTrendingConcepts(source="news", count=amount, returnInfo=retInfo)
  res = er.execQuery(q)
  
  labels = []
  for d in res:
    labels.append(d['uri'])
  
  return labels

def get_news_by_uri(er, uri, page=1, lang="eng"):
  q = QueryArticles(lang=[lang],  isDuplicateFilter = "skipDuplicates")
  q.addConcept(uri)
  q.addRequestedResult(RequestArticlesInfo(page=page, count=200, sortBy="date"))   
  res = er.execQuery(q)

  titles = []
  if 'error' not in res:
    for d in res["articles"]["results"]:
      titles.append(d["title"].encode('utf8'))
    
  return titles

def get_news(er, uri_count=5, pages=1, lang="eng"):
  uris = get_trending_uris(er, uri_count)

  titles = []
  for uri in uris:
    for p in xrange(1,pages+1):
      titles += get_news_by_uri(er, uri, p, lang)
      
  return list(set(titles))  # Remove duplicates

def update(newsfile, uri_count=20, pages=2):
  er = EventRegistry()
  
  if secrets.event_registry_use_login:
    try:
      er.login(secrets.event_registry_email, secrets.event_registry_password)
    except:
      print "Login failed, access will be restricted to 50 EventRegistry queries per day"
    
  news = get_news(er, uri_count, pages)
  with open(newsfile, "wb") as output:
    output.write("\n".join(news))

