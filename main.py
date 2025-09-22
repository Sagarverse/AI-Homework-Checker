from flask import Flask, render_template, request
from PIL import Image
from pytesseract import pytesseract
from gpt4all import GPT4All
app = Flask(__name__)
model = GPT4All('wizardlm-13b-v1.2.Q4_0.gguf')
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def generate_output(text):
    generated_output = model.generate(prompt=text, max_tokens=20000)
    return generated_output

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        image_file = request.files["image"]
        if image_file:
            img = Image.open(image_file)
            pytesseract.tesseract_cmd = path_to_tesseract
            text = pytesseract.image_to_string(img)
            text = text[:-1]
            generated_output = generate_output(text)
            return render_template("result.html", text=text, generated_output=generated_output)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
