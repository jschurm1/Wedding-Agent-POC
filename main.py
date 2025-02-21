from OpenAIVisionTool import OpenAIBrochureProcessingTool
import os
from langgraph.graph import StateGraph
from typing import TypedDict
from PDFToJPEGNode import PDFToJPEGNode
from WeddingVenueGraph import WeddingVenueGraph

sample_prompt = """You are the world's greatest image evaluator, specializing in analyzing brochures from wedding venues. 
   Your task is to extract and structure pricing details from the attached image. Specifically, return only the following details in JSON format:

   - Each package should be a nested JSON object inside "pricing".
   - Each package must include:
     - Package name
     - Price per person
     - Additional package details

   - If there are additional costs beyond per-person pricing, extract and return them under "additional_cost".  
   - Additional costs can include (but are not limited to) venue fees, mandatory gratuity, service charges, ceremony fees, or any other extra expenses.  

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
     },
     "additional_cost": {
       "additional_cost_one": {
         "additional_cost_one_description": "<<description of additional cost>>",
         "additional_cost_one_cost": <<additional cost dollar amount>>
       },
       "additional_cost_two": {
         "additional_cost_two_description": "<<description of additional cost>>",
         "additional_cost_two_cost": <<additional cost dollar amount>>
       }
     }
   }

   **Important Rules:**  
   - If this page does not contain pricing or additional cost information, skip it entirely and return nothing.  
   - If pricing or additional costs are present, return only the details specified above—nothing more.  
   - Ensure JSON keys match the specified structure exactly.  
   - Exclude any unnecessary information beyond pricing and additional costs.
   """

def _get_api_key_():
    file_name = "open_ai_api_key"

    # Read the file
    with open(file_name, "r") as file:
        api_key = file.readline().strip()  # Read the first line and remove any trailing whitespace

    # Print or use the API key
    return str(api_key)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    api_key = _get_api_key_()  # Load API key

    # Initialize components
    pdf_processor = PDFToJPEGNode(dpi=200)
    openai_tool = OpenAIBrochureProcessingTool(api_key=api_key)

    # Create the graph instance
    wedding_graph = WeddingVenueGraph(pdf_processor, openai_tool)

    # Run the workflow
    result = wedding_graph.run("BBI-Wedding.pdf")

    print("Final Extracted Data:", result["extracted_data"])

