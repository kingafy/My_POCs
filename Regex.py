# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:54:42 2018

@author: Anshuman_Mahapatra
"""
import os
os.chdir('D:/Data Science/POC/Regex')
import re

print('\tHello')
print(r'\tHello')

'''
print('\tHello')
        Hello

print(r'\tHello')
\tHello
'''

text_to_search = '''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890
Ha HaHa
MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )
coreyms.com
321-555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234
Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T
cat
mat
pat
bat
'''

sentence = 'Start a sentence and then bring it to an end'

pattern = re.compile(r'abc')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match)
##<_sre.SRE_Match object; span=(1, 4), match='abc'>
    
###IMPORTANT   =====>MetaCharacters (Need to be escaped):
##. ^ $ * + ? { } [ ] \ | ( )
## Ex... \.    \$  if we are trying to search these characters in the data
pattern = re.compile(r'coreyms\.com')
pattern = re.compile(r'.')
## all digits
pattern = re.compile('\d')
##excluding all digits
pattern = re.compile('\D')

##include words a-z A-Z 0-9 and _
pattern = re.compile('\w')

##space /tab  and newline
pattern = re.compile('\s')

##Not space /tab  and newline

pattern = re.compile('\S')


##word boundary 
pattern = re.compile(r'\bHa')

##without word boundary
pattern = re.compile(r'\BHa')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match)
    
    
##Beginning of string  ^

pattern = re.compile(r'^Start')
matches= pattern.finditer(sentence)
for match in matches:
    print(match)
    
##End of string
pattern = re.compile(r'end$')
matches= pattern.finditer(sentence)
for match in matches:
    print(match)    
    
##Phone no matching
pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match) 

###Read data file and do regex for phone no identification
pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d')   
with open('data.txt','r',encoding ='utf-8') as f:
    contents = f.read()
    matches = pattern.finditer(contents)
    for match in matches:
        print(match)


##Include character sets by using brackets.
pattern = re.compile(r'\d\d\d[-.]\d\d\d[-.]\d\d\d')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match)
 
##any number with 8 or 9 with 00
pattern = re.compile(r'[89]00[-.]\d\d\d[-.]\d\d\d')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match)
       


##find all characters ending with at except for bat and pat
pattern = re.compile(r'[^bp]at')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match)
    
##add a quantifier to check telephone 
pattern = re.compile(r'\d{3}[-.]\d{3}[-.]\d{4}')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match)


##optional check  use ? for ex Mr and Mr. if we want to identify both
pattern = re.compile(r'Mr\.?')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match) 
    
##few more combo

pattern = re.compile(r'Mr\.?\s[A-Z]\w+')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match) 


##or check  use () and usi |
pattern = re.compile(r'M(r|s|rs)\.?\s[A-Z]\w+')
matches= pattern.finditer(text_to_search)
for match in matches:
    print(match) 
    
###EMAIL matching
 emails = '''
anshumanmah@gmail.com
rajdps@hotmail.com
indie@gov.in
axy.abc@gmail.com
corey-anderson@gmail.com
corey123@gmail.com
corey_Anderson@gmail.com
'''   
pattern = re.compile(r'[A-Za-z.]+@[a-zA-Z]+\.com')
matches= pattern.finditer(emails)
for match in matches:
    print(match)  

pattern = re.compile(r'[A-Za-z.0-9-_]+@[a-zA-Z]+\.(com|in)')
matches= pattern.finditer(emails)
for match in matches:
    print(match)  
    
    
##for all type of emails
pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
matches= pattern.finditer(emails)
for match in matches:
    print(match)   

##() means group    
###urls
urls = '''
https://www.google.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov
'''

pattern = re.compile(r'https?://(www\.)?(\w+)(\.\w+)')

subbed_urls = pattern.sub(r'\2\3', urls)

print(subbed_urls)



##findall only returns strings no other info

##################
# matches = pattern.finditer(urls)

# for match in matches:
#     print(match.group(3))
    
sentence = 'Start a sentence and then bring it to an end'

pattern = re.compile(r'start', re.I)

matches = pattern.search(sentence)

print(matches)