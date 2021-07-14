from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile("settings.py", silent=True)

    with app.app_context():
        from .blueprints.home import home
        app.register_blueprint(home.home_bp)
        return app
