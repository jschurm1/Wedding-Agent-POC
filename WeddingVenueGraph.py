from langgraph.graph import StateGraph
from typing import TypedDict
import os


class WorkflowState(TypedDict):
    pdf_path: str  # Path to the PDF
    output_dir: str  # Folder where images are saved
    extracted_data: dict  # Store extracted venue details


class WeddingVenueGraph:
    def __init__(self, pdf_processor, openai_tool):
        self.pdf_processor = pdf_processor  # PDF to JPEG Converter
        self.openai_tool = openai_tool  # OpenAI Processing Tool
        self.workflow = self._build_graph()

    def _pdf_to_images(self, state: WorkflowState):
        """Converts PDF to images"""
        success = self.pdf_processor.convert_pdf_to_jpeg(state["pdf_path"])
        if success:
            output_folder = state["pdf_path"].replace(".pdf", "_folder")
            return {"output_dir": output_folder}
        else:
            raise ValueError("PDF conversion failed!")

    def _analyze_images(self, state: WorkflowState):
        """Processes images using OpenAI Vision"""
        output_dir = state["output_dir"]

        prompt_file_path = "prompt_repo"
        prompt = None

        if not os.path.exists(output_dir):
            raise FileNotFoundError(f"Output folder {output_dir} not found!")

        with open(prompt_file_path, "r", encoding="utf-8") as file:
            prompt = file.read().strip()

        extracted_data = self.openai_tool._run(output_dir, prompt)

        return {"extracted_data": extracted_data}

    def _build_graph(self):
        """Creates and compiles the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("pdf_to_images", self._pdf_to_images)
        workflow.add_node("analyze_images", self._analyze_images)

        # Define edges
        workflow.set_entry_point("pdf_to_images")
        workflow.add_edge("pdf_to_images", "analyze_images")

        return workflow.compile()

    def run(self, pdf_path):
        """Runs the workflow"""
        input_data = {"pdf_path": pdf_path}
        return self.workflow.invoke(input_data)
