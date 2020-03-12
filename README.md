# buhtan-no-5
## Getting Started
Team Engine is building the back end with Python >3.5 and Flask-Restful.

First ensure that all of the required packages are installed.
```
python3 -m pip install -r requirements.txt  
```
Next ensure that the .env file is located both in the Crpyto Folder and test_server folder. This is essential
for any of the encryption and decryption operations.Refer to the image below.

![DirSetUp](images/example_dir.png)

[//]: # (### A valid markdown comment but it appears to be only one line)

## Database
Database of use is MongoDB Atlas. This is a NoSQL database which is secured by TLS/SSL authentication. Using pymongo Engine and Database will be able to connect using the MongoClient mondule. To connect to the Database copy and paste the function below.
```
def connector():
    env_path = os.path.abspath(os.path.dirname(__file__))
    location = os.path.join(env_path, '.env')
    load_dotenv(dotenv_path=location)
    client = MongoClient(os.getenv('MongoURL'))
    db = client["StudyStore"]
    return db
```
Then change the "Mongo URL" placeholder with the connection string located in the env file.


## Deployment
TBD, Engine has not decided on the required software to deploy.
For Unix systems with venv installed.
```
source venv/bin/activate
python3 main.py
```

## Documentation
This project will use Sphinx to create local documentation to aide others.There will be a readthedocs in the future.
* [CheatSheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) is a great resourse to utilize in order to improve the README.


## Built With
* [FLASK](https://pypi.org/project/Flask/) - Web Framework used
* [FLASK-RESTFUL](https://flask-restful.readthedocs.io/en/latest/) - RESTFul Framework

## Authors

* **msglarson** - *Initial Documentation work* 
* **besoir** - *Created Magic Button*
