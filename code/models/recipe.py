from models.step import StepDto
from models.ingredient import IngredientRecipeDto
from db import Postgres
import logging


class RecipeDto:
    def __init__(self, _id, name, description, steps, ingredients, prep_time, cook_time, servings):
        self.id = _id
        self.name = name
        self.description = description
        self.steps = steps
        self.ingredients = ingredients
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.servings = servings

    def delete(self):
        #delete steps
        StepDto.delete_by_recipe_id(self.id)

        #delete ingredient recipes
        IngredientRecipeDto.delete_by_recipe_id(self.id)

        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'delete from recipes where id = %s;', (self.id,))
        conn.commit()
        Postgres.closeall(conn, cur)

    @classmethod
    def find_by_id(cls, _id):
        conn = Postgres.connect()
        cur = Postgres.execute(
            conn,
            'select id, name, description, prep_time, cook_time, servings from recipes where id = %s;',
            (_id,))
        row = Postgres.fetchone(cur)
        steps = StepDto.find_by_recipe_id(row[0])
        ingredients = IngredientRecipeDto.find_by_recipe_id(row[0])
        recipe = cls(row[0], row[1], row[2], steps, ingredients, row[3], row[4], row[5])
        Postgres.closeall(conn, cur)
        return recipe

    @classmethod
    def find_all(cls):
        conn = Postgres.connect()
        cur = Postgres.execute(
            conn,
            'select id, name, description, prep_time, cook_time, servings from recipes order by name;',
            None)
        rows = Postgres.fetchall(cur)
        recipes = []
        if not rows:
            logging.error('DB lookup returned NoneType when doing look up for all recipes')
            return recipes
        for row in rows:
            steps = StepDto.find_by_recipe_id(row[0])
            ingredients = IngredientRecipeDto.find_by_recipe_id(row[0])
            recipes.append(cls(row[0], row[1], row[2], steps, ingredients, row[3], row[4], row[5]))
        Postgres.closeall(conn, cur)
        return recipes

    def json(self):
        step_list = []
        if self.steps:
            for step in self.steps:
                step_list.append(step.json())

        ingredient_list = []
        if self.ingredients:
            for ingredient in self.ingredients:
                ingredient_list.append(ingredient.json())

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'steps': step_list,
            'ingredients': ingredient_list,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': str(self.servings)
        }

    @staticmethod
    def validate(data):
        missing_fields = ''
        if 'name' not in data:
            missing_fields = 'name'
        if 'description' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'description'
        if 'prep_time' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'prep_time'
        if 'cook_time' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'cook_time'
        if 'servings' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'servings'
        if 'steps' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'steps'
        if 'ingredients' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'ingredients'
        return missing_fields

    @staticmethod
    def update_from_json(_id, data):
        # check for existing recipe, if not found then throw exception
        recipe = None
        if _id:
            recipe = RecipeDto.find_by_id(_id)
            if not recipe:
                return {'error': 'Recipe not found'}, 404

        missing_fields = RecipeDto.validate(data)
        # make sure json data contains all required fields for a recipe
        if len(missing_fields) > 0:
            raise Exception('JSON recipe data missing field(s): ' + missing_fields)

        #update or insert the recipe
        if recipe:
            # update recipe fields
            recipe.name = data['name']
            recipe.description = data['description']
            recipe.prep_time = data['prep_time']
            recipe.cook_time = data['cook_time']
            recipe.servings = data['servings']
        else:
            recipe = RecipeDto(None, data['name'], data['description'], [], [], data['prep_time'], data['cook_time'], data['servings'])
        recipe.update()
        if not recipe.id:
            raise Exception('Error update/inserting recipe into database')

        # update steps
        step_ids = ''
        for step in data['steps']:
            # make sure step has required fields
            missing_fields = StepDto.validate(step)
            if len(missing_fields) > 0:
                raise Exception('JSON step data missing field(s): ' + missing_fields)

            # see if step has an id if so use the id to create a step object otherwise use None for the id
            step_id = None
            if 'id' in step and step['id'] and step['id'] != -1:
                step_id = step['id]']

            updated_step = StepDto(step_id, recipe.id, step['position'], step['description'])
            updated_step.update()

            # make sure the updated step object has an id
            if not updated_step.id:
                raise Exception('Error saving step: ' + str(updated_step.json()))

            # collect all updated or inserted step ids
            if len(step_ids) > 0:
                step_ids += ','
            step_ids += str(updated_step.id)

        # delete any steps in the database for this recipe which weren't updated or inserted above
        StepDto.delete_by_recipe_id_not_in(recipe.id, step_ids)

        # update ingredients
        ingredient_ids = ''
        for ingredient in data['ingredients']:
            # make sure recipe ingredient has required fields
            missing_fields = IngredientRecipeDto.validate(ingredient)
            if len(missing_fields) > 0:
                raise Exception('JSON ingredient data missing field(s): ' + missing_fields)

            # see if recipe ingredient has an id if so use the id to create a recipe ingredient object otherwise use
            # None for the id
            ingredient_id = None
            if 'id' in ingredient and ingredient['id'] and ingredient['id'] != -1:
                ingredient_id = ingredient['id']

            updated_ingredient =IngredientRecipeDto(ingredient_id, recipe.id, ingredient['name'], ingredient['position'], ingredient['unit'], ingredient['amount'])
            updated_ingredient.update()

            # make sure the updated recipe ingredient object has an id
            if not updated_ingredient.id:
                raise Exception('Error saving recipe ingredient: ' + str(updated_ingredient.json()))

            # collect all updated or inserted recipe ingredient ids
            if len(ingredient_ids) > 0:
                ingredient_ids += ','
            ingredient_ids += str(updated_ingredient.id)

        # delete any recipe ingredients in the database for this recipe which weren't updated or inserted above
        IngredientRecipeDto.delete_by_recipe_id_not_in(recipe.id, ingredient_ids)
        return RecipeDto.find_by_id(recipe.id)

    def update(self):
        conn = Postgres.connect()
        if self.id:
            cur = Postgres.execute(
                conn,
                'update recipes set name = %s, description = %s, prep_time = %s, cook_time = %s, servings = %s from recipes where id = %s;',
                (self.name, self.description, self.prep_time, self.cook_time, self.servings, self.id))
        else:
            cur = Postgres.execute(
                conn,
                'insert into recipes (name, description, prep_time, cook_time, servings) values(%s, %s, %s, %s, %s) returning id;',
                (self.name, self.description, self.prep_time, self.cook_time, self.servings))
            self.id = Postgres.fetchone(cur)[0]
        conn.commit()
        Postgres.closeall(conn, cur)
