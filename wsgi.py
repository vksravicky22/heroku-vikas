from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from app import app as app

if __name__ == '__main__':
    app.run()
