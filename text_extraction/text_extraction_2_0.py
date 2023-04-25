import textract
import os
import sys
import io
import nltk
import spacy
from transformers import AutoTokenizer, pipeline
from Data_Derby_Hackathon import aip_func

# Download required NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('treebank')

# Load SpaCy model
nlp = spacy.load('en_core_web_lg')

output_filename = 'results.txt'


def extract_text(file_path):
    """Extract text from a file using textract."""
    try:
        text = textract.process(file_path)
        return text.decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None


def extract_pdf(file_path):
    """Extract text from a PDF file using textract."""
    try:
        text = textract.process(file_path, method='tesseract', language='eng')
        return text.decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None


def print_transformers(extracted_text):
    """Print named entities using transformers."""
    output = io.StringIO()
    with open(output_filename, 'a') as file:
        print("\n-----------------TRANSFORMERS-----------------\n", file=output)
        classifier = pipeline(task="ner")
        preds = classifier(extracted_text)
        print(*preds, file=output, sep="\n")
        output_string = output.getvalue()
        file.write(output_string)


def print_nltk(extracted_text):
    """Print named entities using NLTK."""
    output = io.StringIO()
    with open(output_filename, 'a') as file:
        print("\n-----------------NLTK-----------------\n", file=output)
        tokens = nltk.word_tokenize(extracted_text)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)
        print(entities, file=output)
        output_string = output.getvalue()
        file.write(output_string)


def print_nlp(extracted_text):
    """Print named entities using SpaCy."""
    output = io.StringIO()
    with open(output_filename, 'a') as file:
        print("\n-----------------NLP-----------------\n", file=output)
        doc = nlp(extracted_text)
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_, file=output)
        output_string = output.getvalue()
        file.write(output_string)


def main():
    if len(sys.argv) < 2:
        print("Usage: python text_extractor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    test_function()

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    if os.path.exists(output_filename):
        os.remove(output_filename)
    else:
        print("The file does not exist")

    # Extract text from file
    if '.txt' in file_path:
        extracted_text = extract_text(file_path)
    elif '.pdf' in file_path:
        extracted_text = extract_pdf(file_path)

    # Print extracted text and named entities
    print("\n-----------------EXTRACTED TEXT-----------------\n")
    if extracted_text:
        print("Extracted text:")
        print(extracted_text)
    else:
        print("Failed to extract text.")

    print_nlp(extracted_text)
    print_nltk(extracted_text)
    print_transformers(extracted_text)

    aip_func(extracted_text)


if __name__ == "__main__":
    main()

def process_chromadb():
    MAX_LENGTH_FOR_INPUT = 512
    pieces = len(extracted_text) / MAX_LENGTH_FOR_INPUT
    piece = extracted_text[0:512]
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    encoded_input = tokenizer(piece)
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="db"
    ))

    if client.get_collection("documentation"):
        client.delete_collection("documentation")

    collection=client.create_collection("documentation")

    ids = []
    documents = []

    documents.append(extracted_text)
    ids.append("my-document")

    collection.add(
        documents=documents,
        ids=ids
    )

    client.persist()

    collection=client.get_collection("documentation")
    docs=collection.get(include=["documents"])