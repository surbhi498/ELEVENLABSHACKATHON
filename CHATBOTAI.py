import streamlit as st
import pyttsx4
import speech_recognition as sr
from res import jk
from res import send_email
from tty_1 import speech_to_text
import uuid
# Function for text-to-speech
def text_to_speech(message):
    engine = pyttsx4.init()
    engine.say(message)
    engine.runAndWait() 

def stt_function():
    st.title("Speech-to-Text with Streamlit")

    # Use radio buttons to choose the input method
    user_choice = st.radio("Choose Input Method:", ("Text Input", "Speech"))

    if user_choice == "Text Input":
        job_keywords_input = st.text_input("Enter job keywords (comma-separated)", key=f"input_method_{str(uuid.uuid4())}")
    elif user_choice == "Speech":
        job_keywords_input = speech_to_text()
        if not job_keywords_input:
            return
        st.write("Spoken text:", job_keywords_input)
        text_to_speech("Got it! Please wait while I process your input.")

    return job_keywords_input    

def op():
    st.title("Chatbot Application")

    # Start the conversation loop
    st.write("Chatbot: Hello! I'm your chatbot. Please provide me with the job description you want to match against.")

    response = ""
    job_keywords_input = stt_function()

    if st.button("Submit"):
        # Convert the user input to a list of keywords
        job_keywords_input = job_keywords_input.strip()
        job_keywords = [keyword.strip() for keyword in job_keywords_input.split(",") if keyword.strip()]

        if not job_keywords:
            st.write("Please enter job keywords to proceed.")
            return
        else:
            response = jk(job_keywords)
    send_email_flag = False
    # Process the user's query and get the top candidates
    if response:
        for i, candidate_info in enumerate(response):
            candidate = candidate_info['Candidate']
            email = candidate_info['email']
            st.write(f"Chatbot: Top Candidate {i + 1}: {candidate}")
            st.write(f"Chatbot: Email: {email}")

        # Ask for email confirmation
        st.write("Chatbot: Do you want to send interview invitations to these candidates? (Yes/No)")
        #email_confirmation = st.text_input("Enter 'yes' or 'no'")
        email_confirmation = st.selectbox("Select 'Yes' or 'No':", ("Yes", "No"), key="email_confirmation")
        #email_confirmation = st.radio("Select 'Yes' or 'No':", ("Yes", "No"))
        if email_confirmation == "Yes":
                # Show the send_email_button
                send_email_flag = True

        if send_email_flag:
            # Implement the email sending only if send_email_flag is True
            subject = "Job Opportunity"
            content = "Congratulations! You have been selected for the job interview. You will receive the test link shortly. Check your mail for updates."
            send_email_button = st.button("Send Email")

            if send_email_button:
                # Implement the email sending
                send_email(subject, content, email)
                st.write("Chatbot: Message sent successfully!")
                send_email_flag = False  # Reset the flag after sending the email

        
    # Prompt the user for the next query
    st.write("Chatbot: Please provide me with the next job description.") 
if __name__ == "__main__":
    op()
