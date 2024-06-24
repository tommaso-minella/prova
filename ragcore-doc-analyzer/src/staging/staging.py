def stage_content(chunked_content, file_identifier, users):
    staged_chunks = []
    for chunk in chunked_content:
        chunk_dict = {
            'text': chunk.text,
            'metadata': {
                'file_identifier': file_identifier,
                'users': users,
            }
        }
        staged_chunks.append(chunk_dict)
    return staged_chunks