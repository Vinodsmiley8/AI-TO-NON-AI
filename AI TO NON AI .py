import os
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

# Function to detect encoding and read file
def read_file_with_encoding(file_path):
    with open(file_path, 'rb') as raw_file:
        result = chardet.detect(raw_file.read())
        encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
        return file.read()

# Function to process all .txt files in a folder
def process_all_txt_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt") and not filename.endswith("_processed.txt"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, filename.replace(".txt", "_processed.txt"))
            
            print(f"📄 Processing: {filename}")
            try:
                input_text = read_file_with_encoding(input_path)
                processed_text = process_text(input_text)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(processed_text)
                print(f"✅ Saved to: {output_path}\n")
            except Exception as e:
                print(f"❌ Failed to process {filename}: {e}\n")

# Example usage
if __name__ == "__main__":
    folder_path = "."  # Change to your folder if needed, or use input()
    process_all_txt_files_in_folder(folder_path)
