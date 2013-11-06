import requests
import sys

for i in range(1,218):
    data = requests.get('http://localhost:8000/myapp/integrated/%d/' % i )
    content = data.content
#    print '\r[%d/218] ' % i
    print >> sys.stdout, "\r%d/218" %i,
    sys.stdout.flush()
