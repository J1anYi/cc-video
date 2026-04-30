# CC Video

A web-based movie watching system with separated frontend and backend services. Users can browse a movie catalog and play uploaded videos; administrators can manage the movie library.

## Features

- User authentication with JWT tokens
- Movie catalog browsing for logged-in users
- Video playback with seeking support
- Admin panel for movie management
- Video file upload

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables (optional, defaults provided):
   ```bash
   # On Windows:
   set SECRET_KEY=your-secret-key-here
   set DATABASE_URL=sqlite+aiosqlite:///./data/cc_video.db
   
   # On macOS/Linux:
   export SECRET_KEY=your-secret-key-here
   export DATABASE_URL=sqlite+aiosqlite:///./data/cc_video.db
   ```

5. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

The backend API will be available at `http://localhost:8000`.

## Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`.

## Default Accounts

The system creates a default admin account on first startup:

- **Username:** `admin`
- **Password:** `admin123`

You can create additional user accounts through the backend API.

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login (returns JWT token)
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/me` - Get current user info

### User Routes (require authentication)
- `GET /api/v1/movies` - List published movies
- `GET /api/v1/movies/{id}` - Get movie details
- `GET /api/v1/movies/{id}/stream` - Stream video file

### Admin Routes (require admin role)
- `GET /api/v1/admin/movies` - List all movies
- `POST /api/v1/admin/movies` - Create movie
- `PUT /api/v1/admin/movies/{id}` - Update movie
- `DELETE /api/v1/admin/movies/{id}` - Delete movie
- `POST /api/v1/admin/movies/{id}/video` - Upload video file

## Usage

1. Start the backend server
2. Start the frontend server
3. Open `http://localhost:5173` in your browser
4. Login with the admin account or a user account
5. Browse the movie catalog and play videos

For admin tasks:
1. Login as admin
2. Navigate to `/admin/movies`
3. Create, edit, or delete movies
4. Upload video files to movies

## Architecture

- **Backend:** FastAPI with SQLAlchemy async, JWT authentication
- **Frontend:** React with Vite, React Router
- **Database:** SQLite (default, configurable)
- **Video Storage:** Local filesystem in `backend/uploads/videos/`

## License

MIT
