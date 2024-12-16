from flask import Flask, render_template, request, redirect, url_for, jsonify, session  
import os
from claude_flashcard import generate_flashcards
# from parse_text_pdf import write_questions_to_pdf
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'    


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
@app.route('/', methods=['POST', 'GET'])
def home():
    print("route of home")
    return render_template('form.html')


@app.route('/upload', methods=['POST'])
def upload():
    # print(request.files)
    if 'pdf' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['pdf']
    if file.filename == '':
        return "No selected file", 400

    # Save the file (optional: customize the save path as needed)
    filename = file.filename
    print("fdfddf")
    file.save(f'uploads/{filename}')
    print("file name upload" + filename)
    # Redirect to a new page with the filename as a parameter
    session['seassion_filename'] = filename

    return redirect(url_for('flashcards_screen'))




@app.route('/generate_flashcard', methods=['GET', 'POST'])
def flashcards_screen():
    # my_file = request.args.get(my_file)
    my_file = session.get('seassion_filename', None)

    print("my_file")
    
    # print(my_file)
    # my_file_2 = request.args.get(my_file)
    my_file = "uploads/" + str(my_file)
    print("my_file:", my_file)

    generate_flashcard(my_file)
    return render_template('flashcards.html')




def generate_flashcard(filepath):

    # filepath = "NLP Presentation.pdf"
    # print(filepath)
    topics_list =  generate_flashcards(filepath)
    # print(topics_list)

    # print("")
    return jsonify(topics_list) 

if __name__ == '__main__':
    app.run(debug=True)
