###  install
1. python3 -m venv env
   .\env\Scripts\activate
2. ctrl shift  p : Python: Select Interpreter 
3. pip3 install flask

导出包文件描述
pip freeze > requirements.txt


python -m pip install --upgrade pip

安装 flask 插件
pip install flask_httpauth    #token
pip install flask-redis       #redis
pip install flask_sqlalchemy  #mysql
pip install tornado           #tornado