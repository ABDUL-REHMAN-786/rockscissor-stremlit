import streamlit as st
import random
import os
import csv

# Function to generate the computer's choice
def computer_choice():
    return random.choice(["Rock", "Paper", "Scissors"])

# Function to determine the winner
def determine_winner(user_choice, comp_choice):
    if user_choice == comp_choice:
        return "It's a tie!"
    elif (user_choice == "Rock" and comp_choice == "Scissors") or \
         (user_choice == "Paper" and comp_choice == "Rock") or \
         (user_choice == "Scissors" and comp_choice == "Paper"):
        return "You win!"
    else:
        return "Computer wins!"

# Function to play sound using URLs for hosted audio files
def play_sound(sound_type):
    if sound_type == "win":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")  # Replace with actual win sound URL
    elif sound_type == "lose":
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")  # Replace with actual lose sound URL
    else:
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3")  # Replace with actual tie sound URL

# Function to load leaderboard from CSV
def load_leaderboard():
    leaderboard = []
    if os.path.exists("leaderboard.csv"):
        with open("leaderboard.csv", mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                leaderboard.append({"name": row["name"], "wins": int(row["wins"])})
    return leaderboard

# Function to save leaderboard to CSV
def save_leaderboard(leaderboard):
    with open("leaderboard.csv", mode='w', newline='') as file:
        fieldnames = ["name", "wins"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in leaderboard:
            writer.writerow(entry)

# Function to update leaderboard with new player score
def update_leaderboard(player_name, player_wins):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": player_name, "wins": player_wins})
    leaderboard = sorted(leaderboard, key=lambda x: x["wins"], reverse=True)[:5]  # Top 5 players
    save_leaderboard(leaderboard)

# Set up the Streamlit interface
def game():
    st.title("Rock, Paper, Scissors Game with Animations and Sound Effects")

    # Track score across sessions
    if 'wins' not in st.session_state:
        st.session_state.wins = 0
    if 'losses' not in st.session_state:
        st.session_state.losses = 0
    if 'ties' not in st.session_state:
        st.session_state.ties = 0

    # Display current score
    st.write(f"**Score**: Wins: {st.session_state.wins} | Losses: {st.session_state.losses} | Ties: {st.session_state.ties}")

    # Add instructions
    st.write("Choose your option and try to beat the computer!")

    # Create the buttons for user input
    user_choice = st.radio("Choose your move", ["Rock", "Paper", "Scissors"], key="user_choice")

    # Display animated GIFs for each choice
    choice_gifs = {
        "Rock": "https://media.giphy.com/media/3o6Zt7EMt0o0t1pnT6/giphy.gif",
        "Paper": "https://media.giphy.com/media/3o6gE5aYjXfrjwlXGo/giphy.gif",
        "Scissors": "https://media.giphy.com/media/3o6ZtpyGH7uB2v2dGo/giphy.gif"
    }

    if user_choice:
        st.image(choice_gifs[user_choice], caption=user_choice, width=150)

    if st.button("Play"):
        # Get the computer's choice
        comp_choice = computer_choice()

        # Display computer's choice as GIF
        st.image(choice_gifs[comp_choice], caption=comp_choice, width=150)

        # Determine the winner
        result = determine_winner(user_choice, comp_choice)
        st.write(f"Result: {result}")

        # Update the score based on the result
        if result == "You win!":
            st.session_state.wins += 1
            play_sound("win")
        elif result == "Computer wins!":
            st.session_state.losses += 1
            play_sound("lose")
        else:
            st.session_state.ties += 1
            play_sound("tie")

        # Provide feedback to the user
        give_feedback(result)

        # Ask for player name if they want to save their score
        player_name = st.text_input("Enter your name to save your score (optional):", "")

        if player_name and st.session_state.wins > 0:
            update_leaderboard(player_name, st.session_state.wins)
    
    # Display leaderboard
    leaderboard()

# Function to provide feedback
def give_feedback(result):
    if result == "You win!":
        st.write("Great job! You outsmarted the computer!")
    elif result == "Computer wins!":
        st.write("Don't worry, try again! Remember: Rock beats Scissors, Scissors beats Paper, Paper beats Rock.")
    else:
        st.write("It's a tie! Keep going!")

# Function to display leaderboard
def leaderboard():
    leaderboard_data = load_leaderboard()
    st.write("### Leaderboard (Top 5 Players)")

    # Display the top 5 players
    for idx, entry in enumerate(leaderboard_data[:5]):
        st.write(f"{idx + 1}. {entry['name']} - {entry['wins']} wins")

# Run the game
if __name__ == "__main__":
    game()
