from twit.api.flask import app as application

if __name__ == "__main__":
    application.debug = True
    application.run()
