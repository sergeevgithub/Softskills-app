from app import create_app
from app.routes import routes

app = create_app()
app.register_blueprint(routes)

if __name__ == '__main__':
    # with app.app_context():
    #     from app.models import db
    #     db.create_all()
    app.run(debug=True)
