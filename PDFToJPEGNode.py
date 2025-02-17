import os
from pdf2image import convert_from_path


class PDFToJPEGNode:
    """
    A LangGraph-compatible node that converts a PDF into JPEG images, stored in a dedicated folder.
    """

    def __init__(self, dpi: int = 200):
        """
        Initializes the node with optional DPI settings.

        Args:
            dpi (int): Resolution for image conversion (default: 200).
        """
        self.dpi = dpi

    def convert_pdf_to_jpeg(self, file_path: str):
        """
        Converts a PDF file into JPEG images, storing them in an output folder.

        Args:
            file_path (str): The path to the PDF file.

        Returns:
            List[str]: A list of file paths to the saved JPEG images.
        """

        try:
            if not os.path.exists(file_path):
                print(f'Error: File not found - {file_path}')
                return False
        except Exception as e:
            print(f"Exception occurred while checking file existence: {e}")
            return False

        pdf_root = os.path.splitext(file_path)[0]
        output_folder = f"{pdf_root}_folder"

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Only process if the folder is empty
        if not os.listdir(output_folder):
            images = convert_from_path(file_path, dpi=self.dpi)
            for i, image in enumerate(images):
                output_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
                if not os.path.exists(output_path):
                    image.save(output_path, "JPEG")

        return True

# Example usage
