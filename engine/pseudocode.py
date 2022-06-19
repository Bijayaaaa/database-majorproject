# engile pseudocode

# crawl the page
def crawl(pages, depth):
   for i  in range(depth)
      for page in pages:   # pages = url_list
         index page <addindex> if not already indexed
         links = get links of page
         for link in links:
            if not already indexed:
               index link 
               newpages.add(url)
         Add link between two pages ini database: from:page to:url with text:linktext
      pages=newpages

# index the url 
def addtoindex(url, soup):
   if not indexed:
      for word in words of page:
         store to table 'wordlocation' values: url, wordid, location
      store pdf url to seperate database <storepdf>

# store to database: 'pdfs' <if link is pdf>
def storepdf(url):
   if (url is drive link) or (link ends with 'pdf' or 'pdf/' or any other document format):
      add url id to database: 'pdfs'
   

# get id of word
def getentryid():
   if not stored:
      store to table 'urllist' values: 'word' -> word
   else:
      get id of stored word

# links between pages
def addlinkref(fromurl, tourl, linktext):
   words = separatewords(linkText)
   fromid = getentryid('urllist','url',urlFrom)
   toid = getentryid('urllist','url',urlTo)
   if fromid==toid: return # i.e. fromurl_id == tourl_id
   insert to table: 'link(fromid,toid)' values: fromid,toid
   
   
   for word in words:
      if word not in ignorewords:
         insert to table 'linkwords(linkid,wordid)' values: linkid, wordid
         ;where linkid=cur.lastrowid

# seperator
source: https://www.pythontutorial.net/python-regex/python-regex-split/
def separatewords(self, text):
        # source: https://www.pythontutorial.net/python-regex/python-regex-split/
        
        # splitter = re.compile('\W*')
        # return [s.lower() for s in splitter.split(text) if s != '']
        splitter = r'\W+'
        return [s.lower() for s in re.split(splitter, text) if s != '']
