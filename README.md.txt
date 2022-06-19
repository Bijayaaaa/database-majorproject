git add .	# if all file are to be updated
git add finelame	# if one file is to be uploaded
git commit -m "what was updated"
git push origin main


# databases
urllist(url)      # <url is a column> <stores list of urls>
wordlist(word)    # <word is a column> <stores list of words>
wordlocation(urlid,wordid,location) # info about wordlocation -> location of word in a page
link(fromid integer, toid integer)  # if two urls have a link, they are stored here <table:urllist.fromid> <table:urllist.toid>
linkwords(wordid,linkid)            # words linking the urls <table:link.linkid> <table:word.wordid>

---------------------------------------------------------------------
--------------------------  searchindex.db --------------------------
---------------------------------------------------------------------
      urllist               |        wordlist            |           wordlocation
rowid       url             |    rowid         word      |  rowid       urlid       wordid      location
1           http://face..   |      1            hello    |     1          2           1            23
1           http://face..   |      2            world    |

# added:
- table to database: 'pdfurl' to store url_id from table urllist if url is pdf or google drive link
- storepdf(url, url_id): function that decides if url is pdf and store to table: 'pdfurl'


# Todo
    pdfs                    |        contains_pdf
rowid       urlid             |   rowid         urlid
  1           2               |     1             2
  2           5               |     2             5
<stores pdf file urls_ids>    |     <stores urls that contain pdf>

- infinite depth for same_website urls
- index/search based on main_tags: [file_name, page_title, urltext]


```
import sqlite3

conn =sqlite3.connect('searchindex.db')
conn =sqlite3.connect('pdfdb.db')
c = conn.cursor()   # create a cursor
print('\nurllist: (url)')
conn.execute(""" select rowid, url from urllist""").fetchall()[:10]

print('\nwordlist:')
conn.execute(""" select rowid, word from wordlist""").fetchall()[:10]

print('\nwordlist:')
conn.execute(""" select rowid, urlid, wordid, location from wordlocation""").fetchall()[:10]


print('\nlink: (link_from_id <int>, link_to_id <int>)')
conn.execute(""" select rowid, fromid, toid from link""").fetchall()[:10]

print('\nlinkwords: (rowid, wordid, linkid)')
conn.execute(""" select rowid, wordid, linkid from linkwords""").fetchall()[:10]


print('\nlinkwords: (rowid, wordid, linkid)')
conn.execute(""" select rowid, wordid, linkid from linkwords""").fetchall()[:10]

print('\nlinkwords: pdfs(urlid)')
conn.execute(""" select urlid from pdfs""").fetchall()[:10]


conn.commit()
conn.close()
```
