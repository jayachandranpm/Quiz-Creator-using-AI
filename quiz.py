import streamlit as st
import os
import google.generativeai as genai
import json
from io import BytesIO

# Set your API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAXdqL57ifjEXUyrrDsyQ8C3sU4VfOzcIg"

# Configure GenerativeAI library with the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Streamlit app
def main():
    st.title("GenerativeAI - Quiz Generator")

    # Input topics and number of questions from the user
    topics = st.text_area("Enter quiz topics (comma-separated):")
    num_questions = st.number_input("Enter the number of questions:", min_value=1, value=5)

    if st.button("Generate Quiz"):
        if not topics:
            st.warning("Please enter quiz topics.")
        else:
            # Generate quiz questions using the GenerativeAI library
            model = genai.GenerativeModel('gemini-pro')

            # Prepare prompt for quiz questions
            prompt = f"Generate {num_questions} quiz questions related to {topics} with options and correct answers"

            response = model.generate_content(prompt)

            # Assuming the quiz questions are within result.parts
            quiz_data = response.parts

            # Use a form to trigger export when the user submits the form
            with st.form(key="export_form"):
                st.markdown("**Generated Quiz Questions:**")
                for i, question in enumerate(quiz_data, start=1):
                    st.markdown(f"**{i}. {question.text}**")

                    # Assuming options are within the 'options' field in a list format
                    options = getattr(question, 'options', None)
                    if options:
                        selected_option = st.radio(f"Options for Question {i}:", options)

                    # Assuming correct answer is within the 'correct_answer' field
                    correct_answer = getattr(question, 'correct_answer', None)
                    if correct_answer:
                        st.write(f"Correct Answer for Question {i}: {correct_answer}")

                export_button = st.form_submit_button("Export Quiz")

            if export_button:
                # Save the quiz content to a JSON file
                quiz_content = {"questions": []}
                for i, question in enumerate(quiz_data, start=1):
                    question_data = {
                        "question_number": i,
                        "question_text": question.text,
                        "options": getattr(question, 'options', None),
                        "correct_answer": getattr(question, 'correct_answer', None)
                    }
                    quiz_content["questions"].append(question_data)

                json_content = json.dumps(quiz_content)
                b = BytesIO(json_content.encode())
                
                # Provide a download link for the user
                st.markdown(f"Download [Quiz.json](data:application/json;base64,{b64encode(b.getvalue()).decode()})")

if __name__ == "__main__":
    main()
