from unstructured.chunking.basic import chunk_elements

def chunk_content(elements, max_characters=500, new_after_n_chars=500, overlap=0):
    return chunk_elements(
        elements,
        max_characters=max_characters,
        new_after_n_chars=new_after_n_chars,
        overlap=overlap
    )
