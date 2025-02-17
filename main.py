from OpenAIVisionTool import OpenAIBrochureProcessingTool

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
    converter = PDFToJPEGNode(dpi=200)
    bool = converter.convert_pdf_to_jpeg("BBI-Wedding.pdf")
    """
    sample_prompt = """You are the world's greatest image evaluator, specializing in analyzing brochures from wedding venues. 
    Your task is to extract and structure pricing details from the attached image. Specifically, return only the following details in JSON format:
    
    - Each package should be a nested JSON object inside "pricing".
    - Each package must include:
      - Package name
      - Price per person
      - Additional package details
    
    **Formatting Requirements:**
    Strictly follow this structure:
    
    {
      "pricing": {
        "package_one": {
          "package_name": "<<insert package one name>>",
          "price_per_person": <<insert pricing of package one>>,
          "additional_details": "<<insert package one additional details>>"
        },
        "package_two": {
          "package_name": "<<insert package two name>>",
          "price_per_person": <<insert pricing of package two>>,
          "additional_details": "<<insert package two additional details>>"
        }
      }
    }
    
    **Important Rules:**  
    - If this page does not contain pricing information, skip it entirely and return nothing.  
    - If pricing information is present, return only the details specified above—nothing more.  
    - Ensure JSON keys match the specified structure exactly.  
    - Exclude any additional details outside of package-specific pricing.
    """

    directory_path = "/Users/johnschurman/PycharmProjects/WeddingExtractionPOC/BBI-Wedding_folder"

    tool = OpenAIBrochureProcessingTool()
    result = tool._run(directory_path=directory_path, prompt=sample_prompt)
    print(result)
