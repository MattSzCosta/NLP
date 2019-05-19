from flask import Flask,jsonify
from flask_restplus import Api, Resource, fields
from service.textMining import getEntities
from service.treinoML import treino


app = Flask(__name__)
api = Api(app)



listNome = api.model('listNome',{'nomes':fields.List(fields.String)})
texto = api.model('diario',{
        'listTexto':fields.List(fields.String)})

@api.route('/findName')
class identifieName(Resource):
    @api.expect(texto)
    def post(self):
        """Find name at text"""
        return jsonify(getEntities(list(api.payload['text'])))


@api.route('/treinamento')
class treinamento(Resource):
    @api.expect(listNome)
    def post(self):
        """Start treinamento"""
        return jsonify(treino(list(api.payload['nomes'])))


if __name__ == '__main__':
    app.run()
