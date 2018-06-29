from flask import Blueprint, make_response, request, jsonify
from flask.views import MethodView
from app.models.categories import Category
from app.handlers.token_handler import assert_token
from app import db

category_blueprint = Blueprint('category', __name__)


class CategoryAPI_POST(MethodView):
    """This class handles get requests on category endpoint"""

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


class CategoryAPI_GET(MethodView):
    """This class handle post request on categories endpoints"""

    def get(self):
        """Handles get on endpoint /categories
        :returns: 200 <ok>"""

        user_id = assert_token(request)
        categories_data = Category.query.filter_by(created_by=user_id)
        result = []
        for each_category in categories_data:
            obj = {
                "id": each_category.id,
                "Recipe Category Name": each_category.name,
                "Recipe Category Detail": each_category.detail,
                "Date Created": each_category.date_created,
                "Date Modified": each_category.date_modified
            }
            result.append(obj)
        if not result:  # if result is empty
            result.append("Nothing here yet")
        response = jsonify(result)
        status = 200 if result[0] != "Nothing here yet" else 222
        return make_response(response), status


base_url = '/v1/'
# Post
category_post_view = CategoryAPI_POST.as_view('category_post_view')
category_blueprint.add_url_rule(
    base_url + 'categories', view_func=category_post_view, methods=['POST'])
# Get
category_get_view = CategoryAPI_GET.as_view('category_get_view')
category_blueprint.add_url_rule(
    base_url + 'categories', view_func=category_get_view, methods=['GET'])
