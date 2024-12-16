from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
from nltk.translate.meteor_score import meteor_score
from rouge import Rouge

# Evaluation for Question-Answer Generation
def evaluate_question_answer(true_labels, pred_labels, k=3):
    """
    Evaluate Precision, Recall, and Accuracy for Question-Answer Generation.
    """
    precision = precision_score(true_labels, pred_labels, average='micro')
    recall = recall_score(true_labels, pred_labels, average='micro')
    accuracy = accuracy_score(true_labels, pred_labels)
    f1 = f1_score(true_labels, pred_labels, average='micro')

    print(f"Precision@{k}: {precision:.2f}")
    print(f"Recall@{k}: {recall:.2f}")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"F1 Score: {f1:.2f}")

# Evaluation for Text Summarization (Flashcards)
def evaluate_flashcards(true_summaries, pred_summaries):
    """
    Evaluate ROUGE, METEOR, and F1 score for text summarization.
    """
    rouge = Rouge()
    scores = rouge.get_scores(pred_summaries, true_summaries, avg=True)

    rouge_1 = scores['rouge-1']['f']
    rouge_2 = scores['rouge-2']['f']
    rouge_l = scores['rouge-l']['f']
    
    meteor_scores = [meteor_score([true], pred) for true, pred in zip(true_summaries, pred_summaries)]
    avg_meteor = sum(meteor_scores) / len(meteor_scores)

    f1 = f1_score(true_summaries, pred_summaries, average='micro')

    print(f"ROUGE-1: {rouge_1:.2f}")
    print(f"ROUGE-2: {rouge_2:.2f}")
    print(f"ROUGE-L: {rouge_l:.2f}")
    print(f"METEOR: {avg_meteor:.2f}")
    print(f"F1 Score: {f1:.2f}")

# Example Usage
# True labels and predictions for question-answer evaluation
true_labels_qa = [
    int(input("Enter true label 1 for QA: ")),
    int(input("Enter true label 2 for QA: ")),
    int(input("Enter true label 3 for QA: ")),
    int(input("Enter true label 4 for QA: ")),
    int(input("Enter true label 5 for QA: "))
]
pred_labels_qa = [
    int(input("Enter predicted label 1 for QA: ")),
    int(input("Enter predicted label 2 for QA: ")),
    int(input("Enter predicted label 3 for QA: ")),
    int(input("Enter predicted label 4 for QA: ")),
    int(input("Enter predicted label 5 for QA: "))
]
evaluate_question_answer(true_labels_qa, pred_labels_qa, k=3)

# True summaries and predicted summaries for text summarization
def preprocess_text(text):
    """Preprocess text by tokenizing and normalizing."""
    return text.lower()

true_summaries = [
    input("Enter the true summary 1: "),
    input("Enter the true summary 2: ")
]
pred_summaries = [
    input("Enter the predicted summary 1: "),
    input("Enter the predicted summary 2: ")
]
evaluate_flashcards([preprocess_text(x) for x in true_summaries],
                    [preprocess_text(x) for x in pred_summaries])