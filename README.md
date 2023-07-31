# AI Chatbot for Candidate Screening and Recruitment

![Chatbot Demo](/path/to/demo.gif)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## Overview

This AI-powered Chatbot is designed to streamline the candidate screening and recruitment process. It leverages Natural Language Processing (NLP) to parse resumes and match job descriptions with top candidates. The Chatbot offers both text and voice-based input options for user convenience. Users can input job keywords or use speech recognition to provide job descriptions. The Chatbot then recommends the top candidates based on the job requirements and allows bulk sending of acceptance/rejection emails. Streamlit is used to create an interactive web application for hosting the Chatbot. The project aims to improve the efficiency and accuracy of the recruitment process.

## Features

- Resume parsing and candidate matching
- Text and voice-based input methods
- Bulk email sending for acceptance/rejection
- Interactive web interface using Streamlit

## Installation

1. Clone the repository.

 git clone https://github.com/your-username/your-repo.git 


2. Create a virtual environment and activate it.

 python3 -m venv myenv
 source myenv/bin/activate


3. Install the required dependencies from `requirements.txt`.

pip install -r requirements.txt 


4. Run the Chatbot using Streamlit.


streamlit run CHATBOTAI.py 

## Usage

1. Access the Chatbot web interface in your browser.

  http://localhost:8501



2. Choose the input method: text or speech.
- For text input, enter job keywords separated by commas.
- For speech input, click the microphone icon and speak your job description.

3. Click "Submit" to get top candidate recommendations.

4. Select candidates for email invitations and send them in bulk.

## Technologies Used

- Python
- Natural Language Processing (NLP) libraries
- Streamlit
- SpeechRecognition
- SMTP (for email sending)

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License




