from flask import Flask,request,render_template
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()
app = Flask(__name__)
@app.route("/",methods=["GET","Post"])
def index():
    code=None
    title=None
    if request.method == "POST":
        prompt = request.form["request"]
        system_default_prompt="""Interact as a Python coding assistant. You will get a task description from a user
         and you will generate a python class inheriting from 'Job(Task)' with fully implemented run() and the operating methods.
          Then produce a short title 
          Respond with this format
           title: Title Here (with no brackets)
           Code:
           ```python
           (code here)
           """

        client = ChatCompletionsClient(
            endpoint=os.getenv("endpoint"),
            credential=AzureKeyCredential(os.getenv("token")),
        )
        response = client.complete(
            messages=[
                SystemMessage(system_default_prompt),
                UserMessage(prompt),
            ],
            temperature=1.0,
            top_p=1.0,
            model=os.getenv("model")
                         )


        answer = response.choices[0].message.content

        # Extract title and code from the response
        lines = answer.splitlines()
        title_line = next((line for line in lines if line.startswith("title:")), "")
        title = title_line.replace("title:", "").strip()

        if "```python" in answer:
            try:
                code_block = answer.split("```python")[1].strip()
                code = code_block.replace('```','')
            except IndexError:
                code = "Code block not found in the response."
        else:
            code = "Code block not found in the response."

    print (title)
    return render_template("index.html", code=code, title=title)

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
