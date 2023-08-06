'''
CodonGenie (c) University of Manchester 2016

CodonGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  neilswainston
'''
import json
import operator
import os
import sys
import traceback
import uuid

from flask import Flask, jsonify, request, Response

from codon_genie.codon_utils import CodonSelector
from synbiochem.utils import seq_utils


# Configuration:
DEBUG = True
SECRET_KEY = str(uuid.uuid4())

# Create application:
_STATIC_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'static')
APP = Flask(__name__, static_folder=_STATIC_FOLDER)
APP.config.from_object(__name__)

_ORGANISMS = sorted(seq_utils.get_codon_usage_organisms().items(),
                    key=operator.itemgetter(0))

_CODON_SELECTOR = CodonSelector()


@APP.route('/')
def home():
    '''Serves homepage.'''
    return APP.send_static_file('index.html')


@APP.route('/organisms/')
def get_all_organisms():
    '''Gets all organisms.'''
    return _get_organisms([{'id': organism[1], 'name': organism[0]}
                           for organism in _ORGANISMS])


@APP.route('/organisms/<term>')
def get_organisms(term):
    '''Gets organisms from search term.'''
    return _get_organisms([{'id': organism[1], 'name': organism[0]}
                           for organism in _ORGANISMS
                           if term.lower() in organism[0].lower()])


@APP.route('/codons')
def get_codons():
    '''Gets codons.'''
    if 'aminoAcids' in request.args:
        codons = _CODON_SELECTOR.optimise_codons(request.args['aminoAcids'],
                                                 request.args['organism'])
    else:
        codons = _CODON_SELECTOR.analyse_codon(request.args['codon'],
                                               request.args['organism'])

    return Response(json.dumps(codons, indent=3, sort_keys=True),
                    mimetype='application/json')


@APP.errorhandler(Exception)
def handle_exception(err):
    '''Exception handling method.'''
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    response = jsonify({'message': err.__class__.__name__ + ': ' + str(err)})
    response.status_code = 500
    return response


def _get_organisms(organisms):
    '''Gets organisms in json format.'''
    return Response(json.dumps(organisms, indent=3, sort_keys=True),
                    mimetype='application/json')
