from flask import request
from flask_restful import Resource
from models.ingredient import IngredientDto
import logging


class Ingredient(Resource):
    def get(self, _id):
        ingredient = IngredientDto.find_by_id(_id)
        if ingredient:
            logging.info("Ingredient {}:{} retrieved".format(ingredient.id, ingredient.name))
            return ingredient.json(), 200
        else:
            logging.error("Ingredient not found with this id:{}".format(_id))
            return {'error': 'Ingredient not found with this id'}, 404

    def put(self, _id):
        ingredient = IngredientDto.find_by_id(_id)
        if ingredient is None:
            logging.error("Ingredient not found with this id:{}".format(_id))
            return {'error': 'Ingredient not found'}, 404
        logging.info("Ingredient {}:{} found".format(ingredient.id, ingredient.name))
        data = request.get_json()
        IngredientDto.update_from_json(data)
        if not ingredient.id:
            logging.error('Error saving ingredient')
            return {'error': 'Error saving ingredient'}, 400
        logging.info("Ingredient {}:{} updated".format(ingredient.id, ingredient.name))
        return ingredient.json(), 201

    def delete(self, _id):
        ingredient = IngredientDto.find_by_id(_id)
        if ingredient is None:
            logging.error("Ingredient not found with this id:{}".format(_id))
            return {'error': 'Ingredient not found'}, 404
        ingredient.delete()
        logging.info("Ingredient {}:{} deleted".format(ingredient.id, ingredient.name))
        return 200


class IngredientList(Resource):
    def get(self):
        ingredients = IngredientDto.find_all()
        list = []
        if ingredients:
            for ingredient in ingredients:
                list.append({'id': ingredient.id, 'name': ingredient.name})
            logging.info('Full ingredient list retrieved')
            return {'ingredients': list}, 200
        else:
            return {'error': 'Error getting ingredients from database.'}

    def post(self):
        data = request.get_json()
        ingredient = IngredientDto(None, data['name'])
        ingredient.update()
        if ingredient.id:
            logging.info("Ingredient {}:{} posted".format(ingredient.id, ingredient.name))
            return ingredient.json(), 201
        else:
            fields = IngredientDto.validate(data)
            if len(fields) > 0:
                return {'error': "Error saving ingredient.  Missing mandatory field(s) ({})".format(fields)}, 400
            else:
                return {'error': "Error saving ingredient.  "}, 400



