# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences



import pickle

from spellchecker import SpellChecker


def prepare_review(review):
    review = review.strip()
    review = review.lower()
    def remove_punc(review):
        punctuations = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~0123456789'
        return review.translate(str.maketrans('', '', punctuations))
    
    review = remove_punc(review)
    
    spell = SpellChecker()
    def correct_spelling(review):
        corrected_review = []
        misspelled_words = spell.unknown(review.split())
        for word in review.split():
            if word in misspelled_words:
                corrected_review.append(spell.correction(word))
            else:
                corrected_review.append(word)
        return " ".join(corrected_review)
    
    review = correct_spelling(review)


    common_words = ['the', 'and', 'a', 'i', 'is', 'to', 'it', 'this', 'of','was', 'in',
                    'for', 'that', 'with', 'my', 'on', 'you', 'but', 'have', 'are', 'as',
                    'its', 'be', 'had', 'at', 'were', 'there', 'an', 'if', 'from', 'they',
                    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
                    "you're", "you've", "you'll", "you'd", 'your', 'yours','yourself',
                    'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
                    'hers', 'herself', 'it', "it's", 'its','itself', 'they', 'them',
                    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
                    'this', 'that', "that'll", 'these','those', 'am', 'is', 'are', 'was',
                    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
                    'does', 'did','doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
                    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with','about',
                    'against', 'between', 'into', 'through', 'during', 'before', 'after',
                    'to', 'from', 'again', 'further', 'then', 'once', 'here', 'there',
                    'when', 'where', 'why', 'how', 'both', 'each','other', 'some', 'such',
                    'own', 'same', 'so','than','s', 't', 'can', 'will', 'just', 'now',
                    'd', 'll', 'm', 'o', 're', 've', 'y']

    remove_words = set([word for word in common_words])
    
    def remove_common_words(review):
        return " ".join([word for word in str(review).split() if word not in remove_words])

    review = remove_common_words(review)
    
    
    
    return [review]


#Function to predict example reviews
def predict_review(model, review):
    
    # Create the sequences
    padding_type='post'
    max_length = 30
    sample_sequences = tokenizer.texts_to_sequences(review)
    review_padded = pad_sequences(sample_sequences, padding=padding_type, maxlen=max_length)           
             
    classes = model.predict(review_padded)

    for x in range(len(review_padded)):
        print('Review: {}'.format(review[x]))
        print('The sentiment analysis for this review is:')
        print('\n')
        if abs(classes[x][0] - 0) > abs(classes[x][0] - 1):
            print('{:.2f}% Positive'.format(classes[x][0] * 100))
            print('{:.2f}% Negative'.format((1 - classes[x][0]) * 100))
        else:
            print('{:.2f}% Positive'.format(classes[x][0] * 100))
            print('{:.2f}% Negative'.format((1 - classes[x][0]) * 100))





if __name__ == '__main__':
    # loading tokenizer
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    nlp_model = keras.models.load_model('final_nlp_model')
    print('------Write your review------')
    predict_review(nlp_model, prepare_review(input()))