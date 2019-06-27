import urllib.parse

query = '=1&q=食品安全+牛奶'
out = urllib.parse.quote(query)
print(out)