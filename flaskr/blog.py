from flask import (Blueprint,flash,g,redirect,render_template,request,url_for)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
import flaskr.repository.post as postRepo

bp = Blueprint('blog',__name__)


@bp.route('/')
def index():
    posts = postRepo.get_all()
    return render_template('blog/index.html',posts=posts)

@bp.route('/create',methods=['POST','GET'])
@login_required
def create():
    if request.method=='POST':
        title = request.form['title']
        body = request.form['body']
        error = None 

        if not title:
            error = 'Title is required.'
        
        if error is not None: 
            flash(error)
        else: 
            postRepo.create(title,body,g.user['id'])
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=['GET','POST'])
@login_required
def update(id):
    post = get_post(id)
    # if this is a post request then perform logic for post
    if request.method == 'POST': 
        title = request.form['title']
        body = request.form['body'] 
        error = None 

        if not title: 
            error = 'title is required.'
        
        if error is None:
            postRepo.update(id,title,body)
            return redirect(url_for("blog.index"))
        else: 
            flash(error)
     # otherwise render update.html template   
    return render_template('blog/update.html',post = post)

@bp.route('/<int:id>/delete',methods=['POST',])
def delete(id):
    post = get_post(id)

    if request.method=='POST':
        postRepo.delete(post['id'])
        return redirect(url_for('blog.index'))

    return redirect(url_for('blog.index'))


def get_post(id):
    # get a post form db
    post = postRepo.get_by_id(id)
    
    # abort when post is not found 
    if post is None:
        abort(404,f"Post with given id: {id} was not found.")
    
    # check author of the post
    if post['author_id'] != g.user['id']:
        abort(403,'You are not the author of the origianl post.')
    
    # return post
    return post
