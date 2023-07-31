import csv
import tensorflow as tf
import tensorflow_hub as hub
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY1")
pwd = os.getenv("pwd")

# API request endpoint
API_ENDPOINT = "https://language.googleapis.com/v1beta2/documents:analyzeEntities?key=" + API_KEY

# Load Universal Sentence Encoder model
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
def send_email(subject, content, recipients):
        # Replace these with your email credentials
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        sender_email = "surbhisharma9099@gmail.com"
        sender_password = pwd

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ", ".join(recipients)
        message["Subject"] = "Job Opportunity"
        content = "Hi, Hello, Congratulations! You have been selected for the job interview."
        message.attach(MIMEText(content, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())
            server.quit()
            return True
        except smtplib.SMTPException:
            return False


def semantic_similarity(text1, text2):
    embeddings = model([text1, text2])
    similarity_score = tf.abs(tf.keras.losses.cosine_similarity(embeddings[0], embeddings[1])).numpy()
    return similarity_score

def analyze_entities(resume_text, job_keywords):
    request_data = {
        "document": {
            "content": resume_text,
            "type": "PLAIN_TEXT"
        },
        "encodingType": "UTF8"
    }

    response = requests.post(API_ENDPOINT, json=request_data)
    job_keywords_lower = {keyword.lower() for keyword in job_keywords}

    if response.status_code == 200:
        api_results = response.json()
        entities = api_results.get("entities", [])
        extracted_keywords = {entity.get("name", "").lower() for entity in entities}
        num_matching_keywords = len(extracted_keywords.intersection(job_keywords_lower))
        return num_matching_keywords, extracted_keywords
    else:
        print(f"Error: Unable to process the request. Status code: {response.status_code}")
        return 0, {}
@st.cache
def jk(job_keywords):
    candidate_resumes = [
        {"name": "John Doe", "email": "deependujha21@gmail.com", "resume_text": "Experienced software engineer with Python skills."},
        {"name": "Jane Smith", "email": "surbhisharma9099@gmail.com", "resume_text": "Java developer with experience in web development."},
        # Add more candidates' resumes as needed
    ]

    with open("filtered_candidates.csv", "w", newline="") as csvfile:
        fieldnames = ["Candidate", "Resume Text", "Num Matching Keywords", "Semantic Similarity Score", "email"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for candidate in candidate_resumes:
            resume_text = candidate["resume_text"]
            num_matching_keywords, extracted_keywords = analyze_entities(resume_text, job_keywords)

            job_description = " ".join(job_keywords)
            resume_keywords = " ".join(extracted_keywords)
            similarity_score = semantic_similarity(job_description, resume_keywords)
            writer.writerow({
                "Candidate": candidate["name"],
                "Resume Text": resume_text,
                "Num Matching Keywords": num_matching_keywords,
                "Semantic Similarity Score": similarity_score.item(),
                "email": candidate["email"]
            })

    # Read the CSV file
    df = pd.read_csv("filtered_candidates.csv")

    # Sort by semantic similarity score in descending order
    df_sorted = df.sort_values(by="Semantic Similarity Score", ascending=False)

    # Select the top candidate
    top_candidate = df_sorted.head(1)

    # Extract email address of the top candidate
    top_email = top_candidate["email"].tolist()[0]

    return [{"Candidate": top_candidate["Candidate"].tolist(), "email": top_email}]
