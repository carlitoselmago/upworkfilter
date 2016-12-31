# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import feedparser
from pprint import pprint
from dict2xml import dict2xml as xmlify
import re
from re import sub
from decimal import Decimal

rssFeed="https://www.upwork.com/ab/feed/topics/rss?securityToken=aa38be043e5b3c12faf6fd43141a2e9caa54842944ec8141f3429cb82c76409946db23d920f6fd3c0a22f0df4424552914102e178c8b7374a6d24de27ef41b02&userUid=796687596739297280&orgUid=796687596743491585"

titleKeywords=["quick","processwire","python","modx","spanish","AI"]
skillsKeywords=["PHP","Python","CSS","Web Scraping","Modx","Spanish"]


minimumBudget=400


#FUNCTIONS

def getBudget(post):
    try:
        budgetStartIndex=str(post.content[0].value).index("Budget</b>:")+12
        budgetEndIndex=str(post.content[0].value)[budgetStartIndex:].index("<")
        budget= str(str(post.content[0].value)[budgetStartIndex+1:budgetStartIndex+budgetEndIndex])
        budget=int(budget.replace(',', ''))
    except:
        budget=False
        
    return budget
    

feed = feedparser.parse(rssFeed, request_headers={'Cache-control': 'max-age=0'})
selected=[]

print "Feed has "+str(len(feed.entries))+" items"

#filter keywords
for post in feed.entries:
   
    #print post.title
    for key in titleKeywords:
        if key.upper() in post.title.upper():
            selected.append(post)
            #print post.title
            
    for key in skillsKeywords:
        if key.upper() in post.content[0].value.upper():
            selected.append(post)
            
  

#filter by Hourly or low bugdet
tempSelected=[]
for i,post in enumerate(selected):
    budget=0
    budget=getBudget(post)
    
    if budget:
        #has budget
        if int(budget)>=minimumBudget:
            tempSelected.append(post)
    else:
        tempSelected.append(post)


    print ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
    print post.title
    print budget,minimumBudget,"BUDGET CHECK::"
    print ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
    print ""
   
selected=tempSelected
    


#remove duplicates
seen_titles = set()
new_list = []
for obj in selected:
    if obj.title not in seen_titles:
        new_list.append(obj)
        seen_titles.add(obj.title)
        
selected=new_list


#END
print ""
print "::::::::::::::"
print ""
for i,post in enumerate(selected):
    #pass
    print post.title
    print post.link
    




if len(selected)==0:
    print "No interesting jobs found"


def convertToRSS(data):
    S=""
    for job in selected:
       S+="<item>"
       S+='<link>'
       S+=job.link
       S+='</link>'
       S+='<title>'
       S+=str(job.title.encode('utf-8'))
       S+='</title>'
       S+='<description>'
       S+='<![CDATA['+str(job.content[0].value.decode('utf-8'))+']]>'
       S+='</description>'
       S+="</item>"
    
    return S

output='<rss version="2.0"><channel>'
output+=convertToRSS(selected)#xmlify(selected, wrap="item", indent="  ")
output+="</channel></rss> "

text_file = open("/var/www/html/upworkfilter/upworkfiltered.xml", "w")
text_file.write(output)
text_file.close()

#with open('upworkfiltered.xml', 'w') as outfile:
    
"""for entry in selected:
    ## Do your processing here
    content = entry.content[0].value
    #clean_content = nltk.word_tokenize(content)
    outfile.write(content)"""
        