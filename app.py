import os
import PyPDF2
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

def extract_pdf_text(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
            
        return pdf_text

def generate_prompt(input_text):
    prompt = f"You are a helpful AI assistant. Given the following text:\n\n{input_text}\n\nPlease provide three actionable ideas on how to connect with this person over LinkedIn."
    return prompt

@app.route("/api/process-pdf", methods=["POST"])
def process_pdf():
    pdf = request.files["pdf"]
    if pdf:
        pdf_path = "temp.pdf"
        pdf.save(pdf_path)

        extracted_text = extract_pdf_text(pdf_path)
        os.remove(pdf_path)

        additional_text = "\n\n“I’m seeking a job and wish to connect with this person over LinkedIn. Based on their top three accomplishments, give me three message ideas on how I can get them to accept a connection request from me. The output should be just 3 example messages to be sent to the person.”"
        text_with_additional = extracted_text + additional_text

        # Generate prompt using GPT-3 chat model
        prompt = generate_prompt(text_with_additional)
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=1.25,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        generated_response = response.choices[0].text.strip()

        return jsonify({"generatedResponse": generated_response})

if __name__ == "__main__":
    app.run(debug=True)
