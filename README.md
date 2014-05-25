This little website is my final project for CS275 at Oregon State University.
It is a (relatively) simple web-based library cataloging application that you
probably shouldn't use.

## Install

- Clone the repo
  ```
git clone https://github.com/zeeman/cs275-final-library.git
cd cs275-final-library
  ```

- (optional) Set up virtualenv
    ```
virtualenv .env
    ```

- Install requirements
    ```
pip install -r requirements.txt
    ```

- Create an empty MySQL database.

- Configure settings
    - Copy the template
        ```
mv /application/settings.py-dist /application/settings.py
        ```
    - Replace every instance of `FIXME` in /application/settings.py

- Use `/db/schema.sql` to create your database.


## Top Level File and Directory Overview

- *base* - Framework classes and interfaces, used by the core application.
    - *model.py* - Defines a standard interface for Models, which perform SQL
    queries and handle domain logic.
    - *viewgenerator.py* - Small framework for generating views.
- *core* - Everything central to the application.
    - *models.py* - Application data models.
    - *settings.py* - User settings.
    - *settings.py-dist* - Template settings file.
- *db* - Database stuff, including the schema definition.
- *docs* - Future site of great documentation!
- *static* - Static resources for the site.
- *templates* - Jinja2 templates.
- *utils* - Some basic helper functions.
- *app.py* - Basic site runner, loads config and starts the dev server if you
    run the file directly.