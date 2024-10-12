import streamlit as st
import os
import google.generativeai as genai
import random

st.set_page_config("Gen-Z-ify", "🕹️")
st.header("Can you Gen-Z it? 🕹️")
st.markdown("#### :blue[Try your hand at changing a regular sentence into a \"Gen Z\" one!]")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def process(sentence, user_sentence):

  # Create the model
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
  )

  try:
    response = model.generate_content([
      "There are two sentences - a normal sentence and one that the user writes trying to recreate the same sentence but using GenZ lingo. You are an assistant that evaluates a sentence on two parameter: \n1. Its GenZ content \n2. Match to the original sentence's sentiment. \n\nProvide a percentage score for the user sentence. Here are a few examples:",
      "sentence: I had a lot of fun at the party last night.",
      "translation: Last night’s party was lit!",
      "score: Score: 100% (Perfect use of “lit” and casual phrasing.)",
      "sentence: I had a lot of fun at the party last night.",
      "translation: That party was fun",
      "score: Score: 50% (Gets the point across, but lacks slang or personality.)",
      "sentence: I don’t understand why he’s so angry with me.",
      "translation: I have no idea why he’s furious with me.",
      "score: Score: 20% (Too formal, words like \"furious\" aren’t typically used in casual GenZ conversations.)",
      "sentence: I don’t understand why he’s so angry with me.",
      "translation: I don’t get why he’s so salty at me.",
      "score: Score: 100% (Uses \"salty,\" which is a popular GenZ term for being upset.)",
      "sentence: That’s an excellent idea, let’s do it",
      "translation: Big bet, let’s run it!",
      "score: Score: 100% (Uses \"big bet\" and \"run it,\" both common phrases among GenZ.)",
      "sentence: That’s an excellent idea, let’s do it.",
      "translation: That’s a superb idea, let’s proceed.",
      "score: Score: 5% (Overly formal, no GenZ slang used.)",
      "sentence: That’s an excellent idea, let’s do it.",
      "translation: That’s a great idea, let’s go for it.",
      "score: Score: 55% (Somewhat casual, but missing key slang.)",
      "sentence: I’ve been really tired after all the work I did yesterday.",
      "translation: I am very exhausted from the tasks I completed yesterday.",
      "score: Score: 10% (Overly formal, no GenZ slang used.)",
      "sentence: I’ve been really tired after all the work I did yesterday.",
      "translation: I’m super tired from yesterday’s work.",
      "score: Score: 80% (Uses \"super\" which is common in GenZ, but could be more slangy.)",
      "sentence: I’ve been really tired after all the work I did yesterday.",
      "translation: I’m dead, yesterday was a grind.",
      "score: Score: 100% (Perfect use of \"dead\" and \"grind,\" both GenZ terms for being exhausted and a lot of work.)",
      f"sentence: {sentence}",
      f"translation: {user_sentence}",
      "score: ",
    ])
    return response.text
  except Exception as e:
    st.error(e)

original_sentences = [
    "I had a lot of fun at the party last night.",
    "I'm really looking forward to our meeting tomorrow.",
    "That restaurant served the best food I've ever had.",
    "I can't believe how tired I am after work.",
    "This is an excellent idea, let’s move forward with it.",
    "He’s lying to impress others.",
    "I don’t understand why he’s so angry with me.",
    "I’m really enjoying this vacation, it’s so relaxing.",
    "I don’t want to talk to you right now.",
    "I think we should take things slow in this relationship.",
]

original_sentence_style = "\"font-size:20px; font-weight:600; text-align:left; font-family:times; font-style:italic; background-color:#1B3B6E; padding:15px; border-radius:10px\""

# User input fields
if "sentence" not in st.session_state:
    st.session_state["sentence"]=random.choice(original_sentences)
st.write(f'<p style={original_sentence_style}>{st.session_state["sentence"]}</p>', unsafe_allow_html=True)
genz_translation = st.text_input("Enter your GenZ translation", value="")

# Button to submit for scoring
if st.button("Get Score"):
    if genz_translation:
        # API call to the model
        print(st.session_state["sentence"])
        result = process(st.session_state["sentence"], genz_translation)
        st.success(f'### {result}')
        st.session_state["sentence"]=random.choice(original_sentences)
    else:
        st.warning("Please provide your GenZ translation.")