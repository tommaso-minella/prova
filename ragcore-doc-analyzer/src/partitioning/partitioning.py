# src/partitioning/partitioning.py
import os
from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.docx import partition_docx
from unstructured.partition.xlsx import partition_xlsx

def partition_content(blob, file_identifier):
    file_extension = file_identifier.split('.')[-1].lower()

    # Write blob to a temporary file
    temp_file_path = f"/tmp/temp.{file_extension}"
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(blob)

    if file_extension == 'pdf':
        elements = partition_pdf(filename=temp_file_path, strategy="hi_res")
    elif file_extension in ['ppt', 'pptx']:
        elements = partition_pptx(filename=temp_file_path)
    elif file_extension in ['doc', 'docx']:
        elements = partition_docx(filename=temp_file_path)
    elif file_extension in ['xls', 'xlsx']:
        elements = partition_xlsx(filename=temp_file_path)
    else:
        elements = partition(filename=temp_file_path)
    
    os.remove(temp_file_path)
    return elements
