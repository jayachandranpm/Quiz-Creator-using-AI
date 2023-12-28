import streamlit as st
import os
import google.generativeai as genai
import uuid

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
            
            # Display the quiz questions, options, and correct answers
            st.markdown("**Generated Quiz Questions:**")
            
            # Generate a unique ID for the quiz
            quiz_id = str(uuid.uuid4())

            for i, question in enumerate(quiz_data, start=1):
                st.markdown(f"**{i}. {question.text}**")
                
                # Assuming options are within the 'options' field in a list format
                options = getattr(question, 'options', None)
                if options:
                    st.write("Options:", options)
                
                # Assuming correct answer is within the 'correct_answer' field
                correct_answer = getattr(question, 'correct_answer', None)
                if correct_answer:
                    st.write("Correct Answer:", correct_answer)

            # Display a shareable link for the quiz
            quiz_link = f"Your quiz link: [Take Quiz](https://quiz-creator-using-ai.streamlit.app/{quiz_id})"
            st.markdown(quiz_link)

if __name__ == "__main__":
    main()
