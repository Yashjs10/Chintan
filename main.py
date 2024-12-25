from flask import Flask, render_template, jsonify, request  
from flask_pymongo import PyMongo  
import openai


openai.api_key = "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"

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://yashawasthi854:sxnGJivoUPK0zDkh@cluster1.af0mc.mongodb.net/chintan"
mongo = PyMongo(app)

@app.route("/")
def home():
    try:
        chats = mongo.db.chats.find({})
        myChats = [chat for chat in chats]
        print(myChats)
        return render_template("index.html", myChats=myChats)
    except Exception as e:
        print("Error fetching chats:", e)
        return render_template("index.html", myChats=[])

@app.route("/api", methods=["POST"])
def qa():
    try:
        question = request.json.get("question")
        if not question:
            return jsonify({"error": "Question is required"}), 400

        # Check if question already exists in MongoDB
        chat = mongo.db.chats.find_one({"question": question})
        if chat:
            return jsonify({"question": question, "answer": chat['answer']})

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        print(response)  # Log the response for debugging

        answer = response.choices[0].message.content if response.choices else "No response from API"
        data = {"question": question, "answer": answer}

        # Save to MongoDB
        mongo.db.chats.insert_one(data)
        return jsonify(data)
    except Exception as e:
        print("Error processing request:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)
