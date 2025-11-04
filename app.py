import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

from src.utils.helpers import *
from src.generator.question_generator import QuestionGenerator

def main():
  st.set_page_config(page_title="study buddy AI")

  if 'quiz_manager' not in st.session_state:
    st.session_state.quiz_manager = QuizManager()
  
  if 'quiz_generated' not in st.session_state:
    st.session_state.quiz_generated = False
  
  if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
  
  if 'rerun_trigger' not in st.session_state:
    st.session_state.rerun_trigger = False
  
  st.title("Study Buddy AI")

  st.sidebar.header('Quiz settings')
  question_type = st.sidebar.selectbox(
    "Select question type",
    ["Multiple Choice", "Fill in the blank"],
    index=0
  )

  topic = st.sidebar.text_input("Enter topic", placeholder="History, Geography, Cricket")

  difficulty = st.sidebar.selectbox(
    "Difficulty level",
    ["Easy", "Medium", "Hard"],
    index=1
  )

  num_questions = st.sidebar.number_input("number of questions", min_value=1, max_value=10, value=5)

  if st.sidebar.button("Generate Quiz"):
    st.session_state.quiz_submitted = False

    generator = QuestionGenerator()
    success = st.session_state.quiz_manager.generator_questions(
      generator, 
      topic=topic, 
      question_type= question_type, 
      difficulty=difficulty, 
      num_questions=num_questions
    )

    st.session_state.quiz_generated = True
    rerun()
  
  if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
    st.header("Quiz")
    st.session_state.quiz_manager.attempt_quiz()

    if st.button("Submit quiz"):
      st.session_state.quiz_manager.evaluate_quiz()
      st.session_state.quiz_submitted = True
      rerun()

  if st.session_state.quiz_submitted:
    st.header("Quiz results")
    results_df = st.session_state.quiz_manager.generate_results_dataframe()

    if not results_df.empty:
      correct_count = results_df['is_correct'].sum()
      total_questions = len(results_df)
      score_percentage = (correct_count/total_questions) * 100
      st.write(f"Score: {score_percentage}")

      for _, result in results_df.iterrows():
        question_num = result['question_number']
        if result['is_correct']:
          st.success(f"Question {question_num}: {result['question']}")
        else:
          st.error(f"Question {question_num}: {result['question']}")
          st.write(f"Your answer: {result['user_answer']}")
          st.write(f"Correct answer: {result['correct_answer']}")
        
        st.markdown("-----")
      
      if st.button("Save Results"):
        saved_file = st.session_state.quiz_manager.save_tocsv()
        if saved_file:
          with open(saved_file, 'rb') as f:
            st.download_button(
              label="Download Results",
              data=f.read(),
              file_name=os.path.basename(saved_file),
              mime="text/csv"
            )
      else:
        st.warning("No results available")
          
if __name__ == '__main__':
  main()