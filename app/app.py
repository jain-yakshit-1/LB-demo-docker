import os
from flask import Flask, request

import os
port = int(os.environ.get("port_env", 5000))

app = Flask(__name__)

@app.route('/')
def index():
	print(request.headers)
	return "Hi!! from server %s" % port

if __name__ == '__main__':
    app.run(host ='0.0.0.0',port=port)

#Run the server in command line as follows:-
# python app.py <Unused port number>
#eg. python app.py 3000