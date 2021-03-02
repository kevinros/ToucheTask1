# methods to load any necessary data files
import xml.etree.ElementTree as ElementTree
import processor

def load_relevance_scores(path):
    """
    Loads the relevance scores
    :param path: path to relevance score text file
    :type path: str 
    :rtype: dict
    :return: dict where keys are the topics and values are (doc,score) tuples 
    """
    with open(path, 'r') as f:
        relevance_scores = {}
        for line in f:
            line = line.strip().split()
            # line[0] is the topic number
            # line[2] is the docId
            # line[3] is the relevance score, note that this is cast to a float for future computation
            if line[0] not in relevance_scores:
                relevance_scores[line[0]] = {}
                relevance_scores[line[0]][line[2]] = float(line[3])
            else:
                relevance_scores[line[0]][line[2]] = float(line[3])
        return relevance_scores

def load_topics(path, onlyTitles=True):
    """
    Loads the topics
    :param path: path to topic text file
    :type path: str
    :param onlyTitles: true if xml file has only titles, false otherwise, default true
    :type onlyTitles: bool
    :rtype: dict
    :return: dict where keys are the topics and values are the titles,descriptions, etc.
    """

    topics = {}
    with open(path, 'r') as f:
        xml = f.read()

    root = ElementTree.fromstring(xml)
    for topic in root:
        topic_num = topic.find('number').text.strip()
        topics[topic_num] = {}
        topics[topic_num]['title'] = topic.find('title').text.strip()
        if not onlyTitles:
            topics[topic_num]['description'] = topic.find('description').text.strip() 
            topics[topic_num]['narrative'] = topic.find('narrative').text.strip()
        
    return topics
        

    
