# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
The purpose of the game is for the player to guess the random number in as few guesses as possible. 
- [x] Detail which bugs you found.
Some bugs that I found were the debug history and attempts number not updating immediately, guesses not in bounds allowed, hints being opposite, and weird logic on even guesses. The rest of the guesses are documented with the #FIX tag.
- [x] Explain what fixes you applied.
I collaborated with Claude to generate fixes to all the bugs mentioned above. I fixed the history and attempts updating incorrectly by changing the order of the python logic, and adding placeholders to keep the rendering of the webpage the same. I also used pytest to make sure that my code is running with the expected outputs and that the fixes that I implemented didn't change the expected functionality of the functions. 

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User chooses easy mode
2. Game changes guess range from 1-20 and attempts to 6
3. User enters guess of 19
4. Game outputs 📉 Go LOWER!
5. User enters guess of 1
6. Game outputs 📈 Go HIGHER!
7. Score updates correctly after each guess
8. Game outputs 🎉 Correct! after number is guessed

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
test_game_logic.py ..........................................................                                                                           [100%]

===================================================================== 58 passed in 0.59s =====================================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
