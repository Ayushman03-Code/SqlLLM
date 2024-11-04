import sqlite3
import random

try:
    # Connect to SQLite database
    connection = sqlite3.connect("student.db")
    cursor = connection.cursor()

    # Create table if it doesn't exist
    table_info = """
    CREATE TABLE IF NOT EXISTS STUDENT (
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        SECTION VARCHAR(25),
        MARKS INT
    ); 
    """
    cursor.execute(table_info)

    # Insert 110 random records
    names = ["Ayushman", "Alex", "Priya", "Sara", "John", "Nina", "Leo", "Maya", "Anil", "Emma", "Chris", "Raj", "Kim", "Sam", "Lily"]
    classes = ["Generative AI", "Machine Learning", "Data Science", "Deep Learning", "Robotics", "Computer Vision", "NLP", "Big Data", "Cybersecurity", "AI"]
    sections = ["A", "B", "C"]

    for _ in range(110):
        name = random.choice(names)
        class_name = random.choice(classes)
        section = random.choice(sections)
        marks = random.randint(70, 100)

        cursor.execute("INSERT INTO STUDENT (Name, Class, Section, Marks) VALUES (?, ?, ?, ?)", (name, class_name, section, marks))

    # Display all the records
    print("The inserted records are:")
    cursor.execute("SELECT * FROM STUDENT")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    # Save changes
    connection.commit()

except sqlite3.Error as error:
    print("Error occurred:", error)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
