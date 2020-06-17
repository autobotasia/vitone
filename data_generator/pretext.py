from tqdm import tqdm
from vncorenlp import VnCoreNLP
import random as rd
import pickle


def analyse_data(corpus_path):

    try:

        vncorenlp_file = r'./VnCoreNLP/VnCoreNLP-1.1.1.jar'
        vncorenlp = VnCoreNLP(vncorenlp_file)
        print('Create VNCoreNLP Object.')

        fi = open(corpus_path, 'r')
        fo_token = open(corpus_path + '-token', 'w')
        fo_pos_tag = open(corpus_path + '-postag', 'w')
        fo_ner = open(corpus_path + '-ner', 'w')
        fo_dep_parse = open(corpus_path + '-dep-parse', 'w')
        fo_anno = open(corpus_path + '-anno', 'w')

        print("Open %s" % corpus_path)
        print("Open %s" % fo_token)
        print("Open %s" % fo_pos_tag)
        print("Open %s" % fo_ner)
        print("Open %s" % fo_dep_parse)
        print("Open %s" % fo_anno)

        line_number = 0
        for line in fi:
            line_number +=1
        fi.close()
        fi = open(corpus_path, 'r')
        print('We have %d in our corpus.' % line_number)

        for count in tqdm(range(line_number)):

            sentences = fi.readline()
            fo_token.write(str(vncorenlp.tokenize(sentences)) + '\n')
            fo_pos_tag.write(str(vncorenlp.pos_tag(sentences)) + '\n')
            fo_ner.write(str(vncorenlp.ner(sentences)) + '\n')
            fo_dep_parse.write(str(vncorenlp.dep_parse(sentences)) + '\n')
            fo_anno.write(str(vncorenlp.annotate(sentences)) + '\n')

        print('Finish analysis data.')

    except Exception as e:
        raise
    finally:
        fi.close()
        fo_token.close()
        fo_pos_tag.close()
        fo_ner.close()
        fo_dep_parse.close()
        fo_anno.close()

        print("Close %s" % corpus_path)
        print("Close %s" % fo_token)
        print("Close %s" % fo_pos_tag)
        print("Close %s" % fo_ner)
        print("Close %s" % fo_dep_parse)
        print("Close %s" % fo_anno)


def random_select_sentence_for_create_error_sentences(fi_path, fo_path):

    try:
        print("fi path:\t" + fi_path)
        print("fo path:\t" + fo_path)
        fi = open(fi_path, 'r')
        fo = open(fo_path, 'w')

        fo_line_index = fo_path + '_line_index'
        print("fo_line_index:\t" + fo_line_index)
        line_number = 0
        for line in fi:
            line_number +=1
        fi.close()
        fi = open(corpus_path, 'r')
        print('we have %d lines in corpus.' % line_number)

        line_index = []
        for count in tqdm(range(line_number)):
            sentence = fi.readline()
            choose = rd.randint(1, 20)
            if choose == 1:
                fo.write(sentence)
                line_index.append(count)

        # see line index (in corpus) in terminal
        s = []
        for i in range(len(line_index)):
            s.append(str(line_index[i]))
            if i % 10 == 9:
                print('\t'.join(s))

        # save line index
        pickle.dump(line_index, fo_line_index)
        fo_line_index.close()
        fo.close()

    except IOError:
        print("IO Exception.")
    finally:
        fi.close()
        fo.close()
