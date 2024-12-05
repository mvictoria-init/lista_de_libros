from flask import Blueprint, render_template, redirect, url_for, request, g
#  Blueprint for create views in flask

from .auth import login_required
# for user validation

from .models import Book
from app import db

from werkzeug.utils import secure_filename

bp = Blueprint('book', __name__, url_prefix='/libro')

@bp.route('/lista')
@login_required
def index():
    
    books = Book.query.all()
    return render_template('book/index.html', books=books)

@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
        
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        desc = request.form['desc']
        n_page = request.form['n_page']
        punctuation = int(request.form['rating'])
        
        if request.files['image']:
            image = request.files['image']
            image.save(f'app/static/media/{secure_filename(image.filename)}')
            image = f'media/{secure_filename(image.filename)}'
        
        book = Book(g.user.id, title, author, genre, desc, n_page, punctuation, image)
        
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('book.index'))
    
    return render_template('book/create.html')

# function to call the record by its id
def get_book(id):
    book = Book.query.get_or_404(id)
    return book

@bp.route('/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):

    book = get_book(id)

    if request.method == 'POST':
        
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.desc = request.form['desc']
        book.n_page = request.form['n_page']
        book.punctuation = int(request.form['rating']) 
        
        if request.files['image']:
            image = request.files['image']
            image.save(f'app/static/media/{secure_filename(image.filename)}')
            image = f'media/{secure_filename(image.filename)}'
       
        book.state = True if request.form.get('state') == 'on' else False

        db.session.commit()
        return redirect(url_for('book.index'))
    return render_template('book/update.html', book = book)

@bp.route('/delete/<int:id>')
def delete(id):

    book = get_book(id)
    
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book.index'))
