from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def read_posts():
    with open('data.json', 'r')as f:
        return json.load(f)
@app.route('/')
def index():
    with open('data.json', 'r')as f:
        blog_posts = read_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        posts = read_posts()
        id = len(posts) + 1
        posts.append({'id': id, 'author': author, 'title': title, 'content': content})
        with open('data.json', 'w')as f:
            json.dump(posts, f)
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)