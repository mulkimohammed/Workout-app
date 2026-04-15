# Workout Tracking API
A backend API for a workout tracking application used by personal trainers.

## Features
- RESTful Flask API for tracking workouts, exercises, and workout sessions
- Complete CRUD operations for exercises and workouts
- Nested data serialization with Marshmallow
- Input validation at both model and schema levels
- SQLAlchemy relationships for data integrity
- Database constraints and model validations
- Comprehensive seed data for testing

## Installation
1. Install dependencies:
```bash
pipenv install
```

2. Activate virtual environment:
```bash
pipenv shell
```

3. Initialize database migrations:
```bash
flask db init
```

4. Generate migration:
```bash
flask db migrate -m "Initial migration"
```

5. Apply migration:
```bash
flask db upgrade
```

6. Seed database:
```bash
python server/seed.py
```

## Running the Application
Start the Flask development server:
```bash
flask run
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints
### Exercises
- `GET /exercises` - Get all exercises
- `GET /exercises/<id>` - Get a single exercise by ID
- `POST /exercises` - Create a new exercise
- `PUT /exercises/<id>` - Update an exercise
- `DELETE /exercises/<id>` - Delete an exercise

### Workouts
- `GET /workouts` - Get all workouts
- `GET /workouts/<id>` - Get a single workout by ID
- `POST /workouts` - Create a new workout
- `PUT /workouts/<id>` - Update a workout
- `DELETE /workouts/<id>` - Delete a workout

### Workout Exercises
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` - Add exercise to workout

## API Documentation
The API includes comprehensive OpenAPI/Swagger documentation available at:
- `openapi.yaml` - Complete API specification
- View the documentation using Swagger UI or any OpenAPI viewer

## Testing the API
To test the API, you can use tools like curl, Postman, or any HTTP client. The seed file provides sample data for testing.

## Running the Application
Start the Flask development server:
```bash
flask run
```

The API will be available at `http://127.0.0.1:5000`

## Data Models
### Exercise
- `id` (integer, primary key)
- `name` (string, required, unique, min 3 chars)
- `category` (string, required)
- `equipment_needed` (boolean, required)

### Workout
- `id` (integer, primary key)
- `date` (date, required)
- `duration_minutes` (integer, required, must be > 0)
- `notes` (text, optional)

### WorkoutExercise (join table)
- `id` (integer, primary key)
- `workout_id` (integer, foreign key)
- `exercise_id` (integer, foreign key)
- `reps` (integer, optional, must be >= 0)
- `sets` (integer, optional, must be >= 0)
- `duration_seconds` (integer, optional, must be >= 0)

## Validation
The API enforces validation at multiple levels:
- Model-level validation using SQLAlchemy `@validates` decorators
- Schema-level validation using Marshmallow `@validates` decorators
- Database constraints (CheckConstraints) for data integrity

## Error Responses
All errors return JSON in the following format:
```json
{
  "error": "Error type",
  "message": "Detailed error message"
}
```

Status codes:
- 400: Bad request (validation errors)
- 404: Not found
- 500: Internal server error

## Testing
To test the API, you can use tools like curl, Postman, or any HTTP client. The seed file provides sample data for testing.

## Project Structure
```
workout-api/
├── Pipfile
├── README.md
├── .gitignore
└── server/
    ├── app.py         # Flask application and routes
    ├── models.py      # SQLAlchemy models
    ├── schemas.py     # Marshmallow schemas
    └── seed.py        # Database seed script
```
