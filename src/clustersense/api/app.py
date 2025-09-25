# Flask app factory


from flask import Flask
from clustersense.api.routes import api_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix="/api")

    # heartbeat ❤️ of mu app:
    # Defines a simple health check endpoint: GET /health.
	# Useful for monitoring, CI/CD, or Kubernetes to check if the service is running.
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

# optional manual run:
# if __name__ == "__main__":
#     app = create_app()
#     app.run(host="0.0.0.0", port=8000, debug=True)