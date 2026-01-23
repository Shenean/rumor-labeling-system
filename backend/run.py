import os

from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('BACKEND_PORT') or os.environ.get('PORT') or 5000)
    app.run(debug=True, port=port)
