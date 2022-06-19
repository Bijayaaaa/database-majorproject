
import urllib.request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import re

# from urlparse import urljoin
# from BeautifulSoup import *
# import urllib2
# import urllib.request

# c = urllib.request.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
# c = urllib.request.urlopen(
#     'https://en.wikipedia.org/wiki/Programming_language')
# contents = c.read()

# print(contents[:50])

# Create a list of words to ignore
ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class Crawler:
   # iniitialize the Crawler with the name database
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

   # Auxilary function for getting an entry id and adding
   # if it's not present
    def getentryid(self, table, field, value, createnew=True):
        # table = 'wordlist', field='word', value = word whose id is to be fetchd
        # table = 'urllist', field='url', value = url whose id is to be fetchd
        cur = self.con.execute(
            "select rowid from %s where %s='%s'" % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute(
                "insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    # index an individual page
    def addtoindex(self, url, soup):
        if self.isindexed(url):
            return
        print('Indexing ' + url)

        # Get the individual words
        text = self.gettextonly(soup)
        words = self.separatewords(text)

        # Get the URL id
        urlid = self.getentryid('urllist', 'url', url)

        # Link each word to this url
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords:
                continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) \
                values (%d,%d,%d)" % (urlid, wordid, i))
        self.storepdf(url, urlid)
    
    
    
    # Extract the text from an HTML page (no tags)
    def gettextonly(self, soup):
        # Finding the Words on a Page
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext+'\n'
            return resulttext
        else:
            return v.strip()

    # Seperate the words by any non-whitespace character
    def separatewords(self, text):
        # source: https://www.pythontutorial.net/python-regex/python-regex-split/
        
        # splitter = re.compile('\W*')
        # return [s.lower() for s in splitter.split(text) if s != '']
        splitter = r'\W+'
        return [s.lower() for s in re.split(splitter, text) if s != '']
        

    # Return True if this url is already indexed
    def isindexed(self, url):
        u = self.con.execute(
            "select rowid from urllist where url='%s'" % url).fetchone()
        if u != None:
            # Check if it has actually been crawled
            v = self.con.execute(
                'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v != None:
                return True
        return False

    # Add link between two pages
    def addlinkref(self, urlFrom, urlTo, linkText):
        words=self.separatewords(linkText)
        fromid=self.getentryid('urllist','url',urlFrom)
        toid=self.getentryid('urllist','url',urlTo)
        if fromid==toid: return  # i.e. fromurl_id == tourl_id
        cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid=cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))

    # Starting with a list of pages, do breadth first search
    # to the given depth, indexing pages as we go
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:  # pages = url_list
                try:
                    # c = urllib.request.urlopen(page)
                    c = requests.get(page)
                except:
                    print(f"cound not open {page}")
                    continue
                # soup = BeautifulSoup(c.read())
                soup = BeautifulSoup(c.text)
                self.addtoindex(page, soup)

                links = soup('a')
                for link in links:
                    if('href' in dict(link.attrs)):
                        # if <a> has a link
                        url = urljoin(page, link['href'])
                        if url.find("\'") != -1:    # ignore url with quote
                            continue
                        url = url.split('#')[0]   # remove location portion
                        if url[:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)   # strange links e.g. 
                        self.addlinkref(page, url, linkText)    # # Add link between two pages: 
                self.dbcommit()
            pages = newpages

    # Create the database tables
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create table pdfs(urlid)')

        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.con.execute('create index pdfurl on pdfs(urlid)')  #  creating index of each  pdf_url
        self.dbcommit()
    
    def storepdf(self, url, url_id):
        # store to database: pdfs <if link is pdf>
        print(f'ispdf: {url} {url_id}')
        document_prefixes = ['drive.google.com', ]
        document_suffixes = ['pdf', '/pdf', 'epub', 'epub']
        if True in [document_prefixes[0] for document_prefix in document_prefixes] + [url.endswith(document_suffix) for document_suffix in document_suffixes]:
            print(f'pdf:{url}, {url_id}')
            self.conn.execute("insert into pdfs(urlid) values (%d)" % (url_id))

class searcher:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self, q):
        # Strings to build query
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # split the words by space
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            # gegt the word ID
            # wordrow = e.con.execute("select * from wordlist").fetchone()
            wordrow = self.con.execute("select rowid from wordlist where word='%s' " % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (
                        tablenumber-1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1
            else:
                print(f'\n\n cant find word: {word}')
                
        # Create the query from the separate parts
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]
        return rows, wordids
    def getscoredlist(self,rows,wordids):
        # context-based ranking
        totalscores=dict([(row[0],0) for row in rows])
        # This is where you'll later put the scoring functions
        weights=[]
        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]
        return totalscores
    def geturlname(self,id):
        # context-based ranking
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone( )[0]
    def query(self,q):
        rows,wordids=self.getmatchrows(q)
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items( )],reverse=1)
        for (score,urlid) in rankedscores[0:10]:
            print ('%f\t%s' % (score,self.geturlname(urlid)))
    
    def normalizescores(self,scores,smallIsBetter=0):
        vsmall=0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0: maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def frequencyscore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows: counts[row[0]]+=1
        return self.normalizescores(counts)

    def locationscore(self,rows):
        locations=dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]: locations[row[0]]=loc
        
        return self.normalizescores(locations,smallIsBetter=1)

    def distancescore(self,rows):
        # If there's only one word, everyone wins!
        if len(rows[0])<=2: return dict([(row[0],1.0) for row in rows])

        # Initialize the dictionary with large values
        mindistance=dict([(row[0],1000000) for row in rows])

        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
            if dist<mindistance[row[0]]: mindistance[row[0]]=dist
        return self.normalizescores(mindistance,smallIsBetter=1)

    def inboundlinkscore(self,rows):
        uniqueurls=dict([(row[0],1) for row in rows])
        inboundcount=dict([(u,self.con.execute('select count(*) from link where toid=%d' % u).fetchone()[0]) for u in uniqueurls])   
        return self.normalizescores(inboundcount)

    def linktextscore(self,rows,wordids):
        linkscores=dict([(row[0],0) for row in rows])
        for wordid in wordids:
            cur=self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
            for (fromid,toid) in cur:
                if toid in linkscores:
                    pr=self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid]+=pr
        maxscore=max(linkscores.values())
        normalizedscores=dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
        return normalizedscores

    def pagerankscore(self,rows):
        pageranks=dict([(row[0],self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        maxrank=max(pageranks.values())
        normalizedscores=dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
        return normalizedscores

    def nnscore(self,rows,wordids):
        # Get unique URL IDs as an ordered list
        urlids=[urlid for urlid in dict([(row[0],1) for row in rows])]
        nnres=mynet.getresult(wordids,urlids)
        scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)


pagelist=['https://en.wikipedia.org/wiki/Programming_language']
#crawler=Crawler('searchindex.db')

pagelist=['https://tapendrapandey.com.np/category/education/books-and-resources', 'https://www.ioenotes.edu.np', 'https://ioe.promod.com.np', 'https://ioesolutions.esign.com.np', 'https://ioenotes.bikrampparajuli.com.np', 'https://www.biofamous.com', 'https://ioeguides.blogspot.com', 'https://notepulchowkcampus.blogspot.com', 'https://ioereader.blogspot.com', 'https://ioengineeringbooks.blogspot.com', 'http://somes.ioe.edu.np', 'https://abhashacharya.com.np', 'https://www.aayushwagle.com.np', 'https://www.nepalshovit.com.np', 'https://pdfcoffee.com']
pagelist.extend(['https://acem.edu.np/pages/downloads', 'https://edunepal.info'])
pagelist.extend(['http://pulchowknotes.blogspot.com', 'http://www.ioenotes.edu.np'])   # ioe notes and syllabus
pagelist.extend(['https://ioesyllabus.com', 'https://ioesyllabus.com/app/Formula', 'https://ioesyllabus.com/app/syllabus', 'https://ioesyllabus.com/app/notes', 'https://ioesyllabus.com/app/Formula', 'https://ioesyllabus.com/app/MSc', 'https://ioesyllabus.com/app/loksewasyllabus'])   # ioe syllabus
crawler=Crawler('pdfdb.db')
try:
    crawler.createindextables() # create table if not already is created
except:
    pass
crawler.crawl(pagelist[:1])         # crawls pages

continue_search = True
while continue_search != False:
    search_text = input('please enter the word to be searched:\t')

    search=searcher('pdfdb.db')
    # search=searcher('searchindex.db')
    print('\n ------------- getmatchrows: ----------------')
    # search.getmatchrows(search_text)

    # context based search
    print('\n ------------- query <context based>: ----------------')
    search.query(search_text)
    continue_search = input('cotinue?')

# Try calling this function with your first multiple-word search:
# reload(searchengine)


# e.con.execute('''select w0.urlid,w0.location,w1.location
# from wordlocation w0,wordlocation w1
# where w0.urlid=w1.urlid
# and w0.wordid=10
# and w1.wordid=17''')

'''
# imports
import engine
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import re

reload(hengine)
e=searcher('searchindex.db')
e.getmatchrows('functional programming')
'''

# import urllib3
# c=urllib3.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
# contents=c.read( )
# print(contents[0:50])

# Used to make requests


# content = urllib.request.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
# print(x.read())
'''
import engine
# pagelist=['http://kiwitobes.com/wiki/Perl.html']
pagelist=['https://en.wikipedia.org/wiki/Programming_language']

crawler=engine.Crawler('searchindex.db')
# crawler.createindextables()     # creates index tables


crawler.crawl(pagelist)         # crawls pages

# checking the entries for a word by querying the database
[row for row in crawler.con.execute(
 'select rowid from wordlocation where wordid=1')]


# querying
select w0.urlid,w0.location,w1.location
from wordlocation w0,wordlocation w1
where w0.urlid=w1.urlid
and w0.wordid=10
and w1.wordid=17

# Try calling this function with your first multiple-word search:
# reload(searchengine)
import engine
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3

import re
e=engine.searcher('searchindex.db')
e.getmatchrows('functional programming')

# context based search
import engine
e=engine.searcher('searchindex.db')
e.query('functional programming')
'''
