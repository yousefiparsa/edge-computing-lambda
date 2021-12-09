from database import connection
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def sensor_data():
    while(1):
        c, conn = connection()

        query = "SELECT * FROM (SELECT * FROM temps_found ORDER BY\
        time_stamp DESC LIMIT 20) sub ORDER BY time_stamp ASC;"
        c.execute(query)

        data = c.fetchall()

        conn.close()

        return render_template("index.html", data=data)


if(__name__ == '__main__'):
    app.debug = True
    app.env = ""
    app.run('0.0.0.0', port=5000)
