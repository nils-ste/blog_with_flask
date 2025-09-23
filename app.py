from flask import Flask, request, render_template, redirect, url_for
import json

app = Flask(__name__)

def read_posts():
    with open('data.json', 'r')as f:
        return json.load(f)

def find_post_index(posts, post_id):
    for index in range(len(posts)):
        post = posts[index]
        if post["id"] == post_id:
            return index

    return None


def fetch_post_by_id(post_id):
    with open('data.json', 'r')as f:
        posts = read_posts()
        index_post = find_post_index(posts, post_id)
        return json.load(f)[int(index_post)]

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

@app.route('/delete/<int:post_id>', methods = ['POST'])
def delete(post_id):
    with open('data.json', 'r')as f:
        posts = read_posts()
        index_post = find_post_index(posts, post_id)
        posts.remove(posts[index_post])
        with open('data.json', 'w')as f:
            json.dump(posts, f)
            return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    posts = read_posts()
    index_post = find_post_index(posts, post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        posts[index_post].update({'author': author, 'title': title, 'content': content})
        with open('data.json', 'w') as f:
            json.dump(posts, f)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)