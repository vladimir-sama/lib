from flask import Flask, send_from_directory, send_file, render_template, redirect, abort, jsonify, url_for, request, g, session
import sqlite3, secrets, time, datetime, string, re, os, sys, glob
from typing import Dict, Any, Callable, Tuple, Union, Optional, List

current_directory : str = os.path.dirname(os.path.abspath(__file__))
database_path : str = os.path.join(current_directory, 'library.db')

app : Flask = Flask(__name__)
app.config['DATABASE'] = database_path
app.secret_key = '53f1ec3f958a2f9c32dc00478df64684'

def get_database() ->  sqlite3.Connection:
    if 'db_library' not in g:
        g.db_library : sqlite3.Connection = sqlite3.connect(app.config['DATABASE'])
    return g.db_library

@app.route('/')
def home() -> Union[str, Any]:
    return render_template('home.html')

@app.route('/edit/<code>/delete')
def delete_book(code:str) -> Union[str, Any]:
    conn : sqlite3.Connection = get_database()
    cursor : sqlite3.Cursor = conn.cursor()
    cursor.execute('SELECT id FROM books WHERE id = ? LIMIT 1', (code,))
    if not cursor.fetchone():
        abort(404)
    delete_query : str = 'DELETE FROM books WHERE id = ?'
    cursor.execute(delete_query, (code,))
    conn.commit()
    return redirect(url_for('list_books'))

@app.route('/edit/<code>', methods=['GET', 'POST'])
def edit_book(code:str) -> Union[str, Any]:
    page_action : str = '/edit/' + code
    conn : sqlite3.Connection = get_database()
    cursor_data : sqlite3.Cursor = conn.cursor()
    cursor_data.execute('SELECT * FROM books WHERE id = ? LIMIT 1', (code,))
    selected_book : Optional[Tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, int, int, int, str]] = cursor_data.fetchone()
    if not selected_book:
        abort(404)
    isbn_11 : str = selected_book[1]
    isbn_13 : str = selected_book[2]
    title : str = selected_book[3]
    edition : str = selected_book[4]
    editor : str = selected_book[5]
    extension : str = selected_book[6]
    authors : str = selected_book[7]
    location : str = selected_book[8]
    position : str = selected_book[9]
    classification : str = selected_book[10]
    tags : str = selected_book[11]
    notes : str = selected_book[12]
    characteristics : str = selected_book[13]
    language : str = selected_book[14]
    year : int = selected_book[15]
    last_modified : int = selected_book[16]
    time_added : int = selected_book[17]
    collection : str = selected_book[18]
    template : Callable = lambda **kwargs: render_template('book.html', code=code, page_action=page_action, value_isbn_11=isbn_11, value_isbn_13=isbn_13, value_title=title, value_edition=edition, value_authors=authors, value_editor=editor, value_year=year, value_extension=extension, value_location=location, value_position=position, value_tags=tags, value_characteristics=characteristics, value_language=language, value_classification=classification, value_notes=notes, value_collection=collection, time_added_formatted=datetime.datetime.fromtimestamp(time_added).strftime("%H:%M %d/%m/%Y"), last_modified_formatted=datetime.datetime.fromtimestamp(last_modified).strftime("%H:%M %d/%m/%Y"))
    if request.method == 'POST':
        data_isbn_11 : str = request.form.get('isbn_11', '')
        data_isbn_13 : str = request.form.get('isbn_13', '')
        data_title : str = request.form.get('title', '')
        data_edition : str = request.form.get('edition', '')
        data_authors : str = request.form.get('authors', '')
        list_authors : List[str] = [author.strip() for author in data_authors.strip().split(',')]
        data_collection : str = request.form.get('collection', '')
        data_editor : str = request.form.get('editor', '')
        data_year : str = request.form.get('year', '')
        data_extension : str = request.form.get('extension', '')
        data_location : str = request.form.get('location', '')
        data_position : str = request.form.get('position', '')
        data_language : str = request.form.get('language', '')
        data_tags : str = request.form.get('tags', '')
        data_characteristics : str = request.form.get('characteristics', '')
        data_classification : str = request.form.get('classification', '')
        list_classification : List[str] = [classification.strip() for classification in data_classification.strip().split(',')]
        data_notes : str = request.form.get('notes', '')
        if not (data_isbn_11 or data_isbn_13):
            return template(message_add='No ISBN entered')
        if not data_title:
            return template(message_add='No title entered')
        if not list_authors:
            return template(message_add='No authors entered')
        
        cursor : sqlite3.Cursor = conn.cursor()
        update_query : str = '''
            UPDATE books
            SET isbn_11 = ?,
                isbn_13 = ?,
                title = ?,
                edition = ?,
                editor = ?,
                extension = ?,
                authors = ?,
                location = ?,
                position = ?,
                classification = ?,
                tags = ?,
                notes = ?,
                physical_characteristics = ?,
                language = ?,
                year = ?,
                last_modified = ?,
                collection = ?
            WHERE id = ?
        '''
        time_modified : int = int(time.time())
        cursor.execute(update_query, (data_isbn_11, data_isbn_13, data_title, data_edition, data_editor, data_extension, ','.join(list_authors), data_location, data_position, ','.join(list_classification), data_tags, data_notes, data_characteristics, data_language, data_year, time_modified, data_collection, code))
        conn.commit()
        return redirect(url_for('edit_book', code=code))
    return template()

@app.route('/add/', methods=['GET', 'POST'])
def add_book() -> Union[str, Any]:
    page_action : str = '/add'
    if request.method == 'POST':
        data_isbn_11 : str = request.form.get('isbn_11', '')
        data_isbn_13 : str = request.form.get('isbn_13', '')
        data_title : str = request.form.get('title', '')
        data_edition : str = request.form.get('edition', '')
        data_authors : str = request.form.get('authors', '')
        list_authors : List[str] = [author.strip() for author in data_authors.strip().split(',')]
        data_collection : str = request.form.get('collection', '')
        data_editor : str = request.form.get('editor', '')
        data_year : str = request.form.get('year', '')
        data_extension : str = request.form.get('extension', '')
        data_location : str = request.form.get('location', '')
        data_position : str = request.form.get('position', '')
        data_language : str = request.form.get('language', '')
        data_tags : str = request.form.get('tags', '')
        data_characteristics : str = request.form.get('characteristics', '')
        data_classification : str = request.form.get('classification', '')
        list_classification : List[str] = [classification.strip() for classification in data_classification.strip().split(',')]
        data_notes : str = request.form.get('notes', '')
        if not (data_isbn_11 or data_isbn_13):
            return render_template('book.html', page_action=page_action, message_add='No ISBN entered')
        if not data_title:
            return render_template('book.html', page_action=page_action, message_add='No title entered')
        if not list_authors:
            return render_template('book.html', page_action=page_action, message_add='No authors entered')
        conn : sqlite3.Connection = get_database()
        cursor : sqlite3.Cursor = conn.cursor()
        insert_query : str = '''
            INSERT INTO books (isbn_11, isbn_13, title, edition, editor, extension, authors, location, position, classification, tags, notes, physical_characteristics, language, year, last_modified, time_added, collection)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        time_added : int = int(time.time())
        cursor.execute(insert_query, (data_isbn_11, data_isbn_13, data_title, data_edition, data_editor, data_extension, ','.join(list_authors), data_location, data_position, ','.join(list_classification), data_tags, data_notes, data_characteristics, data_language, data_year, time_added, time_added, data_collection))
        code : int = cursor.lastrowid
        conn.commit()
        return redirect(url_for('edit_book', code=code))
    return render_template('book.html', page_action=page_action)

@app.route('/list/', methods=['GET', 'POST'])
def list_books() -> Union[str, Any]:
    conn : sqlite3.Connection = get_database()
    cursor : sqlite3.Cursor = conn.cursor()
    results : List[Tuple[int, str, str]] = []
    search_filter : str = ''
    search_sort : str = ''
    search_query : str = ''
    if request.method == 'POST':
        search_query = request.form.get('search_query', '')
        sort_by : str = request.form.get('sort_option', '')
        if sort_by not in ['time_added', 'last_modified']:
            abort(404)
        search_sort = sort_by.replace('_', ' ').capitalize()
        filter_by : str = request.form.get('search_option', '')
        if filter_by not in ['title', 'authors', 'collection', 'language']:
            abort(404)
        search_filter = filter_by.capitalize()
        if search_query:
            match filter_by:
                case 'title':
                    base : str = 'SELECT id, title, authors FROM books WHERE title LIKE ?'
                    search_term_list : list = [x.lower() for x in search_query.split()]
                    for item in search_term_list:
                        for char in string.punctuation:
                            item = item.replace(char, '')
                    keyword_list : list = []
                    if search_term_list:
                        first : str = search_term_list.pop(0)
                        if first:
                            keyword_list.append('%' + first + '%')
                            for keyword in search_term_list:
                                if keyword:
                                    base = base + ' AND title LIKE ?'
                                    keyword_list.append('%' + keyword + '%')
                            keyword_tuple : tuple = tuple(keyword_list)
                            cursor.execute(base + 'ORDER BY %s DESC' % sort_by, keyword_tuple)
                            results = cursor.fetchall()
                case 'authors':
                    base : str = 'SELECT id, title, authors FROM books WHERE authors LIKE ? ORDER BY %s DESC' % sort_by
                    cursor.execute(base, ('%' + search_query + '%',))
                    results = cursor.fetchall()
                case 'collection':
                    base : str = 'SELECT id, title, authors FROM books WHERE collection LIKE ? ORDER BY %s DESC' % sort_by
                    cursor.execute(base, ('%' + search_query + '%',))
                    results = cursor.fetchall()
                case 'language':
                    base : str = 'SELECT id, title, authors FROM books WHERE language LIKE ? ORDER BY %s DESC' % sort_by
                    cursor.execute(base, ('%' + search_query + '%',))
                    results = cursor.fetchall()
    else:
        select_query : str = '''
            SELECT id, title, authors
            FROM books
            ORDER BY time_added DESC
        '''
        cursor.execute(select_query)
        results = cursor.fetchall()
    return render_template('list.html', results=results, search_query=search_query, search_filter=search_filter, search_sort=search_sort)

@app.errorhandler(404)
def not_found(error:Exception) -> Union[str, Any]:
    return render_template('404.html'), 404

@app.teardown_appcontext
def close_database(e) -> None:
    db_library = g.pop('db_library', None)
    if db_library is not None:
        db_library.close()

if __name__ == '__main__':
    try:
        app.run('0.0.0.0', 5555, True)
    except KeyboardInterrupt:
        pass
