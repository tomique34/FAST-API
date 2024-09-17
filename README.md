# FastAPI Blog API 

This project is a RESTful API for a simple blog application built with FastAPI for learning purposes.

## Features

- CRUD operations for blog posts
- User management (create user, get user by ID)
- User authentication (login, generate token)

## Environment Setup

Before running the application, ensure your environment is properly set up:

1. **Python Version**: This project requires Python 3.9 or higher. You can check your Python version with:
   ```
   python --version
   ```

2. **Virtual Environment**: It's recommended to use a virtual environment. Create and activate one with:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**: Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. **Environment Variables**: Create a `.env` file in the root directory with the following variables:
   ```
   DATABASE_HOSTNAME=your_database_host
   DATABASE_PORT=your_database_port
   DATABASE_PASSWORD=your_database_password
   DATABASE_USERNAME=your_database_username
   DATABASE_NAME=your_database_name
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   Replace the placeholders with your actual configuration details.

5. **Database Setup**: Ensure your database is running and accessible with the credentials provided in the `.env` file.

6. **Apply Migrations**: If you're using database migrations, apply them with:
   ```
   alembic upgrade head
   ```
   (Note: You may need to adjust this command based on your specific migration setup)

## Running the Application

After setting up your environment, you can start the application:

```
python -m uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Posts

- `GET /posts/`: Retrieve all posts
- `POST /posts/`: Create a new post
- `GET /posts/{id}`: Retrieve a specific post by ID
- `PUT /posts/{id}`: Update a specific post
- `DELETE /posts/{id}`: Delete a specific post

### Users

- `POST /users/`: Create a new user
- `GET /users/{id}`: Retrieve a user by ID

### Authentication

- `POST /login`: User login

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Technologies Used

- FastAPI
- Pydantic for data validation
- SQLAlchemy for database operations
- Alembic for database migrations (if applicable)

## Troubleshooting

If you encounter any issues:

1. Ensure all environment variables are correctly set in your `.env` file.
2. Check that your database is running and accessible.
3. Verify that all dependencies are installed correctly.
4. If you encounter any "module not found" errors, ensure you're running the application from the correct directory and that your virtual environment is activated.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.