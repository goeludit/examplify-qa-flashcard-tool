from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import ast, re 





def convert_text_to_list_of_dicts(text):
    """
    Converts a string representation of a list of dictionaries into a Python list of dictionaries.
    
    Args:
        text (str): A string representation of a list of dictionaries.
        
    Returns:
        list: A Python list of dictionaries.
    """
    try:
        # Safely evaluate the string to convert it into a Python object
        list_of_dicts = ast.literal_eval(text.strip())

        if isinstance(list_of_dicts, list):
            return list_of_dicts
        else:
            raise ValueError("Input text does not represent a list of dictionaries.")
    except Exception as e:
        raise ValueError(f"Error in converting text to list of dictionaries: {e}")


def write_questions_to_pdf(questions, output_filename):
    """
    Write quiz questions to a PDF.
    
    Args:
    - questions (list of dict): List of questions with options and answers.
    - output_filename (str): The name of the output PDF file.
    
    Returns:
    - None
    """
    questions = convert_text_to_list_of_dicts(str(questions))
    # Initialize the PDF
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    margin = 50
    line_height = 14
    current_y = height - margin
    
    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, current_y, "Quiz Questions")
    current_y -= line_height * 2
    
    # Set body font
    c.setFont("Helvetica", 10)
    
    # Write each question to the PDF
    for idx, item in enumerate(questions, 1):
        question_text = f"{idx}. {item['question']}"
        options_text = item['options']
        answer_text = f"Answer: {item['answer']}"
        
        # Check if we need a new page
        if current_y <= margin + 4 * line_height:
            c.showPage()
            c.setFont("Helvetica", 10)
            current_y = height - margin
        
        # Write the question
        c.drawString(margin, current_y, question_text)
        current_y -= line_height
        
        # Write the options
        for opt_idx, option in enumerate(options_text, 1):
            c.drawString(margin + 20, current_y, f"{opt_idx}. {option}")
            current_y -= line_height
        
        # Write the answer
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(margin + 20, current_y, answer_text)
        c.setFont("Helvetica", 10)
        current_y -= line_height * 2  # Add extra spacing after each question
    
    # Save the PDF
    c.save()



pdf = """
[
    {
        "question": "What is the initial loss value for the Modified SQuAD 2.0 dataset?",
        "answer": "approximately 2.6",
        "options": ["1.5", "2.6", "3.8", "4.9"]
    },
    {
        "question": "How quickly does the fine-tuning loss drop below 1.0 using our custom dataset?",
        "answer": "within the first 20 steps",
        "options": ["before step 10", "between steps 10 and 50", "during the first 100 steps", "after step 200"]
    },
    {
        "question": "What is the primary approach used for fine-tuning?",
        "answer": "two-pronged approach (4-bit quantization + QLoRA framework)",
        "options": ["4-bit quantization only", "QLoRA framework only", "unsupervised learning only", "reinforcement learning"]
    },
    {
        "question": "What is the optimal balance between performance and efficiency for fine-tuning?",
        "answer": "learning rate of 1e-4 and 100 steps",
        "options": ["learning rate of 1e-3 and 50 steps", "learning rate of 2e-6 and 500 steps", "learning rate of 5e-5 and 2000 steps"]
    },
    {
        "question": "What is the key metric that measures the relevance of the top three retrieved results?",
        "answer": "Precision@3",
        "options": ["F1 score only", "Accuracy only", "Precision@2, Precision@3, F1 score"]
    }
]
"""

# print(write_questions_to_pdf(convert_text_to_list_of_dicts(pdf),"sample.pdf"))