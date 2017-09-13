import requests

f = open('results.txt', 'r')
r = f.read()
re = []
for l in r.split('\n'):
    try:
        v = (l.split(' = ')[0],l.split(' = ')[1].replace('\x00', ''))
        re.append(v)
    except:
        pass
print (re)
g = requests.get('http://110.10.212.131:8777/')
IPython.embed()
for res in re:
    prob = res[0]
    key = res[1]
    payload = {'prob' : str(prob), }
    r = requests.post("http://110.10.212.131:8777/auth.php", data={'prob': prob, 'submit': 'Auth', 'key': key}, cookies=g.cookies)
print requests.get('http://110.10.212.131:8777/', cookies=g.cookies).text
    

