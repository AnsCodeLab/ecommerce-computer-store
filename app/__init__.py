from flask import Flask, g, current_app
import sqlite3
from .db import init_db, get_conn

def create_app(db_path=":memory:"):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path
    app.secret_key = "dev"
    init_db(db_path)

    app.teardown_appcontext(close_db)

    @app.context_processor
    def inject_globals():
        from flask import session
        import datetime
        cart = session.get("cart", {})
        return {
            "cart_count": sum(cart.values()) if cart else 0,
            "year": datetime.date.today().year,
        }

    # Blueprints registered as each module is implemented (TDD, one at a time)
    for modname, attr in [("categories", "bp"), ("items", "bp"),
                          ("customers", "bp"), ("orders", "bp"), ("web", "bp")]:
        try:
            mod = __import__(f"app.{modname}", fromlist=[attr])
            app.register_blueprint(getattr(mod, attr))
        except (ImportError, AttributeError):
            pass

    return app

def get_db():
    if "db" not in g:
        g.db = get_conn(current_app.config["DB_PATH"])
    return g.db

def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

