create table if not exists ingredients(
    id serial primary key,
    name varchar(255) not null);

create table if not exists recipes(
    id serial primary key,
    name varchar(255) not null,
    description text,
    servings numeric (5,1),
    prep_time int,
    cook_time int);

create table if not exists steps(
    id serial primary key,
    recipe_id integer,
    description text,
    position integer,
    CONSTRAINT fk_recipe FOREIGN KEY(recipe_id) REFERENCES recipes(id));

create table if not exists recipe_ingredients(
    id serial primary key,
    recipe_id integer,
    name varchar(255),
    position integer,
    unit varchar(255),
    amount varchar(255),
    CONSTRAINT fk_recipe FOREIGN KEY(recipe_id) REFERENCES recipes(id));


DO $$
DECLARE
    _id integer;
BEGIN
    --add base ingredients
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Black Pepper') THEN
        INSERT INTO ingredients(name) values ('Black Pepper');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Salt') THEN
        INSERT INTO ingredients(name) values ('Salt');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Cayenne Pepper') THEN
        INSERT INTO ingredients(name) values ('Cayenne Pepper');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Garlic Clove') THEN
        INSERT INTO ingredients(name) values ('Garlic Clove');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Msg') THEN
        INSERT INTO ingredients(name) values ('Msg');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Garlic Powder') THEN
        INSERT INTO ingredients(name) values ('Garlic Powder');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Ground Bay') THEN
        INSERT INTO ingredients(name) values ('Garlic Bay');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Paprika') THEN
        INSERT INTO ingredients(name) values ('Paprika');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Dry Mustard') THEN
        INSERT INTO ingredients(name) values ('Dry Mustard');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Cubed Ham') THEN
        INSERT INTO ingredients(name) values ('Cubed Ham');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Dry Kidney Beans') THEN
        INSERT INTO ingredients(name) values ('Dry Kidney Beans');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Olive Oil') THEN
        INSERT INTO ingredients(name) values ('Olive Oil');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Onion') THEN
        INSERT INTO ingredients(name) values ('Onion');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Green Bell Pepper') THEN
        INSERT INTO ingredients(name) values ('Green Bell Pepper');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Garlic Minced') THEN
        INSERT INTO ingredients(name) values ('Gariic Minced');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Celery') THEN
        INSERT INTO ingredients(name) values ('Celery');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Water') THEN
        INSERT INTO ingredients(name) values ('Water');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Ham Bone') THEN
        INSERT INTO ingredients(name) values ('Ham Bone');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Bay Leaves') THEN
        INSERT INTO ingredients(name) values ('Bay Leaves');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Dried Thyme') THEN
        INSERT INTO ingredients(name) values ('Dried Thyme');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Dried Sage') THEN
        INSERT INTO ingredients(name) values ('Dried Sage');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Dried Parsley') THEN
        INSERT INTO ingredients(name) values ('Dried Parsley');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Cajun Seasoning, unsalted') THEN
        INSERT INTO ingredients(name) values ('Cajun Seasoning, unsalted');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Smoked Sausage') THEN
        INSERT INTO ingredients(name) values ('Smoked Sausage');
    END IF;
    IF NOT EXISTS(SELECT ID FROM ingredients WHERE name='Rice') THEN
        INSERT INTO ingredients(name) values ('Rice');
    END IF;

    --add base recipes
    IF NOT EXISTS(SELECT ID FROM recipes WHERE name = 'Hall''s BBQ Rub') THEN
        INSERT INTO recipes(
            name,
            description,
            servings,
            prep_time,
            cook_time) values
            (
             'Hall''s BBQ Rub',
             'Based on Walter Jetton''s poultry seasoning, this is the rub we use on many of our smoked meats.',
             8,
             30,
             0
            );
        SELECT ID INTO _id FROM recipes WHERE name = 'Hall''s BBQ Rub';
        -- add steps for recipe
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'Combine all ingredients into a bowl, mixing them thoroughly together.', 0);
        --add ingredients for recipe
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Black Pepper', 0, 'tbs', '3');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Salt', 1, 'tbs', '2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Msg', 2, 'tsp', '1/2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Garlic Powder', 3, 'tbs', '2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Ground Bay', 4, 'tbs', '2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Paprika', 5, '1 tbs + 1 tsp', '');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Dry Mustard', 6, 'tbs', '2');
    END IF;

    IF NOT EXISTS(SELECT ID FROM recipes WHERE name = 'Louisiana Style Red Beans and Rice') THEN
        INSERT INTO recipes(
            name,
            description,
            servings,
            prep_time,
            cook_time) values
            (
             'Red Beans and Rice',
             'I grew up in New Orleans and love good red beans.  This recipe is for classic Louisiana style red beans and rice. Serve with your favorite hot sauce.',
             8,
             30,
             180
            );
        SELECT ID INTO _id FROM recipes WHERE name = 'Hall''s BBQ Rub';
        -- add steps for recipe
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'I like to start with a ham I''ve cooked ealier. Save 5 cups of cubed ham mean, the ham bone and juices.', 0);
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'For the kidney beans I like to use Camellia beans.  First rinse them and then put them in a pot or bowl and cover them with water.  Make sure they are covered by several inches of water.  Leave them to soak overnight.', 1);
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'Chop the onion, bell pepper and celery into small pieces.  In a large pot heat the oil and then add the onion, bell pepper, celery and minced garlic.  Cook until the onion becomes translucent, probably 5 minutes.', 2);
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'Drain the beans.  Add the water, beans, ham, ham bone, ham juices and seasonings to the pot and stir.  Simmer for 2.5 hours, stirring occasionally.  Make sure the beans are not sticking to the bottom of the pot.  If so, try reducing the heat.', 3);
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'Slice the sauage into bite size pieces and add to the pot.  Simmer an additional 30 minutes.', 4);
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'While the sausage is cooking, prepare the rice.', 4);
        INSERT INTO steps (recipe_id, description, position) VALUES (_id, 'Serve the beans over the rice, use your favorite hot sauce to taste.', 4);
        --add ingredients for recipe
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Ham, small cubes', 0, 'cups', '5');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Dry Kidney Beans', 1, 'pound', '1');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Olive Oil', 2, 'cup', '1/4');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Onion', 3, 'large', '1');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Green Bell Pepper', 4, '1', 'chopped');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Garlic, minced', 5, 'tbs', '2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Celery', 6, 'stalks', '2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Water', 7, 'cups', '6');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Bay', 8, 'leaves', '2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Cayenne Pepper', 9, 'tsp', '1/2');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Dried Thyme', 10, 'tsp', '1');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Dried Sage', 11, 'tsp', '1/4');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Dried Parsley', 12, 'tbs', '1');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Cajun Seasoning, unsalted', 13, 'tsp', '1');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Smoked Sausage', 14, 'pound', '1');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Water', 15, 'cups', '6');
        INSERT INTO recipe_ingredients(recipe_id, name, position, unit, amount) values (_id, 'Long Grain Rice', 16, 'cups', '2');
    END IF;
END;
$$;

