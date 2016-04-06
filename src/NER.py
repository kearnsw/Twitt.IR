import ner
from nltk.tag import StanfordNERTagger

stanford_ner_dir = '/home/will/packages/stanfordNER/'
eng_model_filename = stanford_ner_dir + 'classifiers/english.all.3class.distsim.crf.ser.gz'
my_path_to_jar = stanford_ner_dir + 'stanford-ner.jar'

st = StanfordNERTagger(model_filename=eng_model_filename, path_to_jar=my_path_to_jar)
st.tag('Rami Eid is studying at Stony Brook University in NY'.split())

# tagger = ner.HttpNER(host='localhost', port=8080)
# tagger.get_entities("University of California is located in California, United States")
