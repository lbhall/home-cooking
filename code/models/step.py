from db import Postgres


class StepDto:
    def __init__(self, _id, recipe_id, position, description):
        self.id = _id
        self.recipe_id = recipe_id
        self.description = description
        self.position = position

    @classmethod
    def find_by_recipe_id(cls, _id):
        conn = Postgres.connect()
        cur = Postgres.execute(
            conn,
            'select id, recipe_id, position, description from steps where recipe_id = %s order by position;',
            (_id,))
        rows = Postgres.fetchall(cur)
        steps = []
        if rows:
            for row in rows:
                steps.append(cls(*row))
            Postgres.closeall(conn, cur)

        return steps

    @staticmethod
    def delete_by_recipe_id_not_in(recipe_id, not_in_ids):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'delete from steps where recipe_id = %s and id not in (' + not_in_ids + ')', (recipe_id,))
        conn.commit()
        Postgres.closeall(conn, cur)

    @staticmethod
    def delete_by_recipe_id(recipe_id):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'delete from steps where recipe_id = %s', (recipe_id,))
        conn.commit()
        Postgres.closeall(conn, cur)

    def delete(self):
        conn = Postgres.connect()
        cur = Postgres.execute(conn, 'delete from steps where recipe_id = %s', (self.id,))
        rows = Postgres.fetchall(cur)
        conn.commit()
        Postgres.closeall(conn, cur)

    def update(self):
        conn = Postgres.connect()
        if self.id:
            cur = Postgres.execute(conn, 'update steps set description = %s, position = %s where id = %s', (self.description, self.position, self.id))
        else:
            cur = Postgres.execute(
                conn,
                'insert into steps (recipe_id, description, position) values (%s, %s, %s) returning id',
                (self.recipe_id, self.description, self.position))
            self.id = Postgres.fetchone(cur)[0]
        conn.commit()
        Postgres.closeall(conn, cur)

    def json(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'description': self.description,
            'position': self.position
        }

    @staticmethod
    def validate(data):
        missing_fields = ''
        if 'position' not in data:
            missing_fields = 'postion'
        if 'description' not in data:
            if len(missing_fields) != 0:
                missing_fields += ','
            missing_fields += 'description'
        return missing_fields
