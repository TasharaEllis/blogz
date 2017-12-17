from flask import Flask, request, redirect, render_template, flash , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

#Blog Class
class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    body = db.Column(db.String(2000))
    created = db.Column(db.DateTime)

    def __init__(self, title, body ):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()

    def is_valid(self):
        if self.title and self.body and self.created:
            return True
        else:
            return False

# "/Blog" Route
@app.route("/blog")
def display_blog_posts():

    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('blog.html', title="Blog Entry", blog=blog)

#Display the posts in order of most recent to the oldest 
    sort = request.args.get('sort')
    if (sort=="newest"):
        all_posts = Blog.query.order_by(Blog.created.desc()).all()
    else:
        all_posts = Blog.query.all()   
    return render_template('all_posts.html', title="All Posts", all_posts=all_posts)

# "/new_post" Route
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
   
    if request.method == 'POST':
        new_post_title = request.form['title']
        new_post_body = request.form['body']
        newpost = Blog(new_post_title, new_post_body)

        if newpost.is_valid():
            db.session.add(newpost)
            db.session.commit()

            url = "/blog?id=" + str(newpost.id)
            return redirect(url)
        else:
            flash("Your Blog post must contain a Title and Body!", 'error')
            return render_template('new_post_form.html',
                title="Create new blog post",
                new_post_title=new_post_title,
                new_post_body=new_post_body)
   
    else:
        return render_template('new_post_form.html', title="Create new blog post")


@app.route("/")
def index():
  
    return redirect("/blog")


if __name__ == '__main__':
    app.run()

