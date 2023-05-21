from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

app = Flask(__name__)

# قواميس الوثائق
dataset1 = {
    1: 'This is document 1',
    2: 'Another document here',
    3: 'Some more text in document 3'
}

dataset2 = {
    4: 'Document number 4',
    5: 'Text in document 5',
    6: 'Yet another document',
    7:"yet lsnvlnlsndv",
    8:"yetasvsdvsdv",
    9:"yet svdlknlsdv",
    10:"yet aslvknapikanslcknalknSKNDVLNLKNSVD",
    11:"yet",
    12:"yetSDVSD;VKNSV",
    13:"yet",
    14:"yet SALDVKNSV",
    15:"yet",
    16:"yet SVDLM",
    17:"yet",
    18:"yet",
    19:"yet",
    20:"yet",
    21:"yet",
    22:"yet",
    23:"yet",
    24:"yet",
    25:"yet",
    26:"yet",
    27:"yet",
    28:"yet",
    29:"yet",
    30:"yet",
    31:"yet",
    32:"yet",
}

# بناء الفهرس
index = {}
for doc_id, document in dataset1.items():
    words = document.lower().split()
    for word in words:
        if word not in index:
            index[word] = set()
        index[word].add(doc_id)

for doc_id, document in dataset2.items():
    words = document.lower().split()
    for word in words:
        if word not in index:
            index[word] = set()
        index[word].add(doc_id)

# دالة البحث
def search(query, selected_dataset):
    query_words = query.lower().split()
    result = set()
    dataset = dataset1 if selected_dataset == 'dataset1' else dataset2
    for doc_id, document in dataset.items():
        words = document.lower().split()
        for word in query_words:
            if word in words:
                result.add(doc_id)
    return result

# تضليل الكلمة المبحوث عنها
def highlight_word(text, query):
    query_tokens = word_tokenize(query.lower())
    stemmed_query_tokens = [PorterStemmer().stem(token) for token in query_tokens]
    text_tokens = word_tokenize(text.lower())
    highlighted_tokens = []
    for token in text_tokens:
        stemmed_token = PorterStemmer().stem(token)
        if stemmed_token in stemmed_query_tokens:
            highlighted_tokens.append('<span class="highlight">' + token + '</span>')
        else:
            highlighted_tokens.append(token)
    highlighted_text = ' '.join(highlighted_tokens)
    return highlighted_text

# الصفحة الرئيسية للبحث
@app.route('/')
def home():
    return render_template('search.html')

# صفحة استرجاع النتائج
@app.route('/search', methods=['POST'])
def search_page():
    query = request.form['query']
    selected_dataset = request.form['selected_dataset']
    matching_documents = search(query, selected_dataset)
    documents = []
    dataset = dataset1 if selected_dataset == 'dataset1' else dataset2
    for doc_id in matching_documents:
        if doc_id in dataset:
            document = dataset[doc_id]
            highlighted_document = highlight_word(document, query)
            documents.append(highlighted_document)
    return render_template('results.html', query=query, documents=documents)

if __name__ == '__main__':
    app.run()

# ------------------------------------------------------------------------------------#

from flask import Flask, render_template, request
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import csv

app = Flask(__name__)

# Read the dataset from CSV
def read_dataset(file_path):
    dataset = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            dataset.append(row[0])  # Only store the document text
    return dataset

# Read dataset1
dataset1 = read_dataset('static/movie_review.csv')

# Read dataset2
dataset2 = read_dataset('static/realtor-data.csv')

# Build the index for dataset1
index1 = {}
for doc_id, document in enumerate(dataset1, start=1):
    words = document.lower().split()
    for word in words:
        if word not in index1:
            index1[word] = set()
        index1[word].add(doc_id)

# Build the index for dataset2
index2 = {}
for doc_id, document in enumerate(dataset2, start=len(dataset1) + 1):
    words = document.lower().split()
    for word in words:
        if word not in index2:
            index2[word] = set()
        index2[word].add(doc_id)

# Search function
def search(query, selected_dataset):
    query_words = query.lower().split()
    result = set()
    index = index1 if selected_dataset == 'dataset1' else index2
    for word in query_words:
        if word in index:
            result.update(index[word])
    return result

# Highlight the searched word
def highlight_word(text, query):
    query_tokens = word_tokenize(query.lower())
    stemmed_query_tokens = [PorterStemmer().stem(token) for token in query_tokens]
    text_tokens = word_tokenize(text.lower())
    highlighted_tokens = []
    for token in text_tokens:
        stemmed_token = PorterStemmer().stem(token)
        if stemmed_token in stemmed_query_tokens:
            highlighted_tokens.append('<span class="highlight">' + token + '</span>')
        else:
            highlighted_tokens.append(token)
    highlighted_text = ' '.join(highlighted_tokens)
    return highlighted_text

# Home page
@app.route('/')
def home():
    return render_template('search.html')

# Search results page
@app.route('/search', methods=['POST'])
def search_page():
    query = request.form['query']
    selected_dataset = request.form['selected_dataset']
    matching_documents = search(query, selected_dataset)
    documents = []
    dataset = dataset1 if selected_dataset == 'dataset1' else dataset2
    for doc_id, document in enumerate(dataset, start=1):
        if str(doc_id) in matching_documents:
            highlighted_document = highlight_word(document, query)
            documents.append(highlighted_document)
    return render_template('results.html', query=query, documents=documents)

if __name__ == '__main__':
    app.run()

#------------------------------------------------------------------------------------#

# from flask import Flask, render_template, request
# from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer
# import csv

# app = Flask(__name__)

# # Read the dataset from CSV
# def read_dataset(file_path):
#     dataset = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             dataset.append(row)
#     return dataset

# # Read the "movie_review" dataset
# dataset = read_dataset('static/movie_review.csv')

# # Build the index
# index = {}
# for row in dataset:
#     doc_id, document = row[0], row[2]
#     words = document.lower().split()
#     for word in words:
#         if word not in index:
#             index[word] = set()
#         index[word].add(doc_id)

# # Search function
# def search(query):
#     query_words = query.lower().split()
#     result = set()
#     for word in query_words:
#         if word in index:
#             result.update(index[word])
#     return result

# # Highlight the searched word
# def highlight_word(text, query):
#     query_tokens = word_tokenize(query.lower())
#     stemmed_query_tokens = [PorterStemmer().stem(token) for token in query_tokens]
#     text_tokens = word_tokenize(text.lower())
#     highlighted_tokens = []
#     for token in text_tokens:
#         stemmed_token = PorterStemmer().stem(token)
#         if stemmed_token in stemmed_query_tokens:
#             highlighted_tokens.append('<span class="highlight">' + token + '</span>')
#         else:
#             highlighted_tokens.append(token)
#     highlighted_text = ' '.join(highlighted_tokens)
#     return highlighted_text

# # Home page
# @app.route('/')
# def home():
#     return render_template('search.html')

# # Search results page
# @app.route('/search', methods=['POST'])
# def search_page():
#     query = request.form['query']
#     matching_documents = search(query)
#     documents = []
#     for row in dataset:
#         doc_id, document = row[0], row[2]
#         if doc_id in matching_documents:
#             highlighted_document = highlight_word(document, query)
#             documents.append(highlighted_document)
#     return render_template('results.html', query=query, documents=documents)

# if __name__ == '__main__':
#     app.run()
