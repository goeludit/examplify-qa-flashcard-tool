import PyPDF2
import os

def pdf_to_text(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Initialize a variable to store extracted text
        text = ""
        
        # Loop through each page and extract text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        
    return text

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(text)

# Specify the input PDF file and output text file
pdf_path = "/home/udit/Desktop/Projects/examplify-qa-tool/data/PrinciplesofMicroeconomics-OP-custom.pdf"  # Replace with your PDF file path
output_path = "output_text.txt"  # Replace with desired output text file path


def process_multiple_pdfs(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            
            # Extract text from PDF
            pdf_text = pdf_to_text(pdf_path)
            
            # Save the text to a file
            save_text_to_file(pdf_text, output_path)



# Specify the input folder containing PDF files and the output folder for text files
input_folder = "//home/udit/Desktop/Projects/examplify-qa-tool/training_data_pdf"  # Replace with your input folder path
output_folder = "/home/udit/Desktop/Projects/examplify-qa-tool/training_data_text"  # Replace with your output folder path

# Process all PDF files in the input folder
process_multiple_pdfs(input_folder, output_folder)

# # Extract text from PDF
# pdf_text = pdf_to_text(pdf_path)

# # Optionally, save the text to a file
# save_text_to_file(pdf_text, output_path)

print("Text extraction completed and saved to:", output_path)
