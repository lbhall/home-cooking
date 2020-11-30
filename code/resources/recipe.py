from flask import request
from flask_restful import Resource
from models.recipe import RecipeDto
import logging


class Recipe(Resource):
    def get(self, _id):
        recipe = RecipeDto.find_by_id(_id)
        if recipe:
            logging.info("Recipe {}:{} retrieved".format(recipe.id, recipe.name))
            return recipe.json(), 200
        else:
            logging.error('Recipe not found')
            return {'error': 'Recipe not found'}, 404

    def put(self, _id):
        recipe = RecipeDto.update_from_json(_id, request.get_json())
        if recipe is None:
            logging.error('Error saving recipe')
            return {'error': 'Error saving recipe'}, 400
        logging.info("Recipe {}:{} updated".format(recipe.id, recipe.name))
        return recipe.json(), 201

    def delete(self, _id):
        recipe = RecipeDto.find_by_id(_id)
        if recipe is None:
            logging.error('Recipe not found')
            return {'error': 'Recipe not found'}, 404
        recipe.delete()
        logging.info("Recipe {}:{} deleted".format(recipe.id, recipe.name))
        return 200


class RecipeList(Resource):
    def get(self):
        recipes = RecipeDto.find_all()
        list = []
        for recipe in recipes:
            list.append(recipe.json())

        logging.info('Retrieved full recipe list')
        return {'recipes': list}, 200

    def post(self):
        data = request.get_json()
        try:
            recipe = RecipeDto.update_from_json(None, data)
        except (Exception) as error:
            logging.error("{}:{}".format(type(error).__name__, str(error)))
            return {'error': "{}:{}".format(type(error).__name__, str(error))}

        if recipe:
            logging.info("Recipe {}:{} posted".format(recipe.id, recipe.name))
            return recipe.json(), 201

        fields = RecipeDto.validate(data)
        if len(fields) > 0:
            logging.error("Error saving recipe.  Missing mandatory field(s) ({})".format(fields))
            return {'error': "Error saving recipe.  Missing mandatory field(s) ({})".format(fields)}, 400

        logging.error("Error saving recipe.")
        return {'error': "Error saving recipe."}, 400
