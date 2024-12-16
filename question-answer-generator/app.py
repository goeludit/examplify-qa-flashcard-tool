from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from claude_ollama import generate_text
from parse_text_pdf import write_questions_to_pdf
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/generate_test', methods=['POST'])
def generate_test():
    test_name = request.form.get('test_name')
    test_type = request.form.get('test_type')
    test_level = request.form.get('test_level')

    num_questions = request.form.get('num_questions')
    file = request.files['file']

    if file and file.filename != '':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        quiz_questions_chunk =  generate_text(filepath, num_questions, test_level, test_type)
        print(quiz_questions_chunk)
        write_questions_to_pdf(quiz_questions_chunk, f"{test_name}.pdf")
        pdf_gen_path =  f"{test_name}.pdf"
        print(pdf_gen_path)
        # return render_template('pdf_view.html', test_name=pdf_gen_path)
        return send_file(
            pdf_gen_path,
            as_attachment=True,
            mimetype="application/pdf"
        )

    else:
        return "No file uploaded or invalid file!"

# def get_test_name():
#     test_name = request.form.get('test_name')
#     return test_name


# def get_test_type():
#     test_type = request.form.get('test_type')
#     return test_type

# def get_numer_questions():
#     num_questions = request.form.get('num_questions')
#     return num_questions


if __name__ == '__main__':
    app.run(debug=True)
