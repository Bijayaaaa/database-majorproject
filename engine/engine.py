
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sqlite3
import re

# from urlparse import urljoin
# from BeautifulSoup import *
# import urllib2
# import urllib.request

# c = urllib.request.urlopen('http://kiwitobes.com/wiki/Programming_language.html')
c = urllib.request.urlopen(
    'https://en.wikipedia.org/wiki/Programming_language')
contents = c.read()

print(contents[:50])

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
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

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
        pass

    # Starting with a list of pages, do breadth first search
    # to the given depth, indexing pages as we go
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib.request.urlopen(page)
                except:
                    print(f"cound not open {page}")
                    continue
                soup = BeautifulSoup(c.read())
                self.addtoindex(page, soup)

                links = soup('a')
                for link in links:
                    if('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if url.find("\'") != -1:
                            continue
                        url = url.split('#')[0]   # remove location portion
                        if url[:4] == 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText = self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                self.dbcommit()
            pages = newpages

    # Create the database tables
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()


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
        wordlist = []

        # split the words by space
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            # gegt the word ID
            wordrow = self.con.execute(
                "select rowid from wordlist where word='%s' " % word).fetchone()
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
        # Create the query from the separate parts
        fullquery = 'select %s from %s where %s' % (
            fieldlist, tablelist, clauselist)
        cur = self.con.execute(fullquery)
        rows = [row for row in cur]
        return rows, wordids


'''
import engine
reload(hengine)
e=engine.searcher('searchindex.db')
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
crawler=engine.Crawler('')



crawler.crawl(pagelist)


crawler=engine.crawler('searchindex.db')
crawler.createindextables()

# index pages
import engine
crawler=engine.Crawler('searchindex.db')
pages= \
['https://en.wikipedia.org/wiki/Programming_language']
crawler.crawl(pages)

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
e=engine.searcher('searchindex.db')
e.getmatchrows('functional programming')


reload(searchengine)
>> e=searchengine.searcher('searchindex.db')
>> e.getmatchrows('functional programming')
'''
