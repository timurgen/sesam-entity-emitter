"""
Very simple service to create some test entities for Sesam
Expose 1 endpoint "/" which may take next arguments
n - number of generated entities
n_fields - number of fields in each entity
with_updated - to populate _updated property with current timestamp
"""
import os
import json
from random import choice
import time
from flask import Flask, request, Response

app = Flask(__name__)

a_lst = []
n_lst = []


def str_to_bool(s: str): return s.lower() == 'true'


def stream_json_list(generator):
    first = True
    yield '['
    for item in generator:
        if not first:
            yield ','
        first = False
        yield json.dumps(item)
    yield ']'


@app.route('/', methods=['GET'])
def generate():
    n = int(request.args.get('n', 100))
    n_f = int(request.args.get('n_fields', 1))
    with_updated = str_to_bool(request.args.get('with_updated', 'False'))
    return Response(
        stream_json_list(
            (
                {
                    **{'_id': str(x), '_updated': time.time() if with_updated else None},
                    **{f'{choice(a_lst)}_{choice(n_lst)}': f'{choice(a_lst)}_{choice(n_lst)}' for _ in range(0, n_f)}
                } for x in range(1, n + 1)
            )
        ), mimetype='application/json'
    )


if __name__ == '__main__':
    with open('english-adjectives.txt', 'r') as f1:
        a_lst = f1.read().splitlines()

    with open('english-nouns.txt', 'r') as f2:
        n_lst = f2.read().splitlines()
    app.run('0.0.0.0', debug=True, port=int(os.environ.get('PORT', 5000)))
