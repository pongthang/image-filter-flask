## display the images as form
## drop down menu for selecting clothses and view
## next button to go to next view
## show progress


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data
images = {
    "image_0": {
        "view": "front",
        "name": "5715512990538_1_first_pass_0001.png",
        "path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0001.png",
        "ori_name": "5715512990538",
        "ori_path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
        "vote": 0,
        "key": "image_0"
    },
    "image_1": {
        "view": "front",
        "name": "5715512990538_1_first_pass_0002.png",
        "path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0002.png",
        "ori_name": "5715512990538",
        "ori_path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
        "vote": 0,
        "key": "image_1"
    },
    "image_2": {
        "view": "front",
        "name": "5715512990538_1_first_pass_0003.png",
        "path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/generated_first_pass/5715512990538/5715512990538_1_first_pass_0003.png",
        "ori_name": "5715512990538",
        "ori_path": "/home/miko/Documents/personal/Faishme/image-filter-flask/images/original_image_folder/5715512990538/5715512990538_1.jpg",
        "vote": 0,
        "key": "image_2"
    }
}

@app.route('/')
def index():
    return render_template('index.html', images=images)

@app.route('/vote', methods=['POST'])
def vote():
    image_id = request.form.get('image_id')
    action = request.form.get('action')
    
    if image_id in images:
        if action == "up":
            images[image_id]['vote'] += 1
        elif action == "down":
            images[image_id]['vote'] -= 1
        return jsonify({"vote": images[image_id]['vote']})
    
    return jsonify({"error": "Invalid image ID"}), 400

if __name__ == '__main__':
    app.run(debug=True)
