import requests
import json


def pretty_print_request(request):
    print( '\n{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        request.method + ' ' + request.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )


def pretty_print_response(response):
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code:' + str(response.status_code),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        response.text)
    )


existing_recipes = {}
BASE_URL = 'http://127.0.0.1:5000/recipes'

def test_get_recipe_list():
    global BASE_URL
    global existing_recipes

    # additional headers.
    headers = {'Content-Type': 'application/json'}

    # body
    payload = {}

    response = requests.get(BASE_URL, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response
    assert response.status_code == 200
    existing_recipes = response.json()

    # print full request and response
    pretty_print_request(response.request)
    pretty_print_response(response)


def test_post_recipe_list():
    global BASE_URL
    global existing_recipes

    # additional headers.
    headers = {'Content-Type': 'application/json'}

    # body
    payload = {}

    response = requests.get(BASE_URL, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response
    assert response.status_code == 200
    existing_recipes = response.json()

    # print full request and response
    pretty_print_request(response.request)
    pretty_print_response(response)


def test_get_recipe():
    pass


def test_delete_recipe():
    pass


def test_put_recipe():
    ''' Test that the recipe base fields can be changed, existing steps and ingredients can be changed, deleted and added'''
    pass
