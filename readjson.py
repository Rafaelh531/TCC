# json file
  
  
import json
  
# Opening JSON file
f = open('C:\\Users\\rafa6899\\Downloads\\sth\\code\\paulistania30m100sample.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data['results']:
    print(i)
  
# Closing file
f.close()