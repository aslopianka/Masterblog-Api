from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog-Api' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        new_post = {
            "id": max((post['id'] for post in POSTS), default=0) + 1,
            "title": request.json.get('title'),
            "content": request.json.get('content'),
        }

        if not new_post or new_post.get('title') is None or new_post.get('content') is None:
            return jsonify({"error": "Invalid post data"}), 400

        POSTS.append(new_post)

        return jsonify(POSTS), 201

    else:
        sort = request.args.get('sort', None)
        direction = request.args.get('direction', None)

        if (sort and direction and
                sort not in ['title', 'content'] and
                direction not in ['asc', 'desc']):
            
            return jsonify({"error": "Invalid sort or direction parameters"}), 400

        sorted_posts = POSTS

        if sort and direction:
            if direction == 'asc' :
                sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=False)
            elif direction == 'desc':
                sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=True)

        return jsonify(sorted_posts)


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if post:
        data = request.get_json()

        post['title'] = data.get('title', post['title'])
        post['content'] = data.get('content', post['content'])

        return jsonify(post), 200

    else:
        return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((post for post in POSTS if post['id'] == post_id), None)
    if post:
        POSTS.remove(post)
        return jsonify({"message": f"Post with the id {post_id} deleted successfully"}), 200

    else:
        return jsonify({"error": "Post not found"}), 404


@app.route('/api/posts/search', methods=['GET'])
def get_post_by_search():
    title_search = request.args.get('title')
    content_search = request.args.get('content')

    if not title_search and not content_search:
        return jsonify({"error": "Please provide a title or content you would like to search by."}), 400

    matching_post = None

    for post in POSTS:
        title_match = False
        content_match = False

        if title_search and title_search.lower() in post['title'].lower():
            title_match = True

        if content_search and content_search.lower() in post['content'].lower():
            content_match = True

        if title_match or content_match:
            matching_post = post
            break

    if matching_post:
        return jsonify(matching_post), 200
    else:
        return jsonify({"error": "Post not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
