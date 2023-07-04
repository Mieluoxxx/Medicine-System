from models import db
from config import app
from route import bp

app.register_blueprint(bp)  # 设置路由
db.init_app(app)
with app.app_context():
    db.create_all()


@app.cli.command("init-db")
def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()
    with open("./sql/data.sql", "rb") as f:
        sql = f.read()
    statements = sql.decode().split(";")
    engine = db.get_engine()
    for statement in statements:
        if statement.strip():
            engine.execute(statement)
    print("Database initialized.")


@app.cli.command("init-trigger")
def init_db():
    with open("./sql/Trigger.sql", "rb") as f:
        sql = f.read()
    statements = sql.decode().split(";")
    engine = db.get_engine()
    for statement in statements:
        if statement.strip():
            engine.execute(statement)
    print("Trigger initialized.")


if __name__ == '__main__':
    app.run(debug=True)
    db.session.commit()
