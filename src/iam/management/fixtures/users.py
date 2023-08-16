from django.contrib.auth.models import User

from src.iam.models import LibraryUser

DEFAULT_PASSWORD = 'password123'


def create_users():
    # Create Student
    student, _ = User.objects.get_or_create(username="student1")
    student.set_password(DEFAULT_PASSWORD)
    LibraryUser.objects.create(
        user=student,
        is_student=True,
        is_librarian=False
    )
    print(f' [*] Create new student {student.username}')

    # Create Librarian
    librarian, _ = User.objects.get_or_create(username="librarian1")
    librarian.set_password(DEFAULT_PASSWORD)
    LibraryUser.objects.create(
        user=librarian,
        is_student=False,
        is_librarian=True
    )
    print(f' [*] Create new librarian {librarian.username}')
