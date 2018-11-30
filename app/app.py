from flask import Flask
import mysql.connector 
import json

app = Flask(__name__)

# DB configuration payload
config = {
  'user': 'root',
  'password': 'root',
  'host': 'db',
  'port': '3306',
  'database': 'people'
}

def get_payload():  
  # Establish connection to DB
  connection = mysql.connector.connect(**config)
  cursor = connection.cursor()
  # Get data
  get = 'SELECT * FROM developers'
  cursor.execute(get)
  # Construct response
  response = [{
    "user": {
      "name": name,
      "age": age
    }
  } for (user_id, name, age) in cursor]
  # Close connection
  cursor.close()
  connection.close()
  # Respond
  return results 

@app.route('/')
def index():
  payload = get_payload()
  return json.dumps(payload)

if __name__ == '__main__':
  app.run(host='0.0.0.0')


