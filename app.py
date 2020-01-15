from flask import Flask, render_template,request, redirect

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# mysql+pymysql://username:password@server:port/nom_de_la_bd

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:fire@localhost:3306/blogpost'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable = False, default='Unknown')
    date_pub = db.Column(db.DateTime,nullable=False, default = datetime.utcnow )

    def __repr__(self):
        return 'BlogPost ',str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


# post = [
#     {
#         'title' :'Post 1',
#         'content': 'je suis sur le post 1',
#         'author': 'Grace'
#     },
#     {
#         'title': 'Post 2',
#         'content': ' je suis sur le post 2',
#         'author': 'nadia'
#     },
#     {
#         'title': 'Post 3',
#         'content': 'je suis cette post, alors je ne sais l\'autre de c\'est post'
#     }
# ]


@app.route('/post',methods=['POST','GET'])
def page():
    if(request.method == 'POST'):
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        db.session.add(BlogPost(title = post_title,content=post_content,author=post_author))
        db.session.commit()
        return redirect('/post')
    else:
        all_post = BlogPost.query.order_by(BlogPost.date_pub).all()
        return render_template('post.html',posts = all_post)

@app.route('/post/edit/<int:id>',methods=['POST','GET'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if(request.method == 'POST'):
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/post')
    else:   
        return render_template('edit.html',post = post)

@app.route('/post/delete/<int:id>',methods=['POST','GET'])
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/post')


# create de new_post 
@app.route('/post/new', methods=['GET','POST'])
def new_post():
    if(request.method == 'POST'):
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        db.session.add(BlogPost(title=post_title,content=post_content,author=post_author))
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('new_post.html')




if __name__ == '__main__':
    app.run(debug=True)