from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.recipe import RecipeList, Recipe
from resources.ingredient import IngredientList, Ingredient
import logging

logging.basicConfig(filename='../home_cooking.log', level=logging.DEBUG)

app = Flask(__name__)

app.config.update(
    ENV='development'
)

CORS(app)

api = Api(app)

api.add_resource(RecipeList, '/recipes')
api.add_resource(Recipe, '/recipes/<int:_id>')
api.add_resource(IngredientList, '/ingredients')
api.add_resource(Ingredient, '/ingredients/<int:_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)