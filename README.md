this is python weather SaaS on AWS with EC2 instance. there're some tips on how to run it:

   - connect to your ec2 instance
     
   - install all files from repository to your jupyter notebook
     
   - install dependencies
     pip install -r requirements.txt
     
   - get an API key from https://www.visualcrossing.com/weather-api and add it to weather_app.py
     
   - create a token and add it to weather_app.py
     
   - enter this command to run(i hope i configured it correctly)
     uwsgi --http 0.0.0.0:8000 --wsgi-file weather_app.py --callable app --processes 4 --threads 2 --stats your_ip:9191
     
   - enter your request via postman
