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


class CategoryID_GET(MethodView):
    """This class handles get request of category with id """

    def get(self, id):
        """
        Handles get on endpoint /categories/<id>
        :returns: 200 <ok>
        """
        user_id = assert_token(request)
        category = Category.query.filter_by(created_by=user_id).filter_by(
            id=id).first()
        if category:
            response = {
                "id": category.id,
                "Recipe Category Name": category.name,
                "Recipe Detail": category.detail,
                "Date created": category.date_created,
                "Date Modified": category.date_modified
            }
            return make_response(jsonify(response)), 200
        return make_response(
            jsonify({
                "message":
                "The category does not exist, Would you like to create one?"
            })), 404


class CategoryUpdate(MethodView):
    """Handles  update on endpoint /categories/<id>
    :returns: 200 <ok>
    """

    def put(self, id):
        """Handles put request"""
        post_data = request.get_json()
        user_id = assert_token(request)
        get_category = Category.query.filter_by(created_by=user_id).filter_by(
            id=id).first()

        if get_category:

            search_category = Category.query.filter_by(
                created_by=user_id).filter_by(
                    name=post_data.get("name")).first()

            name_exists = bool(get_category.name == search_category.name
                               ) if search_category else False

            if not name_exists:
                get_category.name = post_data.get("name")
                get_category.detail = post_data.get("detail")
                get_category.save()
                response = jsonify({
                    "id": get_category.id,
                    "Recipe Category Name": get_category.name,
                    "Recipe Detail": get_category.detail,
                    "Date created": get_category.date_created,
                    "Date Modified": get_category.date_modified
                })
                return make_response(response), 200
            else:
                response = jsonify({'message': 'Category already exists'})
                return make_response(response), 400
        else:
            return make_response(
                jsonify({
                    "message":
                    "The category does not exist, Would you like to create one?"
                })), 404


base_url = '/v1/'
# Post
category_post_view = CategoryAPI_POST.as_view('category_post_view')
category_blueprint.add_url_rule(
    base_url + 'categories', view_func=category_post_view, methods=['POST'])
# Get
category_get_view = CategoryAPI_GET.as_view('category_get_view')
category_blueprint.add_url_rule(
    base_url + 'categories', view_func=category_get_view, methods=['GET'])

# Get by id
category_get_by_id = CategoryID_GET.as_view('category_get_by_id')
category_blueprint.add_url_rule(
    base_url + 'categories/<int:id>',
    view_func=category_get_by_id,
    methods=['GET'])

#Update by id put
category_update = CategoryUpdate.as_view('category_update')
category_blueprint.add_url_rule(
    base_url + 'categories/<int:id>',
    view_func=category_update,
    methods=["PUT"])
