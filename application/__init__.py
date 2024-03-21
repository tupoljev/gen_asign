from flask import Flask


def init_app():

    app = Flask(__name__)

    with app.app_context():
        from user.user import user
        app.register_blueprint(user)
        return app