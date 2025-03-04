# lsof -i :5000: if port 5000 is in use by another program.
# 如果要run flask 在ec2里，需要run code之后，在terminal里看到提示显示例如：running 例如：* Running on http://193.1.167.144:5001，然后用这个网站开就可以打开
# 注意，不同地方有不同的address ip，需要注意把ec2里的ip改变，和确定port是否一致

from flask import Flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)