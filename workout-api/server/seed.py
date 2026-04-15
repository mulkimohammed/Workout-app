from datetime import date, timedelta
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from server.app import app, db
from server.models import Exercise, Workout, WorkoutExercise


def seed_database():
    with app.app_context():
        print("Clearing database...")
        WorkoutExercise.query.delete()
        Workout.query.delete()
        Exercise.query.delete()
        db.session.commit()

        print("Creating exercises...")
        exercises = [
            Exercise(name='Bench Press', category='Chest', equipment_needed=True),
            Exercise(name='Squat', category='Legs', equipment_needed=True),
            Exercise(name='Deadlift', category='Back', equipment_needed=True),
            Exercise(name='Pull Up', category='Back', equipment_needed=False),
            Exercise(name='Push Up', category='Chest', equipment_needed=False),
            Exercise(name='Lunges', category='Legs', equipment_needed=False),
            Exercise(name='Plank', category='Core', equipment_needed=False),
            Exercise(name='Dumbbell Row', category='Back', equipment_needed=True),
            Exercise(name='Shoulder Press', category='Shoulders', equipment_needed=True),
            Exercise(name='Bicep Curl', category='Arms', equipment_needed=True),
        ]
        db.session.add_all(exercises)
        db.session.commit()
        print(f"Created {len(exercises)} exercises")

        print("Creating workouts...")
        base_date = date.today() - timedelta(days=30)
        workouts = [
            Workout(date=base_date, duration_minutes=60, notes='Morning chest workout'),
            Workout(date=base_date + timedelta(days=2), duration_minutes=75, notes='Leg day with heavy squats'),
            Workout(date=base_date + timedelta(days=5), duration_minutes=45, notes='Quick upper body session'),
            Workout(date=base_date + timedelta(days=7), duration_minutes=90, notes='Full body workout'),
            Workout(date=base_date + timedelta(days=10), duration_minutes=50, notes='Cardio and core'),
        ]
        db.session.add_all(workouts)
        db.session.commit()
        print(f"Created {len(workouts)} workouts")

        print("Creating workout exercises...")
        workout_exercises = [
            WorkoutExercise(workout_id=1, exercise_id=1, reps=10, sets=4, duration_seconds=None),
            WorkoutExercise(workout_id=1, exercise_id=5, reps=15, sets=3, duration_seconds=None),
            WorkoutExercise(workout_id=1, exercise_id=8, reps=12, sets=3, duration_seconds=None),
            
            WorkoutExercise(workout_id=2, exercise_id=2, reps=8, sets=5, duration_seconds=None),
            WorkoutExercise(workout_id=2, exercise_id=6, reps=12, sets=3, duration_seconds=None),
            WorkoutExercise(workout_id=2, exercise_id=7, reps=None, sets=3, duration_seconds=60),
            
            WorkoutExercise(workout_id=3, exercise_id=4, reps=8, sets=4, duration_seconds=None),
            WorkoutExercise(workout_id=3, exercise_id=9, reps=10, sets=3, duration_seconds=None),
            WorkoutExercise(workout_id=3, exercise_id=10, reps=12, sets=3, duration_seconds=None),
            
            WorkoutExercise(workout_id=4, exercise_id=3, reps=5, sets=5, duration_seconds=None),
            WorkoutExercise(workout_id=4, exercise_id=1, reps=10, sets=3, duration_seconds=None),
            WorkoutExercise(workout_id=4, exercise_id=2, reps=10, sets=3, duration_seconds=None),
            WorkoutExercise(workout_id=4, exercise_id=7, reps=None, sets=3, duration_seconds=45),
            
            WorkoutExercise(workout_id=5, exercise_id=7, reps=None, sets=3, duration_seconds=90),
            WorkoutExercise(workout_id=5, exercise_id=5, reps=20, sets=3, duration_seconds=None),
        ]
        db.session.add_all(workout_exercises)
        db.session.commit()
        print(f"Created {len(workout_exercises)} workout exercises")

        print("successfully seeded the database!")


if __name__ == '__main__':
    seed_database()