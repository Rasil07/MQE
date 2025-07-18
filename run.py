from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv('FLASK_CONFIG')

app = create_app(env)



def find_template_files():
    extra_files = []
    for dirname, _, filenames in os.walk(os.path.join('app', 'templates')):
        for filename in filenames:
            if filename.endswith('.html'):
                extra_files.append(os.path.join(dirname, filename))
    return extra_files


if __name__ == '__main__':
    extra_files = find_template_files()
    print("Watching these files:", extra_files)
    app.run(debug=(env == 'development'), extra_files=extra_files, use_reloader=True)
    