from django.shortcuts import render, get_object_or_404, redirect
from tot.models import Set, Box, Flashcard
from .forms import SetForm, BoxForm, FlashcardForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import json
import random
from django.contrib import messages


def home(request):
    return render(request, 'tot/home.html')


def set_list(request):
    sets = Set.objects.all()
    return render(request, 'tot/set_list.html', {'sets': sets})


def set_detail(request, set_id):
    set_obj = get_object_or_404(Set, pk=set_id)
    boxes = set_obj.box_set.all()
    context = {
        'set': set_obj,
        'boxes': boxes,
    }
    return render(request, 'tot/set_detail.html', context)


def box_detail(request, set_id, box_id):
    set_obj = get_object_or_404(Set, pk=set_id)
    box = get_object_or_404(Box, pk=box_id, set=set_obj)
    flashcards = box.flashcard_set.all()

    context = {
        'set': set_obj,
        'box': box,
        'flashcards': flashcards,
    }
    return render(request, 'tot/box_detail.html', context)


def flashcard_detail(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    box = flashcard.box

    flashcards = box.flashcard_set.order_by('id')
    flashcard_ids = [f.id for f in flashcards]
    current_index = flashcard_ids.index(flashcard_id)

    previous_flashcard = flashcards[current_index - 1] if current_index > 0 else None
    next_flashcard = flashcards[current_index + 1] if current_index < len(flashcards) - 1 else None

    context = {
        'flashcard': flashcard,
        'previous_flashcard': previous_flashcard,
        'next_flashcard': next_flashcard,
    }
    return render(request, 'tot/flashcard_detail.html', context)


def create_set(request):
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tot:set_list')
    else:
        form = SetForm()
    return render(request, 'tot/create_set.html', {'form': form})


@login_required
def create_box(request, set_id):
    set_obj = get_object_or_404(Set, pk=set_id)
    if request.method == 'POST':
        form = BoxForm(request.POST)
        if form.is_valid():
            box = form.save(commit=False)
            box.set = set_obj
            box.save()
            return redirect('tot:set_detail', set_id=set_id)
    else:
        form = BoxForm()
    context = {
        'form': form,
        'set': set_obj,
    }
    return render(request, 'tot/create_box.html', context)


def create_flashcard(request, box_id):
    box_obj = get_object_or_404(Box, pk=box_id)
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.box = box_obj
            flashcard.save()
            return redirect('tot:box_detail', set_id=box_obj.set.id, box_id=box_id)
    else:
        form = FlashcardForm()
    return render(request, 'tot/create_flashcard.html', {'form': form, 'box': box_obj})


def edit_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    box_obj = flashcard.box
    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('tot:box_detail', set_id=box_obj.set.id, box_id=box_obj.id)
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'tot/edit_flashcard.html', {'form': form, 'box': box_obj})


def delete_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, pk=flashcard_id)
    box_obj = flashcard.box
    if request.method == 'POST':
        flashcard.delete()
        return redirect('tot:box_detail', set_id=box_obj.set.id, box_id=box_obj.id)
    return render(request, 'tot/delete_flashcard.html', {'flashcard': flashcard})


@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tot:set_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def quiz_view(request):
    # The contents of the JSON file
    try:
        with open('quiz_data/quiz.json', 'r') as file:
            quiz_data = json.load(file)
    except FileNotFoundError:
        # Handle case where JSON file doesn't exist
        return render(request, 'quiz/quiz_error.html', {'message': 'Quiz data file not found.'})
    except json.JSONDecodeError:
        # Handle case where JSON is invalid
        return render(request, 'quiz/quiz_error.html', {'message': 'Error decoding quiz data.'})

    quiz_name = quiz_data.get('quiz_name', 'Quiz')
    questions = quiz_data.get('questions', [])

    if not questions:
        # Handle case where the JSON file has no questions
        return render(request, 'quiz/quiz_error.html', {'message': 'No questions found in the quiz data.'})

    # Initializes session variables if they don't exist
    if 'quiz_score' not in request.session:
        request.session['quiz_score'] = 0
    if 'questions_answered' not in request.session:
        request.session['questions_answered'] = 0
    if 'asked_question_texts' not in request.session:  # Storing texts to avoid re-asking by content
        request.session['asked_question_texts'] = []

    if request.method == 'POST':
        # --- PROCESS ANSWER ---
        try:
            # This question_id is the index of the question that was *just answered*
            answered_question_id_str = request.POST.get('question_id')
            if answered_question_id_str is None:
                # Handle error: question_id not submitted
                return render(request, 'quiz/quiz_error.html', {'message': 'Missing question ID in submission.'})

            answered_question_id = int(answered_question_id_str)
            selected_answer = request.POST.get('answer')

            # Check if the answered_question_id is valid (it should be, as it was displayed)
            if 0 <= answered_question_id < len(questions):
                question_just_answered = questions[answered_question_id]
                correct_answer = question_just_answered['correct_answer']
                is_correct = (selected_answer == correct_answer)
                if is_correct:
                    request.session['quiz_score'] += 1
            else:
                is_correct = None

            request.session['questions_answered'] += 1

        except (ValueError, TypeError):
            # Handle error if question_id is not a valid integer
            return render(request, 'quiz/quiz_error.html', {'message': 'Invalid question ID format.'})

        # --- DETERMINE NEXT QUESTION OR END QUIZ ---

        # Logic to pick next UNASKED question
        asked_texts = request.session.get('asked_question_texts', [])
        available_questions_for_next = []
        for i, q_data in enumerate(questions):
            if q_data['question_text'] not in asked_texts:
                available_questions_for_next.append({'index': i, 'data': q_data})

        if not available_questions_for_next:
            # All questions have been asked OR no more unique questions to ask
            # Quiz is over
            score = request.session['quiz_score']
            total_questions_in_quiz = len(questions)  # Or how many you intended to ask

            # Clear session for next quiz attempt
            del request.session['quiz_score']
            del request.session['questions_answered']
            del request.session['asked_question_texts']
            # request.session.modified = True

            return render(request, 'quiz/quiz_result.html', {
                'quiz_name': quiz_name,
                'score': score,
                'total_questions': total_questions_in_quiz
            })
        else:
            # Select next question randomly from available ones
            next_question_info = random.choice(available_questions_for_next)
            next_question_data = next_question_info['data']
            next_question_id_for_template = next_question_info[
                'index']  # This is the actual index in the 'questions' list

            # Add to asked list for next round
            asked_texts.append(next_question_data['question_text'])
            request.session['asked_question_texts'] = asked_texts
            request.session.modified = True

            context = {
                'quiz_name': quiz_name,
                'question': next_question_data,
                'question_id': next_question_id_for_template,  # ID/index of the question being displayed NOW
                'feedback_is_correct': is_correct,  # Feedback on the *previous* question
                'feedback_correct_answer': correct_answer if is_correct is not None else None,
                'feedback_question_text': question_just_answered['question_text'] if is_correct is not None else None
            }
            return render(request, 'quiz/quiz.html', context)

    else:  # GET request (start of quiz or direct navigation)
        # Reset session for a new quiz attempt on GET
        request.session['quiz_score'] = 0
        request.session['questions_answered'] = 0
        request.session['asked_question_texts'] = []
        request.session.modified = True

        # --- DISPLAY FIRST QUESTION ---
        if not questions:
            return render(request, 'quiz/quiz_error.html', {'message': 'No questions to display.'})

        # Get a random first question
        first_question_data = random.choice(questions)
        first_question_id = questions.index(first_question_data)  # Get its actual index

        # Adds to asked list
        request.session['asked_question_texts'] = [first_question_data['question_text']]
        request.session.modified = True

        context = {
            'quiz_name': quiz_name,
            'question': first_question_data,
            'question_id': first_question_id,  # ID/index of the question being displayed
        }
        return render(request, 'quiz/quiz.html', context)


def quiz_result(request):
    if request.method == 'POST':
        # Get the user's answers from the submitted form
        user_answers = request.POST.getlist('answer')  # Assuming the user's answers are submitted as a list

        # Read the contents of the JSON file
        with open('quiz_data/quiz.json', 'r') as file:
            quiz_data = json.load(file)

        # Access the quiz data
        quiz_name = quiz_data['quiz_name']
        questions = quiz_data['questions']
        correct_answers = [question['correct_answer'] for question in questions]

        # Calculate the score based on the user's answers
        score = 0
        for user_answer, correct_answer in zip(user_answers, correct_answers):
            if user_answer == correct_answer:
                score += 1

        context = {
            'score': score,
            'quiz_name': quiz_name,
        }

        return render(request, 'quiz/quiz_result.html', context)


def study_mode(request, set_id):
    set_obj = get_object_or_404(Set, pk=set_id)
    flashcards = Flashcard.objects.filter(box__set=set_obj).order_by('?')[:10]  # Random 10 cards
    
    context = {
        'set': set_obj,
        'flashcards': flashcards,
        'current_index': 0,
    }
    return render(request, 'tot/study_mode.html', context)
