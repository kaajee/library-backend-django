# library-backend-django
Mini library backend service with Django

### Features
<hr>

1. User role (Student, Librarian)
2. Register user
3. User login
4. Book List
5. Borrow book
6. Return book
7. Renew book due date
8. User borrowed history


### Requirements
<hr>

1. Python 3.8+
2. Docker


### Local Configuration
<hr>

1. clone source code from github

2. go to project directory

   ```shell
   cd library-backend-django
   ```

3. create your own project env
   ```shell
   python3 -m venv env
   ```

4. activate your project env
   ``` shell
   source env/bin/activate
   ```

5. go to your project directory and install requirement.txt

   ```shell
   pip install -r requirement.txt
   ```
   
6. run docker compose

   ```shell
   docker compose up -d
   ```

7. migrate all models to database.

   ```shell
   python3 manage.py migrate
   ```
   
8. then run the apps.
   ```shell
   python3 manage.py runserver
   ```

9. create dummy users for testing. default password is `password123`
   ```shell
   python3 manage.py generate_users
   ```
   | Username   | Role      |
   |------------|-----------|
   | student1   | student   |
   | librarian1 | librarian |

10. create dummy books for testing
   ```shell
   python3 manage.py generate_books
   ```

### Run The Test and Coverage
<hr>

1. run test case.
   ```shell
   python3 manage.py test
   ```
   
   the output should be like this:
   ```shell
   Found 13 test(s).
   Creating test database for alias 'default'...
   System check identified no issues (0 silenced).
   .............
   ----------------------------------------------------------------------
   Ran 13 tests in 7.528s
   
   OK
   Destroying test database for alias 'default'...
   ```
   
2. run test coverage.
   ```shell
   coverage run --source='.' manage.py test .
   coverage report
   ```
   
   the output should be like this:
   ```shell
   Found 13 test(s).
   Creating test database for alias 'default'...
   System check identified no issues (0 silenced).
   .............
   ----------------------------------------------------------------------
   Ran 13 tests in 8.033s
   
   OK
   Destroying test database for alias 'default'...
   Name                                    Stmts   Miss  Cover
   -----------------------------------------------------------
   manage.py                                  12      2    83%
   src/__init__.py                             0      0   100%
   src/asgi.py                                 4      4     0%
   src/book/__init__.py                        0      0   100%
   src/book/admin.py                           1      0   100%
   src/book/apps.py                            4      0   100%
   src/book/factory.py                         9      0   100%
   src/book/migrations/0001_initial.py         5      0   100%
   src/book/migrations/__init__.py             0      0   100%
   src/book/models.py                          7      0   100%
   src/book/serializers.py                    21      0   100%
   src/book/tests.py                          39      0   100%
   src/book/views.py                          25      0   100%
   src/borrow/__init__.py                      0      0   100%
   src/borrow/admin.py                         1      0   100%
   src/borrow/apps.py                          4      0   100%
   src/borrow/factory.py                      13      0   100%
   src/borrow/migrations/0001_initial.py       7      0   100%
   src/borrow/migrations/__init__.py           0      0   100%
   src/borrow/models.py                       14      0   100%
   src/borrow/serializers.py                  47      0   100%
   src/borrow/tests.py                        59      0   100%
   src/borrow/views.py                        45      0   100%
   src/iam/__init__.py                         0      0   100%
   src/iam/admin.py                            1      0   100%
   src/iam/apps.py                             4      0   100%
   src/iam/factory.py                         15      0   100%
   src/iam/migrations/0001_initial.py          7      0   100%
   src/iam/migrations/__init__.py              0      0   100%
   src/iam/models.py                           7      0   100%
   src/iam/permissions.py                     12      0   100%
   src/iam/serializers.py                     22      0   100%
   src/iam/tests.py                           48      0   100%
   src/iam/views.py                           38      0   100%
   src/settings.py                            19      0   100%
   src/urls.py                                 8      0   100%
   src/wsgi.py                                 4      4     0%
   -----------------------------------------------------------
   TOTAL                                     502     10    98%
   ```
   