# TAO2102_Horse_Racing_Prediction

## First Approach
1. In the command prompt, go to the directory: TAO2102_Horse_Racing_Prediction\software\client, type "npm start" to start the frontend server.
2. Open the anaconda command, go to the directory: TAO2102_Horse_Racing_Prediction\software\server, type "pip install -r requirements.txt" to install python packages with specific versions.
2.1. Type "python manage.py runserver" to start the backend server.

## Second Approach
1. In the command prompt, go to the directory: TAO2102_Horse_Racing_Prediction\software\client, type "npm start".
2. Open another command prompt, go to the directory: TAO2102_Horse_Racing_Prediction\software\.venv, type ".\\Scripts\\activate.bat" (type "source Scripts/activate" for Mac) to activate the virtual environment.
2.1. Type "pip install -r requirements.txt" to install python packages with specific versions.
2.2. Type "cd server" to go to the backend directory.
2.3. Type "python manage.py runserver" to start the backend server.

If error happened, it should probably bacause of some missing package in the frontend or backend. Please check and install them back
1. Frontend, in the frontend directory, type "npm install <missing package>"
2. Backend, in the backend directory, type "pip install <missing package>"
