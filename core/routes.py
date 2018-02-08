from .views import get_version

def setup_routes(app):
    app.router.add_get('/api/version', get_version)