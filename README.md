# FNDC Tournament System API

A FastAPI-based REST API for managing Magic: The Gathering tournaments and cube proposals.

## Features

### User Management
- User registration with email verification
- Password reset functionality
- Profile management (name, email, preferred cube)
- JWT-based authentication

### Tournament Management
- Create tournaments (Admin only)
- View all tournaments
- Register for tournaments
- View tournament registrations

### Cube Proposals
- Propose cubes for tournaments (users)
- View enabled cubes for tournaments
- Manage cube proposal status (Admin only)

## Prerequisites

- Python 3.8+
- MongoDB
- Resend API key for email functionality

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd FNDCbackend
```

2. Activate the virtual environment:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
MONGO_URI=mongodb://localhost:27017
RESEND_API_KEY=your_resend_api_key_here
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

Start the development server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user
- `POST /auth/verify-email` - Verify email with token
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token
- `GET /auth/me` - Get current user info

### User Profile
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile

### Tournaments
- `POST /tournaments/` - Create tournament (Admin only)
- `GET /tournaments/` - List all tournaments
- `GET /tournaments/{tournament_id}` - Get tournament details
- `POST /tournaments/{tournament_id}/register` - Register for tournament
- `GET /tournaments/{tournament_id}/registrations` - Get tournament registrations
- `GET /tournaments/{tournament_id}/my-registration` - Check user registration

### Cube Proposals
- `POST /cubes/propose` - Propose a cube for tournament
- `GET /cubes/tournament/{tournament_id}/enabled` - Get enabled cubes
- `GET /cubes/tournament/{tournament_id}/all` - Get all proposals (Admin only)
- `PUT /cubes/{proposal_id}/status` - Update cube status (Admin only)

## Database Collections

The application uses the following MongoDB collections:
- `users` - User accounts and profiles
- `tournaments` - Tournament information
- `cube_proposals` - Cube proposals for tournaments
- `tournament_registrations` - User registrations for tournaments

## User Roles

- **USER**: Can register for tournaments, propose cubes, view enabled cubes
- **ADMIN**: Can create tournaments, manage cube proposal status, view all data

## Email Functionality

The application uses Resend for sending:
- Email verification links
- Password reset links

Make sure to configure your Resend API key in the `.env` file.

## Development

To run in development mode with auto-reload:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

For production deployment:
1. Set appropriate environment variables
2. Configure CORS origins properly
3. Use a production ASGI server like Gunicorn
4. Set up proper MongoDB authentication
5. Configure SSL/TLS certificates

## License

This project is licensed under the MIT License. 