from TSPpy import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print("Running from wsgi on", port)
    app.run(debug=True, host='0.0.0.0', port=port)