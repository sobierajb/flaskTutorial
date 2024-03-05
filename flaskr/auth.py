import functools 
from flask import (
    Blueprint,flash,g,redirect,render_template,request,session,url_for
)
import flaskr.repository.user as userRepo

bp = Blueprint('auth', __name__,url_prefix='/auth')

@bp.route('/register',methods=('GET','POST'))
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        error=None
        if not username: 
            error= 'User name not provided.'
        elif not password:
            error = 'Password is required.'

        if error is None: 
            error = userRepo.create(username,password)
            if error is None: 
                return redirect(url_for("auth.login"))
        
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login',methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None 
        user = userRepo.get_by_name(username)

        if user is None:
             error = 'Login failed'
        elif userRepo.authorize(user,password)==False: 
             error = 'Login failed' 
        else:
            session.clear()
            session['user_id']= user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

# bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested. 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = userRepo.get_by_id(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Creating, editing, and deleting blog posts will require a user to be logged in. 
# A decorator can be used to check this for each view it’s applied to.

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None: 
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view