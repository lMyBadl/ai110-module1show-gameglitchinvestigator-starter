# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  The hints were backwards and the score in the debug panel was negative after a few bad guesses. I was able to enter guesses that were outside of the allowed range, and I could also enter decimals and get the answer correct. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Enter key for inputting guesses| submit guess | nothing | no console output|
| entered 60 | Go HIGHER | Go LOWER | None |
| new game | restart guessing game | nothing | no console output |
| 100000000000 | prompt to enter a guess in the range | Go HIGHER | nothing |
| 98.3342423 | enter an integer | Correct! | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude Code to help write code and debug the project.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
It suggested that on every even attempt, we do a string comparison instead of a numeric one which is correct, which would lead to incorrect hints as instead of going integer type comparisons, the app was instead doing string comparisons. I verified this by typing in the same number that is less than than the answer but more than the most significant digit, and saw that the hint was changing. 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I said that the website that when the hint would suggest going in the opposite direction, claude fixed the first part. However, it did not address the typeerror part, meaning that there were still incorrect hints. I verified this by entering numbers that I knew would be less than the guess both integer and string comparison wise, and I got a go lower hint from the website.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I ran tests through pytest to make sure that the fixes worked. I also manually checked with some of my own tests on the website to confirm that I'm getting expected results.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
One test I ran was for the hints about if the hints were correct through pytest. It confirmed that my hints were incorrect, and should instead be the opposite. 
- Did AI help you design or understand any tests? How?
Claude helped me write all the tests, and then I looked through them and confirmed that they were testing the right functionality. I also prompted Claude to add more test cases as I felt they had missed some. 
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every time the website changes from the user, streamlit reruns the entire python script. This means that all the variables are forgotten. However, streamlit has its own dictionary to store those values, which allows you to get previous session variable values. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
One habit I would like to reuse is  continuing to use AI to help debug code and write tests to ensure that the code is working properly. 
- What is one thing you would do differently next time you work with AI on a coding task?

- In one or two sentences, describe how this project changed the way you think about AI generated code.
