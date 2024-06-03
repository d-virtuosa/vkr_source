from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from app.models import Post, User
from app import db
from datetime import datetime
from sqlalchemy import text
from jinja2 import Template

bp = Blueprint("main", __name__)

@bp.route('/', methods=['GET'])
def index():
    if 'user_id' in session:
        return redirect(url_for('main.list_post'))
    else:
        return redirect(url_for('main.login'))

@bp.route('/list_post', methods=['GET'])
def list_post():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            current_username = user.username

        else:
            current_username = None

        if user_id == 1:
            filter_category = request.args.get('filter', '')
            if filter_category:
                # Secure
                #posts = Post.query.filter_by(category=filter_category).all()
                
                #Insecure
                query = "SELECT * FROM posts WHERE category='{}';".format(filter_category)
                result = db.engine.execute(query)
                posts = result.fetchall()
            else:
                posts = Post.query.all()
            categories = set(post.category for post in Post.query.all())
            return render_template('blog.html', posts=posts, categories=categories, current_username=current_username, current_filter=filter_category)
        else:
            return render_template('no_access.html', current_username=current_username)
    
    
    # Pass current_username to the template context
    return render_template('blog.html', posts=posts, categories=categories, current_username=current_username)

@bp.route("/create_post", methods=["POST"])
def create_post():
    title = request.form["title"]
    category = request.form["category"]
    content = request.form["content"]
    created_at = datetime.now()
    
    # Introducing SSTI vulnerability by rendering the content using the Jinja2 Template class
    rendered_content = Template(content).render()
    
    new_post = Post(title=title, category=category, content=rendered_content, created_at=created_at)
    db.session.add(new_post)
    db.session.commit()
    
    return redirect(url_for("main.list_post")) 


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect(url_for("main.list_post"))  # Redirect authenticated users to /list_post
        else:
            return render_template("login.html", message="Invalid username or password")
    return render_template("login.html")

@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            return render_template("register.html", message="Username already exists")
        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.login"))
    return render_template("register.html")


@bp.before_request
def require_login():
    allowed_routes = ['main.login', 'main.register']  # List of routes that don't require authentication
    if request.endpoint not in allowed_routes:
        # Check if the user ID is in the session
        user_id = session.get('user_id')
        current_app.logger.debug(f"User ID from session: {user_id}")
        if user_id:
            # Check if the user exists in the database
            user = User.query.get(user_id)
            if user:
                # User is authenticated, continue with the request
                return
            else:
                current_app.logger.warning("User not found in the database")
        else:
            current_app.logger.warning("User ID not found in session")
        # If the user is not authenticated or doesn't exist, redirect to the login page
        return redirect(url_for('main.login'))

