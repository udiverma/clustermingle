import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('backend/riddle/db/RiddleDB.db')
cursor = conn.cursor()

# Create the riddles table
cursor.execute('''
CREATE TABLE IF NOT EXISTS riddles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    riddle TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    correct_option TEXT NOT NULL,
    difficulty TEXT,
    category TEXT
)
''')

# List of 25+ riddle questions with answer choices
riddles = [
    ("I'm tall when I'm young and short when I'm old. What am I?", "Candle", "Tree", "Shadow", "A", "Easy", "Logic"),
    ("What has keys but can't open locks?", "Keyboard", "Map", "Lockpick", "A", "Easy", "IT"),
    ("I speak without a mouth and hear without ears. What am I?", "Wind", "Echo", "River", "B", "Medium", "Logic"),
    ("The more you take, the more you leave behind. What am I?", "Footsteps", "Time", "Memory", "A", "Medium", "Logic"),
    ("I can travel around the world without leaving my corner. What am I?", "Postage Stamp", "Compass", "Internet", "A", "Easy", "Business"),
    ("What is always coming but never arrives?", "Deadline", "Tomorrow", "Sunrise", "B", "Easy", "Logic"),
    ("What can you hold in your left hand but not in your right?", "Right Elbow", "Left Thumb", "Left Hand", "A", "Medium", "Logic"),
    ("If I have it, I don't share it. If I share it, I don't have it. What am I?", "Secret", "Idea", "Dream", "A", "Medium", "Logic"),
    ("What has a head, a tail, but no body?", "Coin", "Snake", "Arrow", "A", "Easy", "Logic"),
    ("I start with an 'e', end with an 'e', and contain a letter. What am I?", "Envelope", "Eye", "Embrace", "A", "Hard", "Logic"),
    ("What has one eye but can't see?", "Storm", "Needle", "Mountain", "B", "Medium", "Logic"),
    ("I’m not alive, but I can grow. I don’t have lungs, but I need air. What am I?", "Virus", "Fire", "Plant", "B", "Hard", "Logic"),
    ("What comes once in a minute, twice in a moment, but never in a thousand years?", "M", "Time", "Chance", "A", "Hard", "Logic"),
    ("What building has the most stories?", "Library", "Bookstore", "Museum", "A", "Easy", "Business"),
    ("You see me once in June, twice in November, and not at all in May. What am I?", "Letter E", "Letter N", "Letter V", "A", "Hard", "Logic"),
    ("What can run but never walks, has a mouth but never talks?", "River", "Clock", "Wind", "A", "Medium", "Logic"),
    ("What belongs to you but others use it more than you do?", "Money", "Name", "Car", "B", "Easy", "Logic"),
    ("What has a neck but no head?", "Shirt", "Bottle", "River", "B", "Easy", "Logic"),
    ("The more of this there is, the less you see. What is it?", "Light", "Water", "Darkness", "C", "Easy", "Logic"),
    ("If you drop me, I’m sure to crack, but give me a smile and I’ll always smile back. What am I?", "Mirror", "Egg", "Glass", "A", "Medium", "Logic"),
    ("I can only live where there is light, but I die if the light shines on me. What am I?", "Moon", "Shadow", "Oxygen", "B", "Hard", "Logic"),
    ("What has many teeth but can’t bite?", "Zipper", "Comb", "Saw", "B", "Easy", "Logic"),
    ("Forward I’m heavy, but backward I’m not. What am I?", "Ton", "Rock", "Lead", "A", "Medium", "Logic"),
    ("I am taken from a mine, and shut up in a wooden case, from which I am never released, and yet I am used by almost every person. What am I?", "Coal", "Pencil", "Diamond", "B", "Hard", "Business"),
    ("I am not alive, but I grow; I don’t have lungs, but I need air. I don’t have a mouth, but water kills me. What am I?", "Plant", "Fire", "Moss", "B", "Medium", "Logic"),
    ("I am invisible, weigh nothing, and if you put me in a barrel, it will make it lighter. What am I?", "Hole", "Gas", "Air", "A", "Hard", "Logic"),
    ("What can fill a room but takes up no space?", "Light", "Air", "Shadow", "A", "Easy", "Logic")
]

# Insert riddles into the database
cursor.executemany('''
INSERT INTO riddles (riddle, option_a, option_b, option_c, correct_option, difficulty, category) 
VALUES (?, ?, ?, ?, ?, ?, ?)
''', riddles)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database with 25+ riddle questions created successfully.")