#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ipm.crew import Ipm

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'question': 'Give me a brief about this whole document.'
    }
    
    try:
        Ipm().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Ipm().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Ipm().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        Ipm().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

#!/usr/bin/env python
# import os
# import sys
# import shutil
# import warnings
# import streamlit as st
# from datetime import datetime
# from crew import Ipm

# warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# # Ensure 'knowledge' directory exists
# KNOWLEDGE_DIR = "knowledge"
# os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

# # Streamlit UI
# st.title("📚 AI Document Processor")

# # File Upload Section
# uploaded_file = st.file_uploader("Upload a document for processing", type=["txt", "pdf", "docx"])

# if uploaded_file is not None:
#     # Save uploaded file to knowledge directory
#     file_path = os.path.join(KNOWLEDGE_DIR, uploaded_file.name)

#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     st.success(f"File saved to {file_path}")

#     # Process with CrewAI
#     if st.button("Run CrewAI Analysis"):
#         st.write("🚀 Processing the document...")
#         try:
#             inputs = {"file_path": file_path}
#             result = Ipm().crew().kickoff(inputs=inputs)
#             st.write("### 🔍 Analysis Results:")
#             st.write(result)
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

