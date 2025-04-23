import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib 
import streamlit.components.v1 as components


model = joblib.load('cognitive_model.pkl')  
df = pd.read_csv('Cleaned_Cognitive.csv')  

st.header("🧠 Cognitive Performance Analysis")
st.write("""
    Cognitive performance refers to the efficiency and effectiveness of mental processes such as:

- Memory (recalling information)
- Attention (focusing on tasks)
- Reasoning (logical thinking)
- Problem-solving (finding solutions)
- Decision-making (choosing the best option)
- Processing speed (how quickly the brain understands information)\n
It measures how well the brain performs tasks that require thinking, learning, and understanding.
""")

dataset = st.toggle("Dataset")
if dataset:
    st.dataframe(df)
    fig, ax = plt.subplots()
    sns.boxplot(data=df, y='Cognitive Score (out of 100)', ax=ax)
    ax.set_title('Cognitive Score Distribution')
    ax.set_ylabel('Cognitive Score')
    st.pyplot(fig)

st.subheader("Select Graph for Analysis📈")
x_axis = st.selectbox("Choose feature for X-axis", ["Sleep Hours", "Stress Level", "Daily Screen Time(hrs)", "Memory Test Score (out of 100)",])
y_axis = "Cognitive Score (out of 100)"  

if x_axis in df.columns and y_axis in df.columns:
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=df, x=x_axis, y=y_axis)
    ax2.set_title(f'{x_axis} vs {y_axis}')
    st.pyplot(fig2)

st.subheader("Memory Recall Test📕")

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Memory Recall Game</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      text-align: center;
      padding: 2rem;
      background-color: #f4f4f9;
      color: #333;
    }
    h1 {
      color: #4CAF50;
    }
    #instructions, #words, #result, #inputSection {
      margin-top: 20px;
    }
    textarea {
      width: 60%;
      height: 100px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      background-color: #fff;
      font-size: 16px;
    }
    button {
      background-color: #4CAF50;
      color: black;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    button:hover {
      background-color: #45a049;
    }
  </style>
</head>
<body>

  <h1>🧠 Memory Recall Game</h1>

  <div id="instructions">
    <p>📝 <strong>Instructions:</strong></p>
    <p>Click the button below to start the test. You'll see 10 random words appear on the screen for <strong>7 seconds</strong>.</p>
    <p>Try to remember as many words as possible! After the time is up, enter the words you recall.</p>
  </div>

  <button onclick="startGame()">Start Memory Test</button>

  <div id="words"></div>

  <div id="inputSection" style="display: none;">
    <h3>Enter the words you remember:</h3>
    <textarea id="userInput" placeholder="Type words separated by space or comma"></textarea><br />
    <button onclick="checkAnswers()">Submit</button>
  </div>

  <div id="result"></div>

  <script>
    const wordBank = [
      "apple", "banana", "car", "dog", "elephant", "flower", "grape", "hat",
      "ice", "jungle", "kite", "lion", "moon", "notebook", "orange"
    ];
    let selectedWords = [];

    function startGame() {
      selectedWords = [];
      document.getElementById("result").innerText = "";
      document.getElementById("userInput").value = "";
      document.getElementById("inputSection").style.display = "none";
      document.getElementById("words").innerText = "";

      while (selectedWords.length < 10) {
        const word = wordBank[Math.floor(Math.random() * wordBank.length)];
        if (!selectedWords.includes(word)) {
          selectedWords.push(word);
        }
      }

      document.getElementById("words").innerText = selectedWords.join(", ");

      setTimeout(() => {
        document.getElementById("words").innerText = "⏱ Time's up! Now enter the words you remember.";
        document.getElementById("inputSection").style.display = "block";
      }, 7000);  // 7 seconds = 7000 milliseconds
    }

    function checkAnswers() {
      const userText = document.getElementById("userInput").value.toLowerCase();
      const userWords = userText.split(/[\s,]+/).filter(word => word);
      const correctSet = new Set(selectedWords);
      const remembered = userWords.filter(word => correctSet.has(word));
      const score = Math.round((remembered.length / selectedWords.length) * 100);

      document.getElementById("result").innerText = 
        `✅ You remembered ${remembered.length} out of ${selectedWords.length} words.\\n🧠 Your score: ${score} / 100`;
    }
  </script>

</body>
</html>
"""

components.html(html_code, height=650)

st.subheader("Calculate Your Cognitive Score")

sleep = st.slider("Sleep Time (hours)", 0, 12, 6)
stress = st.slider("Stress Level (1 = Low, 5 = Moderate ,10 = High)", 1, 10, 7)
screen_time = st.slider("Screen Time (hours)", 0, 12, 5)

memory_score = st.number_input("Memory Test Score (0-100)", min_value=0, max_value=100, value=70)

exercise_input = st.radio(
  'How Often do you Workout?',
  options=[
    'Low : Never / Once a Week.',
    'Medium : 2 to 4 Days a Week.',
    'High : 5 times a Week or Daily.'
  ]
)
exercise_map = {
    'Low : Never / Once a Week.' : 0,
    'Medium : 2 to 4 Days a Week.': 1,
    'High : 5 times a Week or Daily.':2
}
exercise = exercise_map[exercise_input]

diet_input = st.radio(
  "How's your Diet Quality based on how often you eat Junk Food ?",
  options=[
    'Poor : I eat Junk Food everyday/Atleast 5 days a Week',
    'Fair : I eat Junk Food 2-4 days a Week',
    'Great : I eat Junk Food just once a Week or Never' 
  ]
)
diet_map = {
  'Poor : I eat Junk Food everyday/Atleast 5 days a Week' : 0,
  'Fair : I eat Junk Food 2-4 days a Week' : 1,
  'Great : I eat Junk Food just once a Week or Never' : 2
}
diet = diet_map[diet_input]

user_input = np.array([[sleep, stress, screen_time, memory_score, exercise, diet]])

if st.button("Calculate Cognitive Score"):
    cognitive_score = model.predict(user_input)[0]  
    cognitive_score = round(cognitive_score, 2)
    st.success(f"Your estimated Cognitive Score is: {cognitive_score}")
    if 0 <= cognitive_score < 20:
        st.error("Your Cognitive Performance is Very Poor 😩")
        st.progress(cognitive_score/100)
    elif 20 <= cognitive_score < 40:
        st.warning("Your Cognitive Performance is Quite Low 😞")
        st.progress(cognitive_score/100)
    elif 40 <= cognitive_score < 60:
        st.info("Your Cognitive Performance is Moderate 😐")
        st.progress(cognitive_score/100)
    elif 60 <= cognitive_score < 80:
        st.success("Your Cognitive Performance is Good 😀")
        st.progress(cognitive_score/100)
    elif 80 <= cognitive_score <= 100:
        st.success("GREAT! Your Cognitive Performance is Extremely Good 🥳", icon="🎯")
        st.progress(cognitive_score/100)
    else:
        st.error("Invalid score range")
        
    recommendations = []       
    if sleep <= 6:
      recommendations.append('Try getting atleast 7-8 hours of sleep.')
    if stress > 6:
      recommendations.append("High stress affects cognitive performance. Consider practicing mindfulness or relaxation techniques like Meditation.")
    if screen_time > 4:
      recommendations.append("Reduce screen time to below 5 hours a day to help your brain stay sharp.")
    if memory_score < 60:
      recommendations.append('Work on improving memory through exercises like puzzles, reading, or memory games.')
    if exercise==0:
      recommendations.append('Regular exercise boosts cognitive health. Aim for at least 3 to 4 days a week.')
    if diet==0:
      recommendations.append('Improve your diet quality with more whole foods, fruits, and vegetables.')  
      
    if recommendations:
      st.subheader('Here are some tips to help improve your Cognitive Performance 🧠\n')
      for tips in recommendations:
        st.write(f'➡️ {tips}')
    else:
      st.success("You're doing great! Keep maintaining your healthy habits 😇")
