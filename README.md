# Vasara - Language Learning Flashcard Application
## Overview
Vasara is a Django-based web application designed to help users learn languages through flashcards, organized sets, and interactive quizzes. The application provides a structured approach to language learning with features like spaced repetition, difficulty tracking, and progress monitoring.

## Features
### Flashcard System
- Sets and Boxes : Organize flashcards into sets and boxes for structured learning
- Multimedia Support : Add images to flashcards for visual learning
- Navigation : Easy navigation between flashcards with previous/next functionality
- CRUD Operations : Create, read, update, and delete flashcards, boxes, and sets
### Quiz System
- Interactive Quizzes : Test your knowledge with the built-in quiz system
- Random Questions : Questions are presented in random order
- Immediate Feedback : Get instant feedback on your answers
- Score Tracking : Track your performance with a scoring system
### Learning Features
- Spaced Repetition : Algorithm adjusts review intervals based on performance
- Difficulty Tracking : System tracks difficulty level (0-5) for each flashcard
- Review Scheduling : Automatically schedules next review date based on performance
- Study Mode : Focused study sessions with randomly selected flashcards
### User Management
- User Authentication : Register, login, and logout functionality
- Progress Tracking : Track correct and incorrect answers for each flashcard
- User-specific Progress : Individual progress tracking for each user
## Technical Details
### Built With
- Django 4.2.1 : Python web framework
- Bootstrap : Frontend styling
- SQLite : Database (default)
- JavaScript : For interactive features
### Models
- Language : For storing language information
- Set : Collection of boxes with language associations
- Box : Container for flashcards within a set
- Flashcard : Core learning unit with question, answer, and optional image
- UserProgress : Tracks user performance on individual flashcards
### Key Features Implementation
- Spaced Repetition : Implemented in the update_review_date method of the Flashcard model
- Quiz System : Uses JSON data source for quiz questions and answers
- Dark Mode : Toggle between light and dark themes with localStorage persistence
## Installation
1. Clone the repository
   
   ```
   git clone https://github.com/Tilooo/vasara.
   git
   cd vasara
   ```
2. Create and activate a virtual environment
   
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/MacOS
   ```
3. Install dependencies
   
   ```
   pip install -r requirements.txt
   ```
4. Create a my_settings.py file in the tilo directory with your secret key
   
   ```
   SECRET_KEY = 'your-secret-key-here'
   ```
5. Apply migrations
   
   ```
   python manage.py migrate
   ```
6. Run the development server
   
   ```
   python manage.py runserver
   ```
7. Access the application at http://127.0.0.1:8000/
## Usage
1. Create a Set : Start by creating a set for a specific language or topic
2. Add Boxes : Create boxes within your set to organize flashcards
3. Create Flashcards : Add flashcards with questions and answers to your boxes
4. Study : Navigate through your flashcards to study
5. Take Quizzes : Test your knowledge with the built-in quiz system
## Future Enhancements
- Mobile application support
- API for third-party integrations
- Advanced statistics and learning analytics
- Social features for sharing sets and collaborative learning
- Import/export functionality for flashcard sets
## License
This project is open source and available under the MIT License .

## Acknowledgements
- Django community for the excellent web framework
- Bootstrap for the responsive design components
- All contributors who have helped improve this project
