from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# Sample images data
images = {
    "image_0": {
        "view": "front",
        "name": "5715512990538_1_first_pass_0001.png",
        "path": "~/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0001.png",
        "ori_name": "5715512990538",
        "ori_path": "~/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
        "vote": 0,
        "key": "image_0"
    },
    "image_1": {
        "view": "front",
        "name": "5715512990538_1_first_pass_0002.png",
        "path": "~/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0002.png",
        "ori_name": "5715512990538",
        "ori_path": "~/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
        "vote": 0,
        "key": "image_1"
    },
    "image_2": {
        "view": "front",
        "name": "5715512990538_1_first_pass_0003.png",
        "path": "~/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0003.png",
        "ori_name": "5715512990538",
        "ori_path": "~/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
        "vote": 0,
        "key": "image_2"
    }
}

@app.route('/')
def index():
    return render_template('index.html', images=images.values())

@app.route('/vote', methods=['POST'])
def vote():
    updates = request.get_json()
    response_data = {}
    for key, delta in updates.items():
        if key in images:
            images[key]['vote'] += delta
            response_data[key] = images[key]['vote']
    return jsonify(response_data)


# Routes to serve images
@app.route('/original_images/<path:filename>')
def serve_original(filename):
    base_dir = '~/Documents/personal/Faishme/image-filter-flask/images/original_image_folder'
    return send_from_directory(base_dir, filename)

@app.route('/generated_images/<path:filename>')
def serve_generated(filename):
    base_dir = '~/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass'
    return send_from_directory(base_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)