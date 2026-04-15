from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workouts = db.relationship('WorkoutExercise', back_populates='exercise')

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 2", name='exercise_name_length_check'),
    )

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("invalid:Exercise name cannot be empty")
        if len(name) < 3:
            raise ValueError("Exercise name must be at least 3 characters long")
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if not category or len(category.strip()) == 0:
            raise ValueError("Exercise category cannot be empty")
        return category.strip()

    @validates('equipment_needed')
    def validate_equipment_needed(self, key, equipment_needed):
        if equipment_needed is None:
            raise ValueError("Equipment needed must be specified")
        return equipment_needed

    def __repr__(self):
        return f'<Exercise {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name='workout_duration_positive'),
    )

    @validates('date')
    def validate_date(self, key, date):
        if date is None:
            raise ValueError("Workout date cannot be empty")
        return date

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes is None:
            raise ValueError("Duration minutes cannot be empty")
        if duration_minutes <= 0:
            raise ValueError("Duration minutes must be greater than 0")
        return duration_minutes

    def __repr__(self):
        return f'<Workout {self.id} on {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    workout = db.relationship('Workout', back_populates='exercises')
    exercise = db.relationship('Exercise', back_populates='workouts')

    __table_args__ = (
        CheckConstraint("reps IS NULL OR reps >= 0", name='workout_exercise_reps_nonnegative'),
        CheckConstraint("sets IS NULL OR sets >= 0", name='workout_exercise_sets_nonnegative'),
        CheckConstraint("duration_seconds IS NULL OR duration_seconds >= 0", name='workout_exercise_duration_nonnegative'),
    )

    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps < 0:
            raise ValueError("Reps must be non-negative")
        return reps

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets < 0:
            raise ValueError("Sets must be non-negative")
        return sets

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, duration_seconds):
        if duration_seconds is not None and duration_seconds < 0:
            raise ValueError("Duration seconds must be non-negative")
        return duration_seconds

    def __repr__(self):
        return f'<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>'