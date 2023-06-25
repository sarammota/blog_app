from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


def get_blog_posts():
    with open('posts.json', 'r') as json_file:
        return json.load(json_file)


@app.route('/')
def index():
    blog_posts = get_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Load existing posts
        blog_posts = get_blog_posts()

        # Generate a new ID
        new_id = len(blog_posts) + 1

        post = {'id': new_id, 'author': author, 'title': title, 'content': content}

        # Append the new post
        blog_posts.append(post)

        # Save the updated posts
        with open('posts.json', 'w') as json_file:
            json.dump(blog_posts, json_file, indent=4)

        return redirect('/')

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing posts
    blog_posts = get_blog_posts()

    # Check if the post_id exists
    if 1 <= post_id <= len(blog_posts):
        # Remove the blog post
        blog_posts.pop(post_id - 1)

        # Update the IDs of remaining posts
        for i in range(len(blog_posts)):
            blog_posts[i]['id'] = i + 1

        # Save the updated posts
        with open('posts.json', 'w') as json_file:
            json.dump(blog_posts, json_file, indent=4)

    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    blog_posts = get_blog_posts()

    # Check if the post_id exists
    if 1 <= post_id <= len(blog_posts):
        post = blog_posts[post_id - 1]  # Get the post by index

        if request.method == 'POST':
            author = request.form['author']
            title = request.form['title']
            content = request.form['content']

            # Update the post details
            post['author'] = author
            post['title'] = title
            post['content'] = content

            # Save the updated posts
            with open('posts.json', 'w') as json_file:
                json.dump(blog_posts, json_file, indent=4)

            return redirect('/')

        return render_template('update.html', post=post)

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)




