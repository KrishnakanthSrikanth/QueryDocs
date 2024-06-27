# Import Dependencies
import os
import PyPDF2
import nltk
import re
from pdf2image import convert_from_path
import pytesseract
import pandas as pd
from sentence_transformers import util

# PyPDF 2 Parser
def parser_pypdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_number in range(num_pages):
            page = reader.pages[page_number]
            page_text = page.extract_text()
            text += page_text
            # Yielding page number and text of each page
            yield page_number + 1, page_text

    # return text

# ==========================================================================================

# OCR PDF Reader.
def parser_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = ""

    for image in images:
        text = pytesseract.image_to_string(image, lang='eng')
        extracted_text += text

    return extracted_text

# ==========================================================================================

# Function to split document into sentences
def get_sentences(text):

    sentences = nltk.sent_tokenize(text)
    return sentences

# ==========================================================================================

# Function to perform text formatting operations on a list of sentences
def sentence_formatter(sentences):

    formatted_sentences = []

    for sentence in sentences:
        sentence = sentence.replace('\n', ' ')
        sentence = sentence.strip()
        sentence = re.sub(r'\s+', ' ', sentence)

        # Skip sentences with more than 85 words
        if len(sentence.split(" ")) > 85:
            continue
        
        if len(sentence.split(" ")) < 4:
            continue

        # Join fragmented sentences
        if len(formatted_sentences) > 0 and not sentence[0].isupper():
            formatted_sentences[-1] += ' ' + sentence
        else:
            formatted_sentences.append(sentence)

    return formatted_sentences


def sentence_parser(pdf_file_path, print_sentences=False, num_sentences=5, parsing_method="pypdf"):

    # Check if file exists
    if not os.path.exists(pdf_file_path):
        print("Error: PDF file not found.")
        return

    # Extract text from the PDF based on the parsing method chosen
    if parsing_method == "pypdf":
        parsed_sentences = list(parser_pypdf(pdf_file_path))  # Convert generator to list
    elif parsing_method == "ocr":
        parsed_sentences = [(1, parser_ocr(pdf_file_path))]  # For OCR, assume all text belongs to the first page
    else:
        print("Error: Invalid parsing method specified.")
        return

    sentences_with_metadata = []
    for page_number, page_text in parsed_sentences:
        sentences = get_sentences(page_text)
        sentences = sentence_formatter(sentences)
        for sentence in sentences:
            sentences_with_metadata.append({
                'Page': page_number,
                'Filename': os.path.basename(pdf_file_path),
                'Sentence': sentence
            })

    # Summary of the number of sentences
    num_total_sentences = len(sentences_with_metadata)
    print("\nSummary:")
    print("Total number of sentences:", num_total_sentences)

    # Print the first n formatted sentences if required
    if print_sentences:
        if num_sentences > 0:
            for idx, item in enumerate(sentences_with_metadata[:num_sentences]):
                print('\n', f"Page: {item['Page']}, Filename: {item['Filename']}", item['Sentence'])
        else:
            for idx, item in enumerate(sentences_with_metadata):
                print('\n', f"Page: {item['Page']}, Filename: {item['Filename']}", item['Sentence'])

    return sentences_with_metadata

# ==========================================================================================

def compute_similarity_v2(model, query, pdf_sentences):
    
    # Create Embeddings for query
    query_embedding = model.encode(query)

    # Create Embeddings for retrieved sentences
    sentence_embedding = model.encode(pdf_sentences)

    # Compute similarity scores
    scores = util.cos_sim(query_embedding, sentence_embedding)[0]

    # Create a DataFrame
    df = pd.DataFrame({
        'Sentence_ID': range(1, len(pdf_sentences) + 1),
        'Sentence': pdf_sentences,
        'Score': scores.tolist()
    })

    # Sort DataFrame by similarity scores in descending order
    sorted_df = df.sort_values(by='Score', ascending=False)

    return sorted_df

# ==========================================================================================

def save_similarity_results(sorted_df, file_name='sorted_results.csv'):

    # Get the user's home directory
    home_directory = os.path.expanduser("~")

    # Depending on the operating system, navigate to the downloads folder
    if os.name == 'posix':  # Unix-based systems including macOS
        downloads_folder = os.path.join(home_directory, 'Downloads')
    elif os.name == 'nt':  # Windows
        downloads_folder = os.path.join(home_directory, 'Downloads')
    else:
        # Handle other operating systems if necessary
        raise NotImplementedError("Operating system not supported")

    # Specify the file path for the CSV file
    csv_file_path = os.path.join(downloads_folder, file_name)

    # Save the sorted DataFrame to the CSV file in the downloads folder
    sorted_df.to_csv(csv_file_path, index=False)

# ==========================================================================================