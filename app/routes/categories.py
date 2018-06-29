from flask import Blueprint, make_response, request, jsonify
from flask.views import MethodView
from app.models.categories import Category
from app.handlers.token_handler import assert_token
from app import db

category_blueprint = Blueprint('category', __name__)


class CategoryAPI(MethodView):
    """Categories Resource"""

    def post(self):
        """Handle post request to url /categories"""
        post_data = request.get_json()
        user_id = assert_token(request)

        check_category = Category.query.filter_by(
            name=post_data.get('name')).first()

        if not check_category:
            my_category = Category(
                post_data.get("name"),
                post_data.get("detail"),
                created_by=user_id)

            # insert the user
            db.session.add(my_category)
            db.session.commit()

            response = {
                'Category Id': my_category.id,
                'Recipe Category Name': my_category.name,
                'Recipe Category Detail': my_category.detail,
                'Date Created': my_category.date_created,
                'Date Modified': my_category.date_modified
            }
            return make_response(jsonify(response)), 201
        else:
            response = jsonify({'message': 'Category already exists'})
            return make_response(response), 400


base_url = '/v1/'
# Post
category_post_view = CategoryAPI.as_view('category_post_view')
category_blueprint.add_url_rule(
    base_url + 'categories', view_func=category_post_view, methods=['POST'])
