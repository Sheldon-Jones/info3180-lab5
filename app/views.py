"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory
import os
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from app.forms import MovieForm
from app.models import Movie
from datetime import datetime



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})



# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


# Get all movies (GET) or add a movie (POST)
@app.route('/api/v1/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        form = MovieForm()
        if form.validate_on_submit():
            # Get form data
            title = form.title.data
            description = form.description.data
            poster = form.poster.data
            
            # Save the poster file
            if poster:
                filename = secure_filename(poster.filename)
                # Add timestamp to make filename unique
                filename = f'{datetime.now().timestamp()}_{filename}'
                
                # Create uploads folder if it doesn't exist
                upload_folder = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                poster.save(os.path.join(upload_folder, filename))
            
            # Create and save movie to database
            movie = Movie(title=title, description=description, poster=filename)
            db.session.add(movie)
            db.session.commit()
            
            return jsonify({
                'message': 'Movie Successfully added',
                'title': movie.title,
                'poster': f'/api/v1/posters/{filename}',
                'description': movie.description
            }), 201
        else:
            # Return validation errors
            return jsonify({'errors': form_errors(form)}), 400
    else:
        # GET request - return all movies
        movies = Movie.query.all()
        movies_data = []
        for movie in movies:
            movies_data.append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'poster': f'/api/v1/posters/{movie.poster}'
            })
        return jsonify({'movies': movies_data}), 200
    

    # Serve poster images
@app.route('/api/v1/posters/<filename>')
def get_poster(filename):
    upload_folder = app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, secure_filename(filename))