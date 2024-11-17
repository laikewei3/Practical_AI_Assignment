from flask import Flask, request, render_template
from flask_restx import Api, Resource, fields, Namespace
from analyze import read_image

app = Flask(__name__, template_folder='templates')

# Create a blueprint for the API
from flask import Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp, version='1.0', title='Image Analysis API', description='A simple Image Analysis API', doc='/docs')

# Define the namespace
ns = Namespace('image', description='Image operations')
api.add_namespace(ns)

# Define the API model
image_model = api.model('Image', {
    'uri': fields.String(required=True, description='The image URI')
})

# API endpoint for image analysis
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

# Register the API blueprint
app.register_blueprint(api_bp)

# Home route for the HTML page
@app.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page with an image analysis form."""
    if request.method == 'POST':
        image_uri = request.form.get('uri')
        if not image_uri:
            return render_template('index.html', error="Image URI is required!")
        try:
            res = read_image(image_uri)
            return render_template('index.html', result=res, image_uri=image_uri)
        except Exception as e:
            print(e)
            return render_template('index.html', error="An error occurred while processing the image.")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
