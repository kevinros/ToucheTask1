# helper methods for processing text
import sys
import spacy
import re


# Use directions from https://spacy.io/usage/models
nlp = spacy.load("en_core_web_sm")

def tokenizeWordSpacy(text, removePunct=True, lower=True, minLength=2):
    """
    Uses spacy model to process and return list of words
    :param text: text to be processed
    :type text: str
    :param removePunct: removes punctuation if true, keeps it if false
    :type removePunct: bool
    :param lower: lowercases text if true
    :type lower: bool
    :param minLength: minimum token length to keep
    :type minLength: int

    :rtype: list of str
    :returns: list of processed words
    """
    if removePunct:
        text = re.sub(r'\W+', ' ', text)
    if lower:
        text = text.lower()
    doc = nlp(text)
    words = [token.text for token in doc if len(token.text) > min_length]
    return words

def tokenizeSentenceSpacy(text):
    """
    Uses spacy model to extract sentences from the text
    :param text: text to be processed
    :type text: str

    :rtype: list of strings
    :returns: list of sentences
    """
    doc = nlp(text)
    sentences = [sent.string.strip() for sent in doc.sents]
    return sentences

def createSentences(text):
    """
    Sometimes, spacy is too slow so this is a faster version of sentence tokenization.
    Note that it isn't robust, and many params are hardcoded. 

    :param text: text to be processed
    :type text: str

    :rtype: list of strings
    :returns: list of sentences
    """
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(|Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Za-z][.][A-Za-z][.](?:[A-Za-z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    
    text = " " + text + "  "
    text = text.replace("\n"," ")

    text = re.sub("=*=", ". ", text) 
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "" in text: text = text.replace(".",".")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [re.sub(' +', ' ', sentence).strip() for sentence in sentences]

    sentences = [s for s in sentences if len(s) > 20]
    return sentences
