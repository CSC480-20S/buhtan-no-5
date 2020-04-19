import gunicorn.app.wsgiapp as wsgi
from application import create_app
from main import app

app = create_app()

if __name__ == '__main__':
    # runs on localhosts
    app.run(host='0.0.0.0',port=12100, debug=True)
    #wsgi.run()
