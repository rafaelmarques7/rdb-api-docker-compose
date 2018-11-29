from flask import Flask
import mysql.connector 
import json

app = Flask(__name__)

def get_payload():  
  config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'people'
  }
  connection = mysql.connector.connect(**config)
  cursor = connection.cursor()
  # get command
  get = 'SELECT * FROM developers'
  cursor.execute(get)
  # iterate over response
  results = [{
    "user": {
      "name": name,
      "age": age
    }
  } for (user_id, name, age) in cursor]
  print(results)
  cursor.close()
  connection.close()
  return results 

@app.route('/')
def index():
  #get user data
  payload = get_payload()
  return json.dumps(payload)

if __name__ == '__main__':
  print("running main app.py")
  app.run(host='0.0.0.0')
  #app.run(host='localhost:5000')


