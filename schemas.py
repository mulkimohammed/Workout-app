from marshmallow import Schema, fields, validates, validates_schema, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Exercise, Workout, WorkoutExercise


class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)


class ExerciseCreateSchema(Schema):
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(required=True)

    @validates('name')
    def validate_name(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError("Exercise name cannot be empty")
        if len(value) < 3:
            raise ValidationError("Exercise name must be at least 3 characters long")

    @validates('category')
    def validate_category(self, value):
        if not value or len(value.strip()) == 0:
            raise ValidationError("Exercise category cannot be empty")


class WorkoutExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True, load_only=True)
    exercise_id = fields.Int(required=True, load_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    exercise = fields.Nested(ExerciseSchema, dump_only=True, exclude=('equipment_needed',))


class WorkoutExerciseCreateSchema(Schema):
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    @validates('reps')
    def validate_reps(self, value):
        if value is not None and value < 0:
            raise ValidationError("Reps must be non-negative")

    @validates('sets')
    def validate_sets(self, value):
        if value is not None and value < 0:
            raise ValidationError("Sets must be non-negative")

    @validates('duration_seconds')
    def validate_duration_seconds(self, value):
        if value is not None and value < 0:
            raise ValidationError("Duration seconds must be non-negative")


class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
        include_fk = True

    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


class WorkoutCreateSchema(Schema):
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    @validates('duration_minutes')
    def validate_duration_minutes(self, value):
        if value is None:
            raise ValidationError("Duration minutes is required")
        if value <= 0:
            raise ValidationError("Duration minutes must be greater than 0")

    @validates('date')
    def validate_date(self, value):
        if value is None:
            raise ValidationError("Date is required")
