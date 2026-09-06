from flask import Blueprint, request, jsonify
from .extensions import db
from .models import Post

posts_bp = Blueprint("posts", __name__)


# ---------- CREATE ----------
@posts_bp.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "title và content là bắt buộc"}), 400

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201


# ---------- READ (list) ----------
@posts_bp.route("/posts", methods=["GET"])
def get_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


# ---------- READ (detail) ----------
@posts_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Không tìm thấy post"}), 404

    return jsonify(post.to_dict()), 200


# ---------- UPDATE (toàn phần) ----------
@posts_bp.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Không tìm thấy post"}), 404

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "title và content là bắt buộc"}), 400

    post.title = title
    post.content = content
    db.session.commit()

    return jsonify(post.to_dict()), 200


# ---------- UPDATE (một phần) ----------
@posts_bp.route("/posts/<int:post_id>", methods=["PATCH"])
def patch_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Không tìm thấy post"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        post.title = data["title"]
    if "content" in data:
        post.content = data["content"]

    db.session.commit()
    return jsonify(post.to_dict()), 200


# ---------- DELETE ----------
@posts_bp.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Không tìm thấy post"}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": f"Đã xóa post {post_id}"}), 200
