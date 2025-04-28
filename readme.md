# README - Projet de fin de session - Sécurité informatique pour l'internet des objets

## Run the code
### 1. Initialisation of the detection part
```bash
python -m venv venv
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
- Create a `.env` file containing the following environnement variables :
- DISCORD_WEBHOOK_URL=  
- SAVE_DIR=  
- API_URL=http://localhost:4000/video/add  
- ENCRYPTION_KEY=  
- VIDEO_CODEC=mp4v  


To run : `python main.py`


### 2. Initialization of the server part 

Requirement : UV
-  Windows install
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
- MacOS and Linux install
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

In the dashboard_secu_iot directory

- Create a `.env` file containing the following environnement variables :
    - Database variable : DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
    - Frenet encryption key : ENCRYPTION_KEY
    - Flask encryption key : SECRET_KEY

- Initialize the database
    ```bash
    flask --app dashboard init-db
    ```

- Run the server
    ```bash
    flask --app dashboard run --port=4000
    ```

<hr>  

## Project Overview


This project implements a secure IoT surveilance system using a webcam and a RaspBerry Pi 4.   
All detection and video processing are performed locally to minimize exposure to external attacks and ensure data confidentiality.
Main characteristics : 

### Detection   
- YOLOv11n object detection model runs locally (on the RP4), runs on an optimized NCNN format made for devices with limited computing power and no graphical acceleration. Ideal for lightweight real time detection.

When a detection occurs : 
- An alert is sent to a Discord channel using a webhook
- A video recording starts and stays active while there is a detection.

When a detection stops :
- The video is encrypted and saved. 
- A POST request is sent to the server, with the address of the recorded video and some data about the detection (timestamp, number of people detected, ..) in JSON format.

All image processing remains fully local, reducing the risk of sensitive data interception.

### Server side
elouan jte laisse compléter


### Overall Security considerations :
- All detection are made locally on the RaspberryPi, minimizing attack surface.
- **Authentication and session security**
  - Strong password policies are enforced when creating user accounts.
  - JWTs are used for user authentication and are stored in Http Only cookies.
- **Acess controls** : Access to videos and detection logs is restricted to authenticated users only.
- **Secure communication** : Access to the app is secured with TLS (HTTPS) using Nginx reverse proxy and a self signed certificate (+ .cert file on the user device).
- **Secure storage** : All videos are encrypted and signed.
- **Logging** : All connections to the app are logged to ensure traceability.



