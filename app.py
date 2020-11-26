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
    
    return [review]


#Function to predict example reviews
def predict_review(model, review):
    
    # Create the sequences
    padding_type='post'
    max_length = 50
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