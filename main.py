import regex
import json
import argparse
from configs.config import *
from util.logic import *
from datetime import datetime
from database.database import MySqlDB
from database.other_data import *


# 数据分批处理，将较大的数据列表切分成指定大小的较小批次。
def batchify(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]


def process_json_result(json_result, mysql_info, cover_status):
    json_result_data = json.loads(json_result)
    file_name = json_result_data['file_name']
    try:
        with MySqlDB(mysql_info) as db:
            if cover_status == 'yes':
                del_teardown_json_breaking_result(db, file_name)
            teardown_json_id = get_next_id()
            processing_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_teardown_json(db, teardown_json_id, file_name, json_result_data, processing_time)

            # 准备批量插入数据,列表推导通常比等效的for循环更快
            breaking_results = [
                (file_name, paragraph_no_data['paragraph_no'], sentence_no_data['sentence_no'],
                 i + 1, teardown_character, teardown_json_id)
                for paragraph_no_data in json_result_data['article']
                for sentence_no_data in paragraph_no_data['paragraph_data']
                for i, teardown_character in enumerate(sentence_no_data['text'])
            ]
            # 批量插入
            for batch in batchify(breaking_results, batch_size=200):
                # print(batch)
                insert_breaking_results_batch(db, batch)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Program has finished executing.")


def split_paragraph_into_sentences(paragraph):
    paragraph = paragraph.replace(" ", "")
    sentences = regex.split(r'\p{P}', paragraph)
    return [s for s in sentences if s]


def exhaustive_split(sentence):
    length = len(sentence)
    result = []
    for i in range(length):
        for j in range(i + 1, length + 1):
            result.append(sentence[i:j])
    return result


def process_paragraph(paragraph):
    sentences = split_paragraph_into_sentences(paragraph)
    paragraph_data = [{"sentence_no": i + 1, "text": exhaustive_split(sentence)} for i, sentence in
                      enumerate(sentences)]
    return paragraph_data


def save_text_to_file(path, text):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        return None


def process_data(input_dir, output_dir, cover_status):
    if str(input_dir).endswith('.txt'):
        with open(input_dir, 'r', encoding='utf-8') as file:
            article = file.readlines()
    elif str(input_dir).endswith('.docx'):
        article = get_docx_data(input_dir)
    elif str(input_dir).endswith('.pdf') or str(input_dir).endswith('.PDF'):
        article = get_pdf_data(input_dir)
    else:
        article = ''

    paragraphs = []
    for i, content in enumerate(article, start=1):
        content = content.rstrip('\n')
        res = process_paragraph(content)
        paragraphs.append({"paragraph_no": i, "paragraph_data": res})
    result = {"file_name": f"{os.path.basename(input_dir)}", "article": paragraphs}
    json_result = json.dumps(result, ensure_ascii=False, indent=2)

    if cover_status == 'yes':
        save_text_to_file(output_dir, json_result)
        process_json_result(json_result, mysql_info, cover_status='yes')
    else:
        if os.path.isfile(output_dir):
            pass
        else:
            save_text_to_file(output_dir, json_result)
            process_json_result(json_result, mysql_info, cover_status='no')


def main():
    parser = argparse.ArgumentParser(description='Process a file.')
    parser.add_argument('input_dir', type=str, help='Path to the input file')
    parser.add_argument('output_dir', type=str, help='Path to the output text file')
    parser.add_argument('cover_status', choices=['yes', 'no'], help='Enter "yes" for true or "no" for false')
    args = parser.parse_args()
    process_data(args.input_dir, args.output_dir, args.cover_status)


if __name__ == "__main__":
    main()
