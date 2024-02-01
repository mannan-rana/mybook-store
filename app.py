from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Function to initialize the database
def init_db():
    with app.app_context():
        db.create_all()

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

# Route for listing books
@app.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/')
def home():
    return redirect(url_for('add_book'))

# Route for adding a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            publication_year=request.form['publication_year']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('list_books'))
    return render_template('add_book.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
