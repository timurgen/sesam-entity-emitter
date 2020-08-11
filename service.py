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

adj_list = []
noun_list = []


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
    n_fields = int(request.args.get('n_fields', 1))
    with_updated = str_to_bool(request.args.get('with_updated', 'False'))
    return Response(
        stream_json_list(
            [(yield {**{'_id': x, '_updated': time.time() if with_updated else None},
                     **{f'{choice(adj_list)}_{choice(noun_list)}': f'{choice(adj_list)}_{choice(noun_list)}' for _ in
                        range(0, n_fields)}})

             for x in range(1, n + 1)]
        ), mimetype='application/json'
    )


if __name__ == '__main__':
    with open('english-adjectives.txt', 'r') as f1:
        adj_list = f1.read().splitlines()

    with open('english-nouns.txt', 'r') as f2:
        noun_list = f2.read().splitlines()
    app.run('0.0.0.0', debug=True, port=int(os.environ.get('PORT', 5000)))
