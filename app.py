from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def gallery():
    images = get_all_files_in_dir(os_dir_join_args=['static'],
                                  file_filter='.jpg')
    return render_template('index.html', title="Gallery", images=images)

def get_all_files_in_dir(os_dir_join_args, file_filter=None):
    dir = os.path.join(*os_dir_join_args)
    files = os.listdir(path=dir)
    if file_filter:
        files = [os.path.join(dir, file)
                 for file in files if file.find(file_filter) >= 0]
    return files

if __name__ == "__main__":
    app.run(debug=True)