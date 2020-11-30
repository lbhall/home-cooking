from db import Postgres


class IngredientDto:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name

    @classmethod
    def find_all(cls):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'select id, name from ingredients order by name;', None)
        rows = Postgres.fetchall(cur)
        ingredients = []
        for row in rows:
            ingredients.append(cls(*row))
        Postgres.closeall(conn, cur)
        return ingredients

    @classmethod
    def find_by_id(cls, _id):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'select id, name from ingredients where id = %s;', (_id,))
        row = Postgres.fetchone(cur)
        ingredient = cls(*row)
        Postgres.closeall(conn, cur)
        return ingredient

    def update(self):
        conn = Postgres.connect()
        if self.id:
            cur = Postgres.execute(conn, 'update ingredients set name = %s where id = %s', (self.name, self.id))
        else:
            cur = Postgres.execute(conn, 'insert into ingredients (name) values (%s) returning id', (self.name,))
            self.id = Postgres.fetchone(cur)[0]
        conn.commit()
        Postgres.closeall(conn, cur)

    def delete(self):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'delete from ingredients where id = %s', (self.id,))
        conn.commit()
        Postgres.closeall(conn, cur)

    def json(self):
        return {'id': self.id, 'name': self.name}

    @staticmethod
    def validate(data):
        missing_fields = ''
        if 'name' not in data:
            missing_fields = 'name'
        return missing_fields

    @staticmethod
    def update_from_json(_id, data):
        # check for existing recipe, if not found then throw exception
        ingredient = IngredientDto.find_by_id(_id)
        if ingredient is None:
            return {'error': 'Ingredient not found'}, 404
        missing_fields = IngredientDto.validate(data)
        # make sure json data contains all required fields
        if len(missing_fields) > 0:
            raise Exception('JSON data missing field(s): ' + missing_fields)

        # update recipe fields
        ingredient.name = data['name']
        ingredient.update()

        return ingredient

class IngredientRecipeDto:
    def __init__(self, _id, recipe_id, name, position, unit, amount):
        self.id = _id
        self.recipe_id = recipe_id
        self.position = position
        self.amount = amount
        self.unit = unit
        self.name = name

    @classmethod
    def find_by_recipe_id(cls, _id):
        conn = Postgres.connect()
        cur = Postgres.execute(
            conn,
            'select id, recipe_id, name, position, unit, amount from recipe_ingredients where recipe_id = %s order by position;',
            (_id,))
        rows = Postgres.fetchall(cur)
        ingedients = []
        if rows:
            for row in rows:
                ingedients.append(cls(*row))
            Postgres.closeall(conn, cur)

        return ingedients

    def json(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'position': self.position,
            'unit': self.unit,
            'amount': self.amount
        }

    @staticmethod
    def validate(data):
        missing_fields = ''
        if 'name' not in data:
            missing_fields = 'name'
        if 'position' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'position'
        if 'amount' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'amount'
        if 'unit' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'unit'

        return missing_fields

    def update(self):
        conn = Postgres.connect()
        if self.id:
            cur = Postgres.execute(
                conn,
                'update recipe_ingredients set name = %s, position = %s, unit = %s, amount = %s where id = %s',
                (self.name, self.position, self.unit, self.amount, self.id))
        else:
            cur = Postgres.execute(
                conn,
                'insert into recipe_ingredients (recipe_id, name, position, unit, amount) values (%s, %s, %s, %s, %s) returning id',
                (self.recipe_id, self.name, self.position, self.unit, self.amount))
            self.id = Postgres.fetchone(cur)[0]
        conn.commit()
        Postgres.closeall(conn, cur)

    @staticmethod
    def delete_by_recipe_id_not_in(recipe_id, not_in_ids):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'delete from recipe_ingredients where recipe_id = %s and id not in (' + not_in_ids + ')', (recipe_id,))
        conn.commit()
        Postgres.closeall(conn, cur)

    @staticmethod
    def delete_by_recipe_id(recipe_id):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'delete from recipe_ingredients where recipe_id = %s', (recipe_id,))
        conn.commit()
        Postgres.closeall(conn, cur)
