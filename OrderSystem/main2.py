# main.py

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:asd860108@127.0.0.1:5432/Admin_data'

db.init_app(app)

# 重置資料庫
@app.route('/createdb')
def createdb():
    sql = """
        CREATE TABLE collection (
        id INT NOT NULL AUTO_INCREMENT,
        website CHAR(100) NOT NULL,
        title CHAR(100),
        description CHAR(100),
        artical_time CHAR(100),
        insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (ID)
    )
    """
    db.engine.execute(sql) 
    return "資料表建立成功！"

@app.route('/')
def index():

    sql_cmd = """
        select *
        from product
        """

    query_data = db.engine.execute(sql_cmd)
    print(query_data)
    return 'ok'


if __name__ == "__main__":
    app.run()