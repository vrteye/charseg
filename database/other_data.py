import json


def insert_teardown_json(db, id, file_name, json_result, processing_time):
    sql = """
    INSERT INTO teardown_json
    (id, file_name, json_result, processing_time)
    VALUES (%s, %s, %s, %s)
    """
    params = (id, file_name, json.dumps(json_result, ensure_ascii=False, indent=2), processing_time)
    db.crud(sql, params)


def insert_breaking_result(db, breaking_result_id, file_name, paragraph_no, sentence_no, dismantling_record_no,
                           teardown_character, teardown_json_id):
    sql = """
    INSERT INTO breaking_result
    (id,file_name,paragraph_no,sentence_no,dismantling_record_no,teardown_character,teardown_json_id)
    VALUES (%s, %s, %s, %s,%s, %s, %s)
    """
    params = (breaking_result_id, file_name, paragraph_no, sentence_no, dismantling_record_no, teardown_character,
              teardown_json_id)
    db.crud(sql, params)


def del_teardown_json_breaking_result(db, file_name):
    sql = f"""
    DELETE FROM teardown_json WHERE file_name = '{file_name}'; 
    DELETE FROM breaking_result WHERE file_name = '{file_name}'"""
    db.crud(sql)


def insert_breaking_results_batch(db, batch):
    insert_query = """
        INSERT INTO breaking_result
        (file_name, paragraph_no, sentence_no, dismantling_record_no, teardown_character, teardown_json_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    db.exec_many(insert_query, batch)