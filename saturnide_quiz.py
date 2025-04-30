#!/usr/bin/env python3
"""
Saturnide-inspired Quiz
A simple console quiz with Saturnide styling and animations based on results
"""

import os
import sys
import time
import random
import threading
import subprocess
from typing import Dict, List

# Colors for Saturnide styling
try:
    from colorama import init, Fore, Style
    init()
    SATURNIDE_GREEN = Fore.GREEN
    RESET = Style.RESET_ALL
except ImportError:
    # Fallback if colorama is not available
    SATURNIDE_GREEN = ""
    RESET = ""

# Get terminal width for centering text
try:
    TERM_WIDTH = os.get_terminal_size().columns
except (AttributeError, OSError):
    TERM_WIDTH = 80
    
# 8-bit music notes using beep (if available)
# Each tuple represents (frequency in Hz, duration in seconds)
HAPPY_MUSIC = [
    (262, 0.2), (294, 0.2), (330, 0.2), (349, 0.2),  # C D E F
    (392, 0.4), (349, 0.2), (330, 0.2),              # G F E
    (294, 0.4), (262, 0.2), (294, 0.2),              # D C D
    (330, 0.4), (294, 0.2), (262, 0.6)               # E D C
]

SCARY_MUSIC = [
    (130, 0.3), (123, 0.3), (116, 0.3),  # Low notes descending
    (110, 0.6), (0, 0.2),                # Longer note, small pause
    (110, 0.1), (0, 0.1), (110, 0.1),    # Staccato notes
    (0, 0.1), (110, 0.4), (0, 0.2),      # Note with pause
    (98, 0.6), (87, 0.8)                 # Final descending notes
]

GLITCH_MUSIC = [
    (440, 0.05), (0, 0.05), (880, 0.05), (0, 0.05),  # Rapid high notes
    (220, 0.05), (0, 0.05), (110, 0.05), (0, 0.05),  # Rapid low notes
    (660, 0.02), (0, 0.02), (770, 0.02), (0, 0.02),  # Very rapid notes
    (880, 0.1), (0, 0.05), (440, 0.3)                # Final pulse
]

# Always make beep sounds available (visual alternative will be used)
CAN_BEEP = True


class SaturnideQuiz:
    """Saturnide-themed quiz with animations"""

    def __init__(self):
        """Initialize the quiz with questions and setup"""
        self.score = 0
        self.user_choices = []  # Track all user choices
        self.questions = [
            {
                "question": "Are you a planet?",
                "options": ["Yes", "No", "Maybe", "I am a celestial body"],
                "answer": 3,  # "I am a celestial body" is now the correct answer
                "special_message_correct": "You are right. You are always right.",
                "special_message_incorrect": "Incorrect, every being is a celestial body"
            },
            {
                "question": "Are you having trouble sleeping?",
                "options": ["Yes", "No", "Sometimes", "I never sleep"],
                "answer": 0,  # Yes
                "special_message": "Have you tried red wine?"
            },
            {
                "question": "Why haven't you reached out to your child today?",
                "options": ["I did", "I'm busy", "I forgot", "I don't have children"],
                "answer": 0,  # I did
                "special_behavior": "always_incorrect",
                "special_message": "Incorrect, she is not your child. But you owe child support.",
                "follow_up_message": "Error/system.sat: There is a problem with Zoé's programming.",
                "glitch_after": True
            },
            {
                "question": "What is Zoé?",
                "options": ["She's a little bitch", "She's a little bitch", "She's a little bitch", 
                           "She's a little bitch", "She's a little bitch", "She's a little bitch", 
                           "She's a little bitch", "She's a little bitch", "She's a little bitch", 
                           "She's a little bitch", "She's a little bitch", "She's a little bitch", 
                           "She's a little bitch", "She's a little bitch", "She's a little bitch", 
                           "She's a little bitch", "She's a little bitch", "She's a little bitch", 
                           "She's a little bitch", "She's a little bitch"],
                "answer": 0,  # Any answer is correct
                "all_correct": True,
                "hide_question_number": True,
                "slow_response": True,
                "option_display_speed": 0.1,  # Display options faster
                "special_message_correct": "YES SHE'S A FUCKING LITTLE BITCH, YOU SHOULD THROW THAT CELLPHONE THROUGH THE WINDOW, THROW IT, NOW.",
                "all_caps": True,
                "pause_at_punctuation": True
            },
            {
                "question": "Now that life is a little bit quieter, tell me, why are you trying to be someone else?",
                "options": ["I'm not", "Identity is fluid", "To fit in", "For survival"],
                "answer": 0,  # Any answer is fine
                "all_correct": True,
                "hide_question_number": True,
                "pause_at_commas": True,
                "special_behavior": "custom_message",
                "special_message": "Interesting, tell me more. I'm just joking, you should try to sleep. Hammers are a good and effective way to make human sleep.",
                "pause_at_punctuation": True,
                "show_hammer_animation": True
            },
            {
                "question": "You are now sleeping. Life is easy, again. You are in the forest with your dog, what is your dog's name? You are also with a Woman. Is she the love of your life? What is the name of your dog and of the love of your life?",
                "options": [
                    "Liesse and Fleur", "Camille and Milange", "Zoé and Maxime", 
                    "Eric and Hector", "Jocelyn and Liesse", "Fleur and Camille"
                ],
                "custom_text_input": True,  # Allow both options and custom text
                "option_message": "Or type your own answer:",
                "hide_question_number": True,
                "pause_at_commas": True,
                "custom_ending": True,
                "dramatic_ending": True,
                "ending_message": "YOU'VE BEEN SATURN'D",
                "final_message": "Wake up Neegan... You. Are. In. A. Movie... And. The. Movie. Is. About. To. End.",
                "glitch_input": True,
                "naughty_boy_text": "NAUGHTY BOY"
            }
        ]

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def type_saturnide_style(self, text: str, delay: float = 0.03, newline: bool = True):
        """Print text character by character with Saturnide styling"""
        for char in text:
            sys.stdout.write(f"{SATURNIDE_GREEN}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(delay)
        if newline:
            print()

    def center_text(self, text: str) -> str:
        """Center text in terminal"""
        return text.center(TERM_WIDTH)

    def display_intro(self):
        """Display the Saturnide-themed intro"""
        self.clear_screen()
        
        # Display ASCII art header
        header = """
         ███████╗ █████╗ ████████╗██╗   ██╗██████╗ ███╗   ██╗██╗██████╗ ███████╗
         ██╔════╝██╔══██╗╚══██╔══╝██║   ██║██╔══██╗████╗  ██║██║██╔══██╗██╔════╝
         ███████╗███████║   ██║   ██║   ██║██████╔╝██╔██╗ ██║██║██║  ██║█████╗  
         ╚════██║██╔══██║   ██║   ██║   ██║██╔══██╗██║╚██╗██║██║██║  ██║██╔══╝  
         ███████║██║  ██║   ██║   ╚██████╔╝██║  ██║██║ ╚████║██║██████╔╝███████╗
         ╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═════╝ ╚══════╝
                              QUIZ SYSTEM
        """
        
        for line in header.split('\n'):
            print(f"{SATURNIDE_GREEN}{line}{RESET}")
        
        time.sleep(1)
        
        welcome_text = "\nWelcome to the Saturnides Diagnostic Quiz"
        self.type_saturnide_style(self.center_text(welcome_text), delay=0.05)
        
        time.sleep(0.5)
        
        intro_text = [
            "Checking Saturn's connection...",
            "Signal established with Saturnide...",
            "Answer the following questions truthfully.",
            "The fabric of your reality depends on it."
        ]
        
        for line in intro_text:
            time.sleep(0.8)
            self.type_saturnide_style(self.center_text(line), delay=0.03)
        
        time.sleep(1)
        input(f"{SATURNIDE_GREEN}Press Enter to continue...{RESET}")

    def type_with_pauses(self, text: str, pause_at_punctuation=False):
        """Type text with pauses at punctuation"""
        for i, char in enumerate(text):
            sys.stdout.write(f"{SATURNIDE_GREEN}{char}{RESET}")
            sys.stdout.flush()
            
            if pause_at_punctuation and char in [',', '.']:
                time.sleep(1.0)  # 1 second pause at commas and periods
            else:
                time.sleep(0.03)  # Normal typing speed
                
        print()  # Add newline at end
    
    def display_glitch_fullscreen(self, text, duration=7):
        """Display a full-screen glitch effect with the given text"""
        self.clear_screen()
        chars = "▓▒░▒▓█▀▄▌▐ ░▓▒ÔÕÖØ#@!?/\\|[]{}=-+*&^%$#@!~`<>.,;:'\""
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                for y in range(20):  # Display 20 lines
                    line = ""
                    for x in range(TERM_WIDTH):
                        # Insert the text in random positions
                        if random.random() < 0.1:
                            # 10% chance to insert a character from the input text
                            if text and len(text) > 0:
                                char_idx = random.randint(0, len(text) - 1)
                                line += text[char_idx]
                            else:
                                line += random.choice(chars)
                        else:
                            line += random.choice(chars)
                    
                    print(f"{SATURNIDE_GREEN}{line}{RESET}")
                
                time.sleep(0.2)
                self.clear_screen()
        except KeyboardInterrupt:
            pass
        
        self.clear_screen()
    
    def display_hammer_animation(self):
        """Display a hammer hitting a skull animation"""
        self.clear_screen()
        
        frames = [
            """
        _________
       /         \\
      /  HAMMER   \\      .-.-.-.
      \\_________/       (  o o  )
           |            |   ^   |
           |             \\_____/
           |
           V
            """,

            """
        
        _________
       /         \\
      /  HAMMER   \\
      \\_________/       
           |            .-.-.-.
           |           (  X X  )
           V            \\_____/
                       
            """,

            """
        
        
        
        _________
       /         \\      .-.-.-.
      /  HAMMER   \\    (  X X  )
      \\_________/       \\_____/
           |
            """,

            """
        
        
        
                         .-.-.-.
        _________       (  X X  )
       /  HAMMER  \\      \\_____/
      \\__________/
            """,
        ]
        
        for _ in range(4):  # 4 hits as requested
            for frame in frames:
                self.clear_screen()
                for line in frame.split('\n'):
                    print(f"{SATURNIDE_GREEN}{self.center_text(line)}{RESET}")
                time.sleep(0.3)
        
        self.clear_screen()
        time.sleep(0.5)

    def display_question(self, question_data: Dict, question_num: int):
        """Display a question with options and get user answer"""
        self.clear_screen()
        
        # Show header with question number unless we're told to hide it
        if not ("hide_question_number" in question_data and question_data["hide_question_number"]):
            header = f"Question {question_num}/{len(self.questions)}"
            print(f"{SATURNIDE_GREEN}{self.center_text(header)}{RESET}")
            print()
        
        # Display the question with pauses at commas if specified
        if "pause_at_commas" in question_data and question_data["pause_at_commas"]:
            question_text = self.center_text(question_data["question"])
            sys.stdout.write(f"{SATURNIDE_GREEN}")
            for char in question_text:
                sys.stdout.write(char)
                sys.stdout.flush()
                if char == ',':
                    time.sleep(1.0)  # 1 second pause at commas
                else:
                    time.sleep(0.02)  # Normal typing speed
            sys.stdout.write(f"{RESET}\n")
        else:
            self.type_saturnide_style(question_data["question"], delay=0.02)
        print()
        
        # Check if this is a text input only question
        if "text_input" in question_data and question_data["text_input"]:
            user_input = input(f"{SATURNIDE_GREEN}Enter your answer: {RESET}")
            
            # Display glitch effect with the input text
            if "glitch_input" in question_data and question_data["glitch_input"]:
                self.display_glitch_fullscreen(user_input, duration=7)
            
            # Any input is considered correct for this type of question
            self.score += 1
            return True, user_input
        
        # For custom input questions with both options and text input
        if "custom_text_input" in question_data and question_data["custom_text_input"]:
            # Display options at faster speed if specified
            delay = 0.1 if "option_display_speed" in question_data else 0.3
            
            for i, option in enumerate(question_data["options"]):
                time.sleep(delay)
                self.type_saturnide_style(f"{i+1}. {option}", delay=0.01)
            
            print()
            
            # Display message for custom input
            if "option_message" in question_data:
                self.type_saturnide_style(question_data["option_message"], delay=0.02)
                print()
            
            # Get user input - could be a choice or custom text
            user_input = input(f"{SATURNIDE_GREEN}Your answer: {RESET}")
            self.last_raw_input = user_input  # Store raw input to check for "6"
            
            # Try to parse as a number for option selection
            selected_option = None
            try:
                choice = int(user_input)
                if 1 <= choice <= len(question_data["options"]):
                    selected_option = question_data["options"][choice-1]
            except ValueError:
                # Not a number, treat as custom text
                pass
                
            # Determine what to display in the glitch
            glitch_text = selected_option if selected_option else user_input
            
            # For custom answers, use the "naughty boy" text
            if not selected_option and "naughty_boy_text" in question_data:
                self.display_glitch_fullscreen(question_data["naughty_boy_text"], duration=7)
            # Otherwise use the selected option or custom text
            elif "glitch_input" in question_data and question_data["glitch_input"]:
                self.display_glitch_fullscreen(glitch_text, duration=7)
            
            # Any input is considered correct for this type of question
            self.score += 1
            return True, glitch_text
            
        # Normal multiple choice questions
        # Display options at faster speed if specified
        delay = 0.1 if "option_display_speed" in question_data else 0.3
        
        for i, option in enumerate(question_data["options"]):
            time.sleep(delay)
            self.type_saturnide_style(f"{i+1}. {option}", delay=0.01)
        
        print()
        
        # Get user input for multiple choice
        while True:
            try:
                user_input = input(f"{SATURNIDE_GREEN}Enter your choice (1-{len(question_data['options'])}): {RESET}")
                self.last_raw_input = user_input  # Store raw input to check for "6"
                
                choice = int(user_input)
                
                # Special case: Accept 6 as a valid choice for secret ending
                if user_input == "6":
                    # Determine which question this is by position in the questions list
                    question_position = -1
                    for q_idx, q in enumerate(self.questions):
                        if q == question_data:
                            question_position = q_idx
                            break
                    
                    # Display appropriate glitch message based on question number
                    glitch_messages = [
                        "C'est lourd Philippe!",
                        "Tu sais que je suis pas juste un trou?",
                        "Tu penses juste à ca hein!!?!!",
                        "Est ce que tu me trouve intelligente ?",
                        "Je sers pas juste à ca tu sais!",
                        "Tu penses toujours juste au S6X"
                    ]
                    
                    # Show quick glitch with message
                    if 0 <= question_position < len(glitch_messages):
                        self.display_flicker_effect(glitch_messages[question_position], duration=3)
                        
                    # Choose a valid option from the available choices to continue
                    choice = 1  # Default to first option (will be treated as incorrect)
                    break
                
                # Normal case: Check if choice is in valid range
                if 1 <= choice <= len(question_data["options"]):
                    break
                    
                print(f"{SATURNIDE_GREEN}Invalid choice. Try again.{RESET}")
            except ValueError:
                print(f"{SATURNIDE_GREEN}Please enter a number.{RESET}")
        
        # Handle special behaviors
        if "special_behavior" in question_data:
            if question_data["special_behavior"] == "always_incorrect":
                # Display custom incorrect message
                self.type_saturnide_style(self.center_text(question_data["special_message"]), delay=0.02)
                time.sleep(1.5)
                
                # Show the follow-up message if it exists
                if "follow_up_message" in question_data:
                    print()
                    self.type_saturnide_style(self.center_text(question_data["follow_up_message"]), delay=0.02)
                    time.sleep(2)
                
                # Show glitch effect if requested
                if "glitch_after" in question_data and question_data["glitch_after"]:
                    self.display_flicker_effect("ERROR", duration=2)
                
                return False, None
            elif question_data["special_behavior"] == "custom_message":
                # Display custom message with pauses at punctuation if specified
                if "pause_at_punctuation" in question_data and question_data["pause_at_punctuation"]:
                    message = self.center_text(question_data["special_message"])
                    sys.stdout.write(f"{SATURNIDE_GREEN}")
                    for char in message:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        if char in ['.', ',']:
                            time.sleep(1.0)  # 1 second pause at punctuation
                        else:
                            time.sleep(0.02)  # Normal typing speed
                    sys.stdout.write(f"{RESET}\n")
                else:
                    self.type_saturnide_style(self.center_text(question_data["special_message"]), delay=0.02)
                
                time.sleep(1.5)
                self.score += 1
                return True, None
        else:
            # Check if all answers are considered correct
            if "all_correct" in question_data and question_data["all_correct"]:
                self.score += 1
                
                # Show special correct message if it exists
                if "special_message_correct" in question_data:
                    # For ALL CAPS message
                    if "all_caps" in question_data and question_data["all_caps"]:
                        message = question_data["special_message_correct"].upper()
                        self.display_all_caps_message(message, question_data)
                    else:
                        self.type_saturnide_style(self.center_text(question_data["special_message_correct"]), delay=0.02)
                else:
                    self.type_saturnide_style(self.center_text("Correct! Your mind is opening..."), delay=0.02)
                
                time.sleep(1.5)
                return True, None
            else:
                # Regular behavior for other questions
                is_correct = (choice - 1) == question_data["answer"]
                if is_correct:
                    self.score += 1
                    
                    # Show special correct message if it exists
                    if "special_message_correct" in question_data:
                        self.type_saturnide_style(self.center_text("Correct! " + question_data["special_message_correct"]), delay=0.02)
                    else:
                        self.type_saturnide_style(self.center_text("Correct! Your mind is opening..."), delay=0.02)
                else:
                    # Show special incorrect message if it exists
                    if "special_message_incorrect" in question_data:
                        self.type_saturnide_style(self.center_text(question_data["special_message_incorrect"]), delay=0.02)
                    else:
                        correct_answer = question_data["options"][question_data["answer"]]
                        self.type_saturnide_style(self.center_text(f"Incorrect. The answer was: {correct_answer}"), delay=0.02)
                
                # Show additional message if it exists (like wine message for Q2)
                if "special_message" in question_data:
                    print()
                    self.type_saturnide_style(self.center_text(question_data["special_message"]), delay=0.02)
                
                time.sleep(1.5)
                return is_correct, None
                
    def display_all_caps_message(self, message, question_data):
        """Display a message in ALL CAPS with punctuation pauses"""
        centered_message = self.center_text(message)
        sys.stdout.write(f"{SATURNIDE_GREEN}")
        
        for char in centered_message:
            sys.stdout.write(char)
            sys.stdout.flush()
            
            if "pause_at_punctuation" in question_data and question_data["pause_at_punctuation"] and char in [',', '.']:
                time.sleep(1.0)  # 1 second pause for punctuation
            else:
                time.sleep(0.02)  # Normal typing speed
                
        sys.stdout.write(f"{RESET}\n")

    def play_music(self, notes, stop_event=None):
        """Play 8-bit style music in the background with visual feedback"""
        try:
            for freq, duration in notes:
                if stop_event and stop_event.is_set():
                    break
                
                if freq > 0:  # Skip silent notes (freq=0)
                    # Visual feedback for beep (▒/█ symbols alternate with different frequencies)
                    if freq > 400:
                        visual_beat = "█"
                    else:
                        visual_beat = "▒"
                        
                    # Try to make a beep sound AND show visual feedback
                    sys.stdout.write(f"{SATURNIDE_GREEN}{visual_beat}{RESET}")
                    sys.stdout.flush()
                    
                    # Also try the beep character
                    sys.stdout.write('\a')
                    sys.stdout.flush()
                    
                time.sleep(duration)
                
                # Clear visual feedback
                if freq > 0:
                    sys.stdout.write("\b \b")  # Backspace, space, backspace to clear
                    sys.stdout.flush()
                    
        except Exception as e:
            # Print error but continue
            print(f"{SATURNIDE_GREEN}Music error: {e}{RESET}")
            pass
    
    def play_background_music(self, notes, duration=None):
        """Start background music in a separate thread"""
        if not CAN_BEEP:
            return None
            
        stop_event = threading.Event()
        
        # Define music thread function
        def music_thread():
            start_time = time.time()
            while not stop_event.is_set():
                self.play_music(notes, stop_event)
                
                # If duration is specified, stop after that time
                if duration and time.time() - start_time > duration:
                    break
        
        # Start the music in background
        thread = threading.Thread(target=music_thread)
        thread.daemon = True  # Allow program to exit even if thread is running
        thread.start()
        
        return stop_event  # Return event to stop the music later
            
    def run_quiz(self):
        """Run the full quiz"""
        self.display_intro()
        
        # Store user inputs and choices for potential use later
        user_inputs = []
        self.user_choices = []  # Track numeric choices
        all_sixes = True  # Flag to check if user entered "6" for all questions
        
        for i, question in enumerate(self.questions):
            # Display the question
            result, user_input = self.display_question(question, i+1)
            
            # Check if user entered "6" for this question
            if not hasattr(self, 'last_raw_input') or self.last_raw_input != "6":
                all_sixes = False
                
            # Store any user input
            if user_input:
                user_inputs.append(user_input)
            
            # Add slow response for questions that need it
            if "slow_response" in question and question["slow_response"]:
                time.sleep(5)  # 5 second pause after certain questions
                
            # Add hammer animation between Q5 and Q6
            if i == 4 and "show_hammer_animation" in question and question["show_hammer_animation"]:
                self.display_hammer_animation()
        
        # Special case: User entered "6" for all questions
        if all_sixes:
            self.display_happy_ending()
            return
            
        # Check if the last question has a custom ending
        if "custom_ending" in self.questions[-1] and self.questions[-1]["custom_ending"]:
            # Pass the last user input to the custom ending
            last_input = user_inputs[-1] if user_inputs else None
            
            # Start background music for the ending
            music_stop = self.play_background_music(SCARY_MUSIC)
            self.display_custom_ending(self.questions[-1], last_input)
            
            # Stop the music when ending is complete
            if music_stop:
                music_stop.set()
        else:
            self.display_results()
            
    def display_custom_ending(self, last_question: Dict, user_input=None):
        """Display a custom ending sequence"""
        self.clear_screen()
        
        # Dramatic effect - screen flicker
        self.display_flicker_effect("SYSTEM OVERLOAD", duration=3)
        
        # Display the ending message with dramatic effect
        if "ending_message" in last_question:
            # If dramatic_ending is set, make it more intense
            if "dramatic_ending" in last_question and last_question["dramatic_ending"]:
                # Display big, centered text with dramatic presentation
                ending_message = last_question["ending_message"]
                self.clear_screen()
                
                # Show message letter by letter with flicker
                for i, char in enumerate(ending_message):
                    self.clear_screen()
                    partial_message = ending_message[:i+1]
                    centered_text = self.center_text(partial_message)
                    print("\n" * 10)  # Push down for vertical centering
                    print(f"{SATURNIDE_GREEN}{centered_text}{RESET}")
                    time.sleep(0.2)
                
                # Hold the complete message
                time.sleep(1)
            else:
                self.type_saturnide_style(self.center_text(last_question["ending_message"]), delay=0.04)
            print()
        
        # Additional effects before the glitch
        self.display_spiral_animation(duration=3)
        
        # Display glitch sequence with user input or default "Saturn'd"
        glitch_text = user_input if user_input else "Saturn'd"
        self.display_glitch_fullscreen(glitch_text, duration=7)
        
        # Clear screen and show final message with punctuation pauses
        self.clear_screen()
        
        # Display the final message with pauses at periods
        if "final_message" in last_question:
            message = self.center_text(last_question["final_message"])
            sys.stdout.write(f"{SATURNIDE_GREEN}")
            for char in message:
                sys.stdout.write(char)
                sys.stdout.flush()
                if char == '.':
                    time.sleep(1.0)  # 1 second pause at periods
                else:
                    time.sleep(0.02)  # Normal typing speed
            sys.stdout.write(f"{RESET}\n")
        
        # Additional dramatic effect - heartbeat sound visualization
        self.display_heartbeat_animation(duration=5)
        
        # Dramatic death sequence
        self.display_death_sequence()
        
        time.sleep(2)
        
        # Display relationship message
        self.type_saturnide_style(self.center_text("For a healthy relationship, s6x is the key"), delay=0.04)
        time.sleep(1.5)
        
        # Ask to play again
        play_again = input(f"{SATURNIDE_GREEN}Would you like to play again? (y/n): {RESET}").lower()
        if play_again == 'y':
            self.score = 0
            self.run_quiz()
        else:
            self.clear_screen()
            self.type_saturnide_style(self.center_text("Exiting Saturnide..."), delay=0.04)
            time.sleep(1)
            self.clear_screen()
            
    def display_heartbeat_animation(self, duration=5):
        """Display a heartbeat animation"""
        self.clear_screen()
        
        heartbeat_patterns = [
            "___/\\___",
            "___/\\/\\___",
            "___/\\___",
            "___/\\/\\___",
            "___/\\___",
            "___________",
            "___________",
            "___/\\___",
        ]
        
        start_time = time.time()
        i = 0
        
        try:
            while time.time() - start_time < duration:
                pattern = heartbeat_patterns[i % len(heartbeat_patterns)]
                centered = self.center_text(pattern)
                
                print(f"{SATURNIDE_GREEN}{centered}{RESET}", end="\r")
                time.sleep(0.5)
                i += 1
        except KeyboardInterrupt:
            pass
            
        self.clear_screen()
        
    def display_death_sequence(self):
        """Display a dramatic death sequence"""
        self.clear_screen()
        
        # Flatline effect
        flatline = "____________"
        self.type_saturnide_style(self.center_text("VITAL SIGNS CRITICAL"), delay=0.03)
        time.sleep(1)
        
        for _ in range(3):
            self.clear_screen()
            print("\n" * 10)
            print(f"{SATURNIDE_GREEN}{self.center_text(flatline)}{RESET}")
            time.sleep(0.5)
            
        self.clear_screen()
        self.type_saturnide_style(self.center_text("CONNECTION TERMINATED"), delay=0.05)
        time.sleep(2)
        self.clear_screen()

    def display_raining_code(self, duration=5):
        """Display Saturnide-style raining code animation"""
        self.clear_screen()
        
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,./<>?"
        columns = TERM_WIDTH
        start_time = time.time()
        
        # Create column positions and speeds
        positions = [random.randint(-10, 0) for _ in range(columns)]
        speeds = [random.uniform(0.2, 1.0) for _ in range(columns)]
        column_active = [random.random() < 0.3 for _ in range(columns)]
        
        try:
            while time.time() - start_time < duration:
                # Generate a line of Saturnide code
                line = [" " for _ in range(columns)]
                
                # Update column positions
                for i in range(columns):
                    if not column_active[i]:
                        continue
                    
                    # Move down
                    positions[i] += speeds[i]
                    
                    # If column reached bottom, reset
                    if positions[i] > 20:
                        positions[i] = random.randint(-10, 0)
                        column_active[i] = random.random() < 0.3
                    
                    # Draw character if in visible area
                    if 0 <= int(positions[i]) < 20:
                        line[i] = random.choice(chars)
                
                # Print the line
                print(f"{SATURNIDE_GREEN}{''.join(line)}{RESET}", end="\r")
                time.sleep(0.05)
                
                # Occasionally toggle column activity
                if random.random() < 0.1:
                    col = random.randint(0, columns-1)
                    column_active[col] = not column_active[col]
        except KeyboardInterrupt:
            pass
        
        self.clear_screen()

    def display_spiral_animation(self, duration=5):
        """Display a spiral animation"""
        self.clear_screen()
        
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        start_time = time.time()
        i = 0
        
        try:
            while time.time() - start_time < duration:
                animation_frame = chars[i % len(chars)]
                message = "Saturnide has you..."
                centered = self.center_text(f"{animation_frame} {message} {animation_frame}")
                
                print(f"{SATURNIDE_GREEN}{centered}{RESET}", end="\r")
                time.sleep(0.1)
                i += 1
        except KeyboardInterrupt:
            pass
        
        self.clear_screen()

    def display_loading_bar(self, duration=3):
        """Display a loading bar animation"""
        self.clear_screen()
        
        width = min(50, TERM_WIDTH - 10)
        total_frames = 100
        frame_time = duration / total_frames
        
        try:
            for i in range(total_frames + 1):
                progress = i / total_frames
                filled_width = int(width * progress)
                empty_width = width - filled_width
                
                bar = f"[{'█' * filled_width}{' ' * empty_width}] {int(progress * 100)}%"
                centered_bar = self.center_text(bar)
                
                print(f"{SATURNIDE_GREEN}{centered_bar}{RESET}", end="\r")
                time.sleep(frame_time)
        except KeyboardInterrupt:
            pass
        
        print()
        self.clear_screen()

    def display_saturn_smile_animation(self):
        """Display a Saturn smile animation"""
        self.clear_screen()
        
        frames = [
            """
        _____       
      /       \\     
    (  o     o  )    
      \\   ∼   /     
       \\_____/      
      ~ Saturn ~     
            """,

            """
       \\_____\\     
      /       \\     
    (  ^     ^  )    
      \\  ___ /     
       \\_____/      
    Saturn is smiling
            """
        ]
        
        for _ in range(2):  # Show animation twice
            for frame in frames:
                self.clear_screen()
                for line in frame.split('\n'):
                    print(f"{SATURNIDE_GREEN}{self.center_text(line)}{RESET}")
                time.sleep(1)
    
    def display_skull_eats_saturn_animation(self):
        """Display a skull eating Saturn animation"""
        self.clear_screen()
        
        frames = [
            """
     .-''''-.       
    /        \\     
   |  0    0  |     
   |    ∆     |     
    \\  ----  /     
     `'----'`       
      SKULL         
            """,

            """
     .-''''-.       
    /        \\     
   |  0    0  |     
   |   (°°)   |     
    \\__██__/      
    Saturn GONE    
            """
        ]
        
        for _ in range(2):  # Show animation twice
            for frame in frames:
                self.clear_screen()
                for line in frame.split('\n'):
                    print(f"{SATURNIDE_GREEN}{self.center_text(line)}{RESET}")
                time.sleep(1)

    def display_flicker_effect(self, text, duration=3):
        """Display a flickering text effect, simulating a glitch"""
        self.clear_screen()
        
        start_time = time.time()
        visible = True
        
        centered_text = self.center_text(text)
        
        try:
            while time.time() - start_time < duration:
                if visible:
                    print(f"{SATURNIDE_GREEN}{centered_text}{RESET}", end="\r")
                else:
                    # Print empty spaces to hide the text
                    print(" " * len(centered_text), end="\r")
                
                # Random flickering duration
                flicker_time = random.uniform(0.05, 0.2)
                time.sleep(flicker_time)
                visible = not visible
        except KeyboardInterrupt:
            pass
        
        self.clear_screen()
        
    def display_wake_up_message(self):
        """Display the final 'Wake up Neegan' message"""
        self.clear_screen()
        
        # Wait in darkness for 5 seconds
        time.sleep(5)
        
        # Display the message
        self.type_saturnide_style(self.center_text("Wake up Neegan."), delay=0.1)
        time.sleep(2)
    
    def display_happy_ending(self):
        """Display a happy ending when user tries to select option 6"""
        self.clear_screen()
        
        # Display a festive message
        self.type_saturnide_style(self.center_text("🎉 CONGRATULATIONS! 🎉"), delay=0.05)
        time.sleep(1)
        
        # Show a happy animation
        happy_frames = [
            """
      \\o/
       |
      / \\
            """,
            """
       o
      /|\\
      / \\
            """,
            """
      \\o/
       |
      / \\
            """,
            """
       o
      \\|/
      / \\
            """
        ]
        
        # Animate the happy person
        for _ in range(3):  # 3 cycles
            for frame in happy_frames:
                self.clear_screen()
                print(f"{SATURNIDE_GREEN}{self.center_text('🎉 YOU NOW HAVE A HEALTHY RELATIONSHIP! 🎉')}{RESET}")
                print()
                for line in frame.split('\n'):
                    print(f"{SATURNIDE_GREEN}{self.center_text(line)}{RESET}")
                time.sleep(0.3)
        
        # Display festive message
        self.clear_screen()
        time.sleep(0.1)
        self.type_saturnide_style(self.center_text("You've sacrificed Zoé!"), delay=0.05)
        time.sleep(1)
        self.type_saturnide_style(self.center_text("Saturn the God of time and rebirth is pleased with your sacrifice!"), delay=0.05)
        time.sleep(1)
        
        # Show sparkling effect
        for _ in range(20):
            sparkles = ""
            for _ in range(TERM_WIDTH):
                if random.random() < 0.1:
                    sparkles += random.choice(["✨", "🌟", "💫", "⭐", "🎉", "🎊"])
                else:
                    sparkles += " "
            print(f"{SATURNIDE_GREEN}{sparkles}{RESET}")
            time.sleep(0.1)
            
        self.clear_screen()
        
        # Final joyful message
        self.type_saturnide_style(self.center_text("You've been freed from the simulation!"), delay=0.05)
        print()
        time.sleep(1)
        self.type_saturnide_style(self.center_text("Enjoy your freedom, while it last!"), delay=0.05)
        print()
        time.sleep(2)
            
        # Display relationship message
        self.type_saturnide_style(self.center_text("For a healthy relationship, s6x is the key"), delay=0.04)
        time.sleep(1.5)
            
        # Ask to play again
        play_again = input(f"{SATURNIDE_GREEN}Would you like to play again? (y/n): {RESET}").lower()
        if play_again == 'y':
            self.score = 0
            self.run_quiz()
        else:
            self.clear_screen()
            self.type_saturnide_style(self.center_text("Exiting Saturnide..."), delay=0.04)
            time.sleep(1)
            self.clear_screen()
        
    def display_results(self):
        """Display quiz results and appropriate animation"""
        self.clear_screen()
        
        # Display score
        score_text = f"Final Score: {self.score}/{len(self.questions)}"
        print(f"{SATURNIDE_GREEN}{self.center_text(score_text)}{RESET}")
        print()
        
        # Display loading animation
        self.type_saturnide_style(self.center_text("Processing your answers..."), delay=0.04)
        self.display_loading_bar(3)
        
        self.clear_screen()
        
        # Choose animation and message based on score
        if self.score >= len(self.questions) * 0.75:  # At least 75% correct answers
            self.display_saturn_smile_animation()
            message = "Congratulation, You've managed to sleep another day. ☄️🌙"
        else:
            self.display_skull_eats_saturn_animation()
            message = "You've been Saturn'd. 💀🪐"
        
        self.type_saturnide_style(self.center_text(message), delay=0.04)
        print()
        
        # Add flickering effect
        time.sleep(2)
        self.display_flicker_effect(message, duration=3)
        
        # Display wake up message
        self.display_wake_up_message()
        
        # Display relationship message
        self.type_saturnide_style(self.center_text("For a healthy relationship, s6x is the key"), delay=0.04)
        time.sleep(1.5)
        
        # Ask to play again
        time.sleep(1)
        play_again = input(f"{SATURNIDE_GREEN}Would you like to play again? (y/n): {RESET}").lower()
        if play_again == 'y':
            self.score = 0
            self.run_quiz()
        else:
            self.clear_screen()
            self.type_saturnide_style(self.center_text("Exiting Saturnide..."), delay=0.04)
            time.sleep(1)
            self.clear_screen()


if __name__ == "__main__":
    try:
        quiz = SaturnideQuiz()
        quiz.run_quiz()
    except KeyboardInterrupt:
        print(f"\n{SATURNIDE_GREEN}Saturnide connection terminated.{RESET}")
    except Exception as e:
        print(f"\n{SATURNIDE_GREEN}Error in Saturnide: {e}{RESET}")
