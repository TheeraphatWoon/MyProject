# Durian Disease Analysis and Recommendation System via LINE Chatbot with Object Detection

**Team Members:**
* Theeraphat Sukwong ([https://github.com/TheeraphatWoon])

## 📝 Overview 

This project introduces an AI-driven system designed to detect and analyze diseases on durian leaves using object detection, providing real-time recommendations through a LINE Chatbot. Developed as a final year project for Electronics Engineering, this system aims to assist durian farmers in early disease identification and management, leveraging modern AI and communication technologies.

## ✨ Key Features 

* **AI-Powered Disease Detection:** Utilizes YOLOv8 model for accurate identification and classification of various durian leaf diseases from uploaded images.
* **Real-time Analysis via LINE Chatbot:** Users can upload images directly to the LINE Chatbot and receive instant disease analysis and recommendations.
* **Data Management:** Implemented MySQL database for efficient storage and retrieval of disease information and user interaction data.
* **Seamless Integration:** Connects AI model with LINE Messaging API, Webhooks, and a Flask backend for robust communication and functionality.
* **Cultivation Advice:** Offers practical recommendations for disease management and cultivation practices based on detection results.

## ⚙️ Technologies Used 

* **Programming Languages:** Python
* **AI/Machine Learning:** YOLOv8 (Object Detection)
* **Database:** MySQL
* **Web Framework:** Flask
* **Messaging Platform:** LINE Messaging API, LINE Chatbot
* **Deployment/Connectivity:** Webhooks
* **Other Libraries/Tools:** (e.g., OpenCV, NumPy)

## 💡 System Architecture 

*Briefly explain how different components interact in text:*
* The system begins when a user sends an image of a durian leaf to the LINE Chatbot.
* The LINE Chatbot, configured with a Webhook, forwards this image to the Flask backend application.
* The Flask backend processes the incoming image and feeds it into the pre-trained YOLOv8 AI model for disease detection and classification.
* Once detection results (e.g., disease type) are obtained, the system queries the MySQL database to fetch relevant disease information and recommended cultivation advice.
* Finally, the analysis results, along with practical recommendations, are sent back to the user through the LINE Chatbot for immediate display.

## 🚀 Getting Started 

### Prerequisites 
* Python 3.x
* MySQL Server
* LINE Developers Account
* Ngrok (for local testing of webhooks)

### Installation 
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TheeraphatWoon/MyProject.git
    cd MyProject
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Remember to create a `requirements.txt` file by running `pip freeze > requirements.txt` after installing all your project's libraries.)*
4.  **Database Setup:**
    * Create a MySQL database.
5.  **LINE Chatbot Setup:**
    * Configure your LINE Messaging API (obtain Channel Access Token and Channel Secret).
    * Set up your Webhook URL using Ngrok or deploy to a public server.
6.  **Run the Flask application:**
    ```bash
    python FinalProject.py
    ```

## 📋 Usage 

1.  Add the LINE Chatbot to your LINE account.
2.  Send an image of a durian leaf to the chatbot.
3.  Receive immediate analysis of potential diseases and recommended actions.

## 🛣️ Future Enhancements 

* Integrate more disease types and expand the knowledge base.
* Develop a mobile application for a richer user experience.
* Implement real-time monitoring of environmental factors.
* Add multi-language support.

## 📧 Contact 

For any inquiries or feedback, please contact:
* Theeraphat Sukwong: [theeraphatwoon@gmail.com]
