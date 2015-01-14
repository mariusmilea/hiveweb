from app import app
from flask import render_template, request, redirect, url_for, \
    Response, stream_with_context
from hive import HiveQuery
from pyhs2.error import Pyhs2Exception


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('query'))


@app.route('/query', methods=['GET', 'POST'])
def query():
    query = HiveQuery()
    query_text = selected_db = ''
    query_result = []
    databases = query.getdb()
    if request.method == 'POST':
        query_text = request.form['text'].rstrip(';')
        selected_db = request.form['selected_db']
        query = HiveQuery(database=selected_db)
        query_result = [result for result in query.query_exec(query_text)]
        if request.form['btn'] == 'Export':
            def generate_csv():
                """
                generate a csv from the query_result
                """
                yield str(query.columns).strip('[]').replace('\'', '')
                for result in query_result:
                    yield str(result).strip('[]') + '\n'
            return Response(stream_with_context(generate_csv()),
                            mimetype='text/csv')
    return render_template('query.html',
                           title='Query Hive',
                           columns=query.columns,
                           databases=databases,
                           selected_db=selected_db,
                           query_text=query_text,
                           query_result=query_result)


@app.errorhandler(Pyhs2Exception)
def special_exception_handler(error):
    return render_template('500.html', error=error), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('400.html'), 404
