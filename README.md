# Pizza Delivery System API
This is a REST API for a Pizza delivery service built using following technologies : 
1. FastAPI
2. SQLAlchemy
3. PostgreSQL (Supabase)
4. Render (for deployment)

Visit the [API](https://pizzadileverysystemapi.onrender.com/docs)

![Firefox_Screenshot_2023-12-04T07-08-50 380Z](https://github.com/ayush20501/PizzaDeliverySystemAPI/assets/77526719/406433db-e119-43fb-b57f-be9cb990d745)

## API Routes

| Endpoint                        | Method | Description                                      | Access |
|---------------------------------|--------|--------------------------------------------------|--------------------------|
| `/login`           | POST   | Authenticate a user and return a token                           | All users                     |
| `/signup` | POST    | Register a new user | All users                      |
| `/pizzas`| GET | List available pizza types and their prices                | All users                     |
| `/order`           | GET   | Retrieve a list of all orders                           |Authenticated users                     |
| `/order` | POST    | Place a new pizza order | Authenticated users                     |
| `/order/{order_id}`| GET | Retrieve details of a specific order                    | Authenticated users                     |
| `/order/{order_id}`           | PUT   |Update an existing order                           | Authenticated users                    |
| `/order/{order_id}` | DELETE    | Cancel an order |Authenticated users

## How to run the Project

   - Install Python
   - Git clone the project with  git clone `https://github.com/ayush20501/PizzaDeliverySystemAPI.git`
   - Create your virtualenv and activate it
   - Install the requirements with `pip install -r requirements.txt`
   - Set Up your PostgreSQL database and set its URI in your database.py
      
      ```bash
      SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:<username>:<password>@localhost/<db_name>'
      ```
   - Finally run the API `uvicorn main:app `

## How to test the Project

Test the API without setting up the project locally

**On Swagger UI**
- Open url `https://pizzadileverysystemapi.onrender.com/docs`
- If you are not signed up, click on the `/signup ` endpoint and fill in the required details. If you have already signed up, click on the "Authenticate" button and input your username and password
- Create your virtualenv and activate it
- Once authenticated, you will have access to authenticated routes

**On Postman**
- Download and Install Postman
- Open Postman and create a new request
- Enter the URL for your FastAPI login endpoint (e.g., http://127.0.0.1:8000/login)
- Select `"x-www-form-urlencoded"` or `"raw"` and set the content type accordingly
- Provide the username and password in the request body to to obtain a JWT token by sending a POST request with valid credentials
- Copy the received token
- Use the `protected` endpoints by sending a request with the token in the Authorization header (Bearer token)

***
Created By: Ayush Gupta<br/>
Gmail: ayush20501.ag@gmail.com<br/>
[Linkedin](https://www.linkedin.com/in/ayush-gupta-3bb02a1a2)

