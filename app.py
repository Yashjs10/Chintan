from flask import Flask, render_template, jsonify, request  
from flask_pymongo import PyMongo  





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

       
        chat = mongo.db.chats.find_one({"question": question})
        if chat:
            return jsonify({"question": question, "answer": chat['answer']})

       
        
       
        data = {"question": question, "answer": answer}

        # Save to MongoDB
        mongo.db.chats.insert_one(data)
        return jsonify(data)
    except Exception as e:
        print("Error processing request:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001, use_reloader=False)
