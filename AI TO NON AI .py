import nltk
import random
import chardet
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet, stopwords
import language_tool_python

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Initialize LanguageTool for grammar checking
grammar_tool = language_tool_python.LanguageTool('en-US')

# Get stopwords
stop_words = set(stopwords.words('english'))

# Function to get synonyms for a word
def get_synonyms(word):
    if word.lower() in stop_words:
        return [word]
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower():
                synonyms.add(name)
    return list(synonyms) or [word]

# Function to replace words with synonyms
def replace_with_synonyms(text):
    words = word_tokenize(text)
    modified_words = []
    for word in words:
        synonyms = get_synonyms(word)
        modified_words.append(random.choice(synonyms))
    return " ".join(modified_words)

# Function to correct grammar
def correct_grammar(text):
    matches = grammar_tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

# Function to enhance the text: synonym replacement and grammar correction
def enhance_text(text):
    modified_text = replace_with_synonyms(text)
    corrected_text = correct_grammar(modified_text)
    return corrected_text

# Function to process text and make it "anti-AI-detectable"
def process_text(input_text):
    sentences = input_text.splitlines()
    enhanced_sentences = [enhance_text(sentence) for sentence in sentences]
    enhanced_text = "\n".join(enhanced_sentences)
    return enhanced_text

# Function to read text from a file, process it, and save to a new file
def process_file(input_file_path, output_file_path):
    # Detect encoding using chardet
    with open(input_file_path, 'rb') as raw_file:
        result = chardet.detect(raw_file.read())
        detected_encoding = result['encoding']
        print(f"Detected encoding: {detected_encoding}")

    # Read the input file
    with open(input_file_path, 'r', encoding=detected_encoding, errors='ignore') as file:
        input_text = file.read()

    # Process the text
    output_text = process_text(input_text)

    # Write the processed text to an output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(output_text)

    print(f"✅ Processed text has been saved to: {output_file_path}")

# Example usage
if __name__ == "__main__":
    # Set the input and output file paths
    input_file_path = 'What is data mining.txt'  # Change if needed
    output_file_path = input_file_path.replace('.txt', '_processed.txt')

    # Process the file
    process_file(input_file_path, output_file_path)
