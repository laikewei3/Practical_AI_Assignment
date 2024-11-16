from flask import Flask, request, jsonify, render_template
from analyze import read_image
from flask_restx import Api, Resource, fields

app = Flask(__name__, template_folder='templates')
api = Api(app, version='1.0', title='Image Analysis API', description='A simple Image Analysis API')
ns = api.namespace('api/v1', description='Image operations')

@app.route("/")
def home():
    return render_template('index.html')


# # API at /api/v1/analysis/
# @app.route("/api/v1/analysis/", methods=['GET'])
# def analysis():
#     # Try to get the URI from the JSON
#     try:
#         get_json = request.get_json()
#         image_uri = get_json['uri']
#     except Exception as error:
#         return jsonify({'error': 'Missing URI in JSON'}), 400
#
#     # Try to get the text from the image
#     try:
#         res = read_image(image_uri)
#
#         response_data = {
#             "text": res
#         }
#
#         return jsonify(response_data), 200
#     except:
#         return jsonify({'error': 'Error in processing'}), 500

image_model = api.model('Image', {
    'uri': fields.String(required=True, description='The image URI') })

@ns.route('/analysis/')
class Analysis(Resource):
    @ns.expect(image_model, validate=True)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error')
    @ns.response(500, 'Internal Server Error')
    def post(self):
        """Analyze image and extract text"""
        image_uri = request.json.get('uri')
        if not image_uri:
            api.abort(400, 'Missing URI in JSON')
        try:
            res = read_image(image_uri)
            response_data = {"text": res}
            return response_data, 200
        except Exception as e:
            print(e)
            api.abort(500, 'Error in processing')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)