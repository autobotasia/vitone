from tqdm import tqdm
from vncorenlp import VnCoreNLP
import random as rd
import pickle
import os
import re
import ast


def get_word_list(word_list_path):

    fi = open(word_list_path, 'r')
    print("Open file word_list at %s ." % word_list_path)
    word_list = [line.strip() for line in fi]
    fi.close()
    print("Close file word_list at %s ." % word_list_path)
    return word_list


def convert_list_to_string_type_paragraph(list_type_paragraph):

    temp_paragraph = []
    for list_type_sentence in list_type_paragraph:
        string_type_sentence = ' '.join(list_type_sentence)
        temp_paragraph.append(string_type_sentence)
    string_type_paragraph = ' '.join(temp_paragraph)

    return string_type_paragraph


def random_delete_words(paragraph):

    '''
    input pattern example (in error-sentences-token file):

    [['BS', '.'], ['CKI', 'Nguyễn_Tiến_Dũng', ',', 'Trưởng', 'khoa', 'Khám_chữa', 'bệnh', 'theo', 'yêu_cầu', ',', 'Trưởng', 'đơn_nguyên', 'Phẫu_thuật', 'thần_kinh', 'BVĐK', 'tỉnh', 'cho', 'biết', ':', 'Cháu', 'Trung', 'vào', 'viện', 'trong', 'tình_trạng', 'vô_cùng', 'nguy_kịch', ',', 'phẫu_thuật', 'xử_trí', 'các', 'tổn_thương', 'cần', 'cẩn_trọng', 'và', 'tuyệt_đối', 'chính_xác', '.']]

    pattern of return value same as input
    '''

    for i in range(len(paragraph)):

        sentence = paragraph[i]
        number_of_words_to_delete = rd.randint(1, len(sentence) // 2 + 1)
        index_of_random_words = set(rd.sample(range(len(sentence)), number_of_words_to_delete))
        new_sentence = []
        for j in range(len(sentence)):
            if j in index_of_random_words:
                continue
            new_sentence.append(sentence[j])
        paragraph[i] = new_sentence
    new_paragraph = []
    for element in paragraph:
        if len(element) != 0:
            new_paragraph.append(element)

    return new_paragraph


def random_swap_words_in_sentence(paragraph):

    '''
    input pattern example (in error-sentences-token file):
    [['BS', '.'], ['CKI', 'Nguyễn_Tiến_Dũng', ',', 'Trưởng', 'khoa', 'Khám_chữa', 'bệnh', 'theo', 'yêu_cầu', ',', 'Trưởng', 'đơn_nguyên', 'Phẫu_thuật', 'thần_kinh', 'BVĐK', 'tỉnh', 'cho', 'biết', ':', 'Cháu', 'Trung', 'vào', 'viện', 'trong', 'tình_trạng', 'vô_cùng', 'nguy_kịch', ',', 'phẫu_thuật', 'xử_trí', 'các', 'tổn_thương', 'cần', 'cẩn_trọng', 'và', 'tuyệt_đối', 'chính_xác', '.']]

    pattern of return value same as input
    '''
    assert type(paragraph) is list, "input of random_swap_words_in_sentence func should be 2D list of tokens"

    # print("choose paragraph of %s sentence to create error." % " ".join(paragraph[0]))
    for sentence in paragraph:
        number_of_words_for_swap_opr = len(sentence) // 6
        if number_of_words_for_swap_opr <= 1:
            continue
        word_indices = rd.sample(range(len(sentence)), number_of_words_for_swap_opr)
        if number_of_words_for_swap_opr == 2:
            # swap 2 words
            sentence[word_indices[0]], sentence[word_indices[1]] = sentence[word_indices[1]], sentence[word_indices[0]]
        else:
            code_str_list = []
            for index in word_indices:
                code_str_list.append("sentence[%d]," % index)

            code_str_list.append('=')
            rd.shuffle(word_indices)

            for index in word_indices:
                code_str_list.append("sentence[%d]," % index)
            code_str = ' '.join(code_str_list)
            exec(code_str)
    return paragraph


def random_swap_tokens_in_word(paragraph):

    '''
    input pattern example (in error-sentences-token file):
    [['BS', '.'], ['CKI', 'Nguyễn_Tiến_Dũng', ',', 'Trưởng', 'khoa', 'Khám_chữa', 'bệnh', 'theo', 'yêu_cầu', ',', 'Trưởng', 'đơn_nguyên', 'Phẫu_thuật', 'thần_kinh', 'BVĐK', 'tỉnh', 'cho', 'biết', ':', 'Cháu', 'Trung', 'vào', 'viện', 'trong', 'tình_trạng', 'vô_cùng', 'nguy_kịch', ',', 'phẫu_thuật', 'xử_trí', 'các', 'tổn_thương', 'cần', 'cẩn_trọng', 'và', 'tuyệt_đối', 'chính_xác', '.']]

    pattern of return value same as input
    '''

    assert type(paragraph) is list, "input of random_swap_words_in_sentence func should be 2D list of tokens"

    for sentence in paragraph:
        for i in range(len(sentence)):
            # sentence[i] = word
            is_multi_syllables = True if '_' in sentence[i] else False
            if is_multi_syllables:
                if rd.randint(1, 3) == 1:
                    syllables = sentence[i].split('_')
                    if len(syllables) == 2:
                        syllables[0], syllables[1] = syllables[1], syllables[0]
                    else:
                        rd.shuffle(syllables)
                    sentence[i] = '_'.join(syllables)

    return paragraph


def random_insert_word_to_sentence(paragraph, word_list):

    '''
    input pattern example (in error-sentences-token file):
    [['BS', '.'], ['CKI', 'Nguyễn_Tiến_Dũng', ',', 'Trưởng', 'khoa', 'Khám_chữa', 'bệnh', 'theo', 'yêu_cầu', ',', 'Trưởng', 'đơn_nguyên', 'Phẫu_thuật', 'thần_kinh', 'BVĐK', 'tỉnh', 'cho', 'biết', ':', 'Cháu', 'Trung', 'vào', 'viện', 'trong', 'tình_trạng', 'vô_cùng', 'nguy_kịch', ',', 'phẫu_thuật', 'xử_trí', 'các', 'tổn_thương', 'cần', 'cẩn_trọng', 'và', 'tuyệt_đối', 'chính_xác', '.']]

    pattern of return value same as input
    '''

    assert type(paragraph) is list, "input of random_swap_words_in_sentence func should be 2D list of tokens"

    for sentence in paragraph:

        number_of_word_for_insert = len(sentence) // 7
        words_for_insert = rd.sample(word_list, number_of_word_for_insert)
        indices_for_insert = rd.sample(range(len(sentence)), number_of_word_for_insert)

        for i in range(number_of_word_for_insert):
            sentence.insert(indices_for_insert[i], words_for_insert[i])

    return paragraph


def random_replace_word_with_synonym(sentence):
    pass


def create_error_data(corpus_path, output_path, word_list_path):

    """
    create error data method.

    input:
            corpus_path
            output_path
            word_list_path
    output:
            error data
    """

    fi = open(corpus_path, 'r')
    print("Open %s corpus file for create error data." % corpus_path)
    word_list = get_word_list(word_list_path)
    fo = open(output_path, 'w')

    str_code = [
        "if do_random_swap_tokens_in_word: random_swap_tokens_in_word(paragraph)",
        "if do_random_swap_words_in_sentence: random_swap_words_in_sentence(paragraph)",
        "if do_random_delete_words: random_delete_words(paragraph)",
        "if do_random_insert_word_to_sentence: random_insert_word_to_sentence(paragraph, word_list)",
    ]
    choose_str_code = [0, 1, 2, 3]

    for line in fi:
        paragraph = ast.literal_eval(line.strip())
        do_random_swap_tokens_in_word = (rd.random() <= 0.73) # choose 10%
        do_random_swap_words_in_sentence = (rd.random() <= 0.73)
        do_random_delete_words = (rd.random() <= 0.73)
        do_random_insert_word_to_sentence = (rd.random() <= 0.73)
        rd.shuffle(choose_str_code)
        for index in choose_str_code:
            exec(str_code[index])
        string_paragraph = convert_list_to_string_type_paragraph(paragraph)
        fo.write(str(string_paragraph) + '\n')

    fi.close()
    fo.close()


def analyse_data(corpus_path):

    '''
    return output data folder path
    '''

    try:

        vncorenlp_file = r'./VnCoreNLP/VnCoreNLP-1.1.1.jar'
        vncorenlp = VnCoreNLP(vncorenlp_file)
        print('Create VNCoreNLP Object.')

        path = corpus_path.split('/')
        corpus_folder_path = '/'.join(path[:-1])
        corpus_filename = path[-1]
        print("corpus folder: %s" % corpus_folder_path)
        print("corpus filename: %s" % corpus_filename)
        output_data_folder_path = corpus_folder_path + '/output-data/'
        if not os.path.exists(output_data_folder_path):
            os.makedirs(output_data_folder_path)
            print("Created %s folder" % output_data_folder_path)

        fi = open(corpus_path, 'r')
        fo_token = open(output_data_folder_path + corpus_filename + '-token', 'w')
        print("Open %s" % corpus_path)
        print("Open %s" % fo_token.name)


        line_number = 0
        for line in fi:
            line_number +=1
        fi.close()
        fi = open(corpus_path, 'r')
        print('We have %d in our corpus.' % line_number)

        for count in tqdm(range(line_number)):

            sentences = fi.readline()
            fo_token.write(str(vncorenlp.tokenize(sentences)) + '\n')

        print('Finish analysis data.')

    except Exception as e:
        raise
    finally:
        fi.close()
        fo_token.close()

        print("Close %s" % corpus_path)
        print("Close %s" % fo_token.name)

    return output_data_folder_path


def random_select_sentence_for_create_error_sentences(fi_path, fo_path):

    """
    return ( file_output_path, file_output_line_index_path)

    file_output_path : text file with sentences for create error sentences
    file_output_line_index_path: line number of sentences in main corpus
    """

    try:
        print("fi path:\t" + fi_path)
        print("fo path:\t" + fo_path)
        fi = open(fi_path, 'r')
        fo = open(fo_path, 'w')

        fo_line_index = open(fo_path + '-line-index', 'wb')
        print("fo_line_index:\t" + fo_line_index.name)
        line_number = 0
        for line in fi:
            line_number +=1
        fi.close()
        fi = open(fi_path, 'r')
        print('we have %d lines in corpus.' % line_number)

        line_index = []
        for count in tqdm(range(line_number)):
            sentence = fi.readline()
            choose = rd.randint(1, 20)
            if choose == 1:
                fo.write(sentence)
                line_index.append(count)

        # uncomment to see line number (in main corpus) of sentence in terminal
        # s = []
        # for i in range(len(line_index)):
        #
        #     s.append(str(line_index[i]))
        #     if i % 10 == 9:
        #         print('\t'.join(s))

        # save line index
        pickle.dump(line_index, fo_line_index)
        fo_line_index.close()
        fo.close()

    except IOError:
        print("IO Exception.")
    finally:
        fi.close()
        fo.close()
        return (fo_path, fo_line_index_path)


if __name__ == '__main__':

    print("Start main func.")
    word_list_path = "../data/word_list"
    corpus_path = '/media/neil-do/SSDIntersection/NCC/ViTone/vitone/corpus/errors/output-data/mini-corpus-error-sentences-token'
    output_path = '../corpus/errors/mini-corpus-error-sentences'
    create_error_data(corpus_path, output_path, word_list_path)
    print("Finish all tasks.")
    # fo_path, fo_line_index_path = random_select_sentence_for_create_error_sentences('../corpus/mini-corpus', '../corpus/errors/mini-corpus-error-sentences')
    # analyse_data(fo_path)
