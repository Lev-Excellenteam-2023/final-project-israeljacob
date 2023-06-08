from pptx import Presentation


def extract_text_from_pptx(file_path):
    """
        Extracts text from a .pptx file using the python-pptx package.

        Args:
            file_path (str): The path to the .pptx file.

        Returns:
            str: The extracted text from the .pptx file.
    """

    presentation = Presentation(file_path)
    extracted_text = ""
    for slide in presentation.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        extracted_text += run.text + " "
            elif shape.has_table:
                table = shape.table
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                extracted_text += run.text + " "
    return extracted_text
