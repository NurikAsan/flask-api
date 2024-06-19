from flask import Blueprint, request, jsonify
import validators
from src.database import Bookmarks, db
from src.constants.http_status_codes import (HTTP_409_CONFLICT,
                                             HTTP_400_BAD_REQUEST,
                                             HTTP_201_CREATED,
                                             HTTP_200_OK)
from flask_jwt_extended import jwt_required, get_jwt_identity

bookmarks = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')


@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required
def bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            }), HTTP_400_BAD_REQUEST

        if Bookmarks.query.filter_by(url=url).first():
            return jsonify({
                'error': 'URL already exists'
            }), HTTP_409_CONFLICT

        bookmark = Bookmarks(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), HTTP_201_CREATED
    else:
        bookmarks = Bookmarks(user_id=current_user)

        data = []

        for bookmark in bookmarks.items:
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visit': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at,
            })

        return jsonify({'data': data}), HTTP_200_OK
