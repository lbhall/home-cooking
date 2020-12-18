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


def test_get_recipe():
    url = 'http://127.0.0.1:5000/recipes'

    # additional headers.
    headers = {'Content-Type': 'application/json'}

    # body
    payload = {}

    response = requests.get(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response
    assert response.status_code == 200
    response_body = response.json()
    #assert response_body['url'] == url

    # print full request and response
    pretty_print_request(response.request)
    pretty_print_response(response)