import os
import json
from typing import Dict, Any
from langchain_core.tools import Tool
from langchain_core.tools import BaseTool
from pdf2image import convert_from_path


class PDFToJpegTool(BaseTool):
    """
    A LangGraph tool that converts a PDF into JPEG images stored in a dedicated folder.
    """

    def __init__(self, dpi: int = 200):
        super().__init__(
            name="pdf_to_jpeg_tool",  # ✅ Pass directly
            func=self._run,
            description="Converts a PDF file into JPEG images stored in a dedicated folder."
        )
        self._dpi = dpi

    def _run(self, file_path: str) -> None:
        print("got to the run function")
        """
        Converts the PDF file into JPEG images, one per page, saving them in a folder.

        Args:
            file_path (str): The path to the PDF file.

        Returns:
            Dict[str, Any]: Jpeg object containing the output folder and saved images.
        """
        if not os.path.exists(file_path):
            print('{"error": "File not found"}')

        if os.path.exists(file_path):
            pdf_root = os.path.splitext(file_path)[0]
            output_folder = f"{pdf_root}_folder"

            # Ensure the folder exists, create if not
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Only process if the folder is empty
            image_files = []
            if not os.listdir(output_folder):
                images = convert_from_path(file_path, dpi=self._dpi)
                for i, image in enumerate(images):
                    output_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
                    if not os.path.exists(output_path):
                        image.save(output_path, "JPEG")
                        image_files.append(output_path)
