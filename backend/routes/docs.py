from flask import Blueprint
from flask_restx import Api, Resource, fields
from flask_jwt_extended import jwt_required

docs_bp = Blueprint('docs', __name__)
api = Api(docs_bp, 
    title='CipherQuest API',
    version='1.0',
    description='A comprehensive API for the CipherQuest CTF learning platform',
    doc='/docs',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type 'Bearer <JWT>' where JWT is the access token"
        }
    },
    security='apikey'
)

# Define common models for documentation
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'email': fields.String(required=True, description='Email address'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'level': fields.Integer(description='User level'),
    'experience': fields.Integer(description='Experience points'),
    'is_admin': fields.Boolean(description='Admin status')
})

module_model = api.model('Module', {
    'id': fields.Integer(readonly=True, description='Module ID'),
    'title': fields.String(required=True, description='Module title'),
    'description': fields.String(description='Module description'),
    'difficulty': fields.String(enum=['beginner', 'intermediate', 'advanced'], description='Difficulty level'),
    'category': fields.String(description='Module category'),
    'duration': fields.String(description='Estimated duration'),
    'lessons': fields.Integer(description='Number of lessons'),
    'progress': fields.Integer(description='User progress percentage'),
    'is_active': fields.Boolean(description='Module availability')
})

challenge_model = api.model('Challenge', {
    'id': fields.Integer(readonly=True, description='Challenge ID'),
    'title': fields.String(required=True, description='Challenge title'),
    'description': fields.String(description='Challenge description'),
    'difficulty': fields.String(enum=['beginner', 'intermediate', 'advanced'], description='Difficulty level'),
    'category': fields.String(description='Challenge category'),
    'points': fields.Integer(description='Points awarded'),
    'module_id': fields.Integer(description='Associated module ID'),
    'is_active': fields.Boolean(description='Challenge availability')
})

leaderboard_entry_model = api.model('LeaderboardEntry', {
    'rank': fields.Integer(description='User rank'),
    'username': fields.String(description='Username'),
    'total_score': fields.Integer(description='Total score'),
    'modules_completed': fields.Integer(description='Modules completed'),
    'challenges_solved': fields.Integer(description='Challenges solved'),
    'level': fields.Integer(description='User level')
})

# Auth namespace
auth_ns = api.namespace('auth', description='Authentication operations')

@auth_ns.route('/register')
class Register(Resource):
    @api.doc('register_user')
    @api.expect(api.model('RegisterInput', {
        'username': fields.String(required=True, description='Username'),
        'email': fields.String(required=True, description='Email address'),
        'password': fields.String(required=True, description='Password'),
        'first_name': fields.String(description='First name'),
        'last_name': fields.String(description='Last name')
    }))
    @api.response(200, 'Success', api.model('AuthResponse', {
        'message': fields.String(description='Success message'),
        'user': fields.Nested(user_model),
        'access_token': fields.String(description='JWT access token'),
        'refresh_token': fields.String(description='JWT refresh token')
    }))
    @api.response(400, 'Validation Error')
    @api.response(409, 'User Already Exists')
    def post(self):
        """Register a new user"""
        pass

@auth_ns.route('/login')
class Login(Resource):
    @api.doc('login_user')
    @api.expect(api.model('LoginInput', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    }))
    @api.response(200, 'Success', api.model('AuthResponse', {
        'access_token': fields.String(description='JWT access token'),
        'refresh_token': fields.String(description='JWT refresh token'),
        'user': fields.Nested(user_model)
    }))
    @api.response(401, 'Invalid Credentials')
    def post(self):
        """Authenticate user and get access tokens"""
        pass

# Modules namespace
modules_ns = api.namespace('modules', description='Learning modules operations')

@modules_ns.route('/')
class ModulesList(Resource):
    @api.doc('list_modules')
    @api.marshal_list_with(module_model)
    @api.response(401, 'Unauthorized')
    def get(self):
        """List all learning modules"""
        pass

@modules_ns.route('/<int:id>')
@api.param('id', 'The module identifier')
class ModuleDetail(Resource):
    @api.doc('get_module')
    @api.marshal_with(module_model)
    @api.response(404, 'Module not found')
    def get(self, id):
        """Get a specific module"""
        pass

# Challenges namespace
challenges_ns = api.namespace('challenges', description='CTF challenges operations')

@challenges_ns.route('/')
class ChallengesList(Resource):
    @api.doc('list_challenges')
    @api.marshal_list_with(challenge_model)
    @api.response(401, 'Unauthorized')
    def get(self):
        """List all CTF challenges"""
        pass

@challenges_ns.route('/<int:id>/submit')
@api.param('id', 'The challenge identifier')
class ChallengeSubmit(Resource):
    @api.doc('submit_flag')
    @api.expect(api.model('FlagSubmission', {
        'flag': fields.String(required=True, description='Challenge flag')
    }))
    @api.response(200, 'Success', api.model('SubmissionResponse', {
        'correct': fields.Boolean(description='Flag correctness'),
        'message': fields.String(description='Response message'),
        'points': fields.Integer(description='Points awarded')
    }))
    @api.response(401, 'Unauthorized')
    @api.response(404, 'Challenge not found')
    def post(self, id):
        """Submit a flag for a challenge"""
        pass

# Leaderboard namespace
leaderboard_ns = api.namespace('leaderboard', description='Leaderboard operations')

@leaderboard_ns.route('/')
class LeaderboardList(Resource):
    @api.doc('list_leaderboard')
    @api.marshal_list_with(leaderboard_entry_model)
    @api.response(401, 'Unauthorized')
    def get(self):
        """Get leaderboard rankings"""
        pass

# AI namespace
ai_ns = api.namespace('ai', description='AI assistant operations')

@ai_ns.route('/chat')
class AIChat(Resource):
    @api.doc('chat_with_ai')
    @api.expect(api.model('ChatInput', {
        'prompt': fields.String(required=True, description='User prompt'),
        'model': fields.String(description='AI model to use'),
        'temperature': fields.Float(description='Response creativity (0-1)'),
        'stream': fields.Boolean(description='Enable streaming response')
    }))
    @api.response(200, 'Success', api.model('ChatResponse', {
        'response': fields.String(description='AI response')
    }))
    @api.response(400, 'Invalid Input')
    @api.response(429, 'Rate Limited')
    @api.response(500, 'Server Error')
    def post(self):
        """Send a prompt to the AI assistant"""
        pass

# Health check
@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.response(200, 'Healthy', api.model('HealthResponse', {
        'status': fields.String(description='Service status'),
        'message': fields.String(description='Status message'),
        'timestamp': fields.DateTime(description='Current timestamp')
    }))
    def get(self):
        """Health check endpoint"""
        pass 