Homework 4 Feedback
==================

Commit graded:  6ae8b06e51fb4f48ba843f0f5a5e0a98f828262a

### Incremental development using Git (8/10)

-2, Only files necessary for your homework solution only should be committed.  Files like `.idea` are not necessary.  Ideally you should commit only source files, not derived files, to your version control repository.  If you find yourself accidentally committing derived files to your repository you should probably add the appropriate file types to your .gitignore file ([LINK TO GITIGNORE]).  See [https://help.github.com/articles/ignoring-files/] for details.

### Fulfilling the grumblr specification (30/30)

-0, When changing passwords, it is a good idea to have people confirm their old and new passwords.

### Proper Form-based validation (17/20)

-3, Validation for all forms should be replaced with that of Django Forms.

### Appropriate use of web application technologies (58/60)

#### Template Inheritance and Reverse Urls (10/10)

#### Image upload (5/5)

#### Email Sending (5/5)

#### Basic ORM Usage (20/20)

-0.1, The `related_name` for your many-to-many relationships do not make sense. The `related_name` is used as the name for the relation from the related model back to this one. For example, a good `related_name` for a 'followers' relation would be 'following'.

#### Advanced ORM Usage (10/10)

#### Routing and Requests (8/10)

-2, You should modularize your Django projects by using application-specific `urls.py` files in each application directory, and use your project-wide `urls.py` file to include each application's routes.

### Design

### Additional Information

---
#### Total score (113/120)
---
Graded by: Kelly Cheng (kuangchc@andrew.cmu.edu)

To view this file with formatting, visit the following page: https://github.com/CMU-Web-Application-Development/zhiqiaol/blob/master/grades/homework4.md