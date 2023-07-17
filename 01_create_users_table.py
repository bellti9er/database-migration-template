"""
Create users table 
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
         CREATE TABLE users (
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(200) NOT NULL,
            PRIMARY KEY(id)
        );
        """
    )
]
