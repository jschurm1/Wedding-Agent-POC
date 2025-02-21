from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import BaseTool
import base64
from pydantic import PrivateAttr  # ✅ Required for non-Pydantic fields
import re
import os
import json

class OpenAIBrochureProcessingTool(BaseTool):
    """A LangGraph-compatible tool for calling OpenAI's ChatCompletion with image support."""
    name: str = "openai_vision_tool"
    description: str = "Analyzes an image and describes its contents using OpenAI's GPT-4 Vision."
    _chat: ChatOpenAI = PrivateAttr()
    _supported_image_extensions: tuple = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")

    def __init__(self,
                 api_key,
                 model: str = "gpt-4o"):
        super().__init__()
        self._chat = ChatOpenAI(model=model, openai_api_key=api_key)

    def encode_image(self, image_path: str) -> str:
        """Encodes an image as a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _run(self, directory_path: str, prompt: str) -> str:
        """Processes the image and sends it to OpenAI for analysis."""

        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Error: '{directory_path}' is not a valid directory")

        return_dictionary = {}
        venue_name = directory_path.replace("_folder", "")

        for filename in os.listdir(directory_path):
            if filename.lower().endswith(self._supported_image_extensions):
                image_path = os.path.join(directory_path, filename)
                image_base64 = self.encode_image(image_path)
                message = HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                )
                response = self._chat.invoke([message])

                cleaned_string = self._clean_string_convert_to_json(response.content)

                try:
                    cleaned_json = json.loads(cleaned_string)  # Attempt to parse JSON
                    return_dictionary[venue_name] = cleaned_json  # Add to dictionary
                    print(f"{filename}: \n{cleaned_json}")
                except json.JSONDecodeError:
                    print(f"Skipping {filename}: Invalid JSON format")
        return ""

    def _clean_string_convert_to_json(self, json_string):
        pattern = r'^```json\s*(.*?)\s*```$'
        cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL).strip()
        return cleaned_string
