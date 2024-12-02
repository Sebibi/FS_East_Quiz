import streamlit as st
import pandas as pd
import numpy as np
from dataclasses import dataclass
from time import perf_counter, sleep

@dataclass
class Quiz:

    nb_questions: int
    timeout: int
    options: list[str]
    answers: list[str]


    def get_score(self, user_answers):
        correct_answers = [u == a for u, a in zip(user_answers, self.answers)]
        return sum(correct_answers)
    

def main():

    st.set_page_config(layout="wide")

    if "quiz" not in st.session_state:

        nb_questions = st.number_input("Number of questions", min_value=1, value=8)
        timeout = st.number_input("Timeout (seconds)", min_value=1, value=60)

        # Text input for options
        options = st.text_input("Options (comma separated)", value="A,B,C,D").split(",")


        cols = st.columns(nb_questions)
        answers = []
        for i in range(nb_questions):
            answers.append(cols[i].radio(f"Q{i+1}", options))

        if st.button("Create quiz"):

            st.session_state.quiz = Quiz(
                nb_questions=nb_questions, 
                timeout=timeout, 
                options=options,
                answers=answers,
            )
            st.rerun()

    else:

        # Create a timer
        if "start_time" not in st.session_state:
            if st.button("Start quiz"):
                st.session_state.start_time = int(perf_counter())
                st.session_state.last_time = 0
                st.rerun()
        else:
   
            if int(perf_counter()) - st.session_state.last_time > st.session_state.quiz.timeout:
                st.write("You can submit again")

                cols = st.columns(st.session_state.quiz.nb_questions)
                user_answers = []
                for i in range(st.session_state.quiz.nb_questions):
                    user_answers.append(cols[i].radio(f"Q{i+1}", st.session_state.quiz.options))

                if st.button("Submit"):
                    with st.spinner("Submitting..."):
                        sleep(3)
                    st.session_state.score = st.session_state.quiz.get_score(user_answers)
                    st.session_state.last_time = int(perf_counter())
           
                    if st.session_state.score == st.session_state.quiz.nb_questions:
                        st.success("Congratulations! You got all the answers right!")
                        total_seconds = st.session_state.last_time - st.session_state.start_time
                        total_minutes = total_seconds // 60
                        total_seconds = total_seconds % 60
                        st.title(f"Total Time: {total_minutes} min {total_seconds} seconds")
                        st.balloons()
                        st.stop()
                    else:
                        st.session_state.user_answers = user_answers
                        st.rerun()
                    
            else:
                st.error(f"You got {st.session_state.score} out of {st.session_state.quiz.nb_questions} questions right.")
                st.info(f"Your last submisson was : {st.session_state.user_answers}")

                elapsed_time = int(perf_counter()) - st.session_state.last_time
                remaining_time = st.session_state.quiz.timeout - elapsed_time
                
                # Write in the center of the page
                st.markdown(
                    f"""
                    <div style="text-align: center; font-size: 36px; font-weight: bold; margin-top: 20px;">
                    {remaining_time} seconds remaining
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
                sleep(1)
                st.rerun()

main()






        


