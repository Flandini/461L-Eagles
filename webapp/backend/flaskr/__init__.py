import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flaskr import db
    db.init_app(app)

    #Import models
    from flaskr import model, book, Abstract_review, Amazon_review

    # Import controllers
    from flaskr import home_controller, book_controller, search_controller, auth_controller, about_controller, user_controller
    # app.register_blueprint(auth.bp)
    app.register_blueprint(home_controller.bp)
    app.register_blueprint(book_controller.bp)
    app.register_blueprint(search_controller.bp)
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(about_controller.bp)
    app.register_blueprint(user_controller.bp)

    app.add_url_rule('/', endpoint='index')

    return app
