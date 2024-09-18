import streamlit as st
import os
import google.generativeai as genai
import json
import typing_extensions as typing
import time

def process(sentence):
  genai.configure(api_key=os.environ["GEMINI_API_KEY"])

  class Sentence(typing.TypedDict):
    score: int
    explanation: str

  # Create the model
  generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    "response_schema": Sentence
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="""
    You are an assistant that scores sentences based on how \"Gen-Z\" they are - i.e. how typical the sentence is of someone who is in Generation Z. The scores are on a percentage scale of 0 to 100. The scoring is based on the following criteria:\n1. punctuation/grammar - Gen-Z sentences often do not use completely correct grammatical structure, are informal, do not start with capital letters etc.\n2. use of emoji - Gen-Z sentences often use emojis such as 😂, 🤓, 😎, 😩, 😭, 😳, 🥵, 🥶, 👺, 💀, ☠️, 👁️👄👁️, 🔥,  and 💯 throughout the sentence.\n3. use of Gen-Z slang - Gen-Z sentences make use of the following slang words: \nAf/Asf Asl Ate Aura Banger Based Basic BDE Bestie Bet Bffr Big yikes Blud Body count Boujee Brainrot Bruh Bussin' Bussy Cap Caught in 4K Cook Cooked Clapback Dab Dank Ded Delulu Drip Era Extra Fanum tax Fire Fit/Fit check Flex Gagged Girlboss Ghost Glaze Glow-up GOAT Gucci Gyat Hits different Ick IJBOL I oop iPad kid It's giving Iykyk Jit Karen Lit Looksmaxxing Main character Mew Mid Moot/Moots Netflix and chill NPC OK Boomer Oomf Oof Opp Out of pocket Owned Periodt Pick-me Pluh Pookie Queen Ratio Ratio Red flag Rizz Roman Empire Salty Secure the bag Sheesh Shook Sigma Simp Situationship Sksksk Skibidi Slaps Slay Sleep on Snatched Stan Sus Tea Touch grass Tweaking Understood the assignment UwU Valid Vibe check VSCO girl Wig Yap Yeet Zesty\n4. Cultural references - Gen-Z sentences sometimes include cultural references, such as recent events, names of celebrities etc.\n5. Tone and Conciseness - Gen-Z sentences are, at times, self-deprecating and nihilistic, though not always. They are often shorter in length, similar to texts on messaging apps and social media platforms.\n\nGiven a sentence, score the sentence based on all of the criteria listed above. Provide an explanation for the score as well.\n\n In the first set, called Examples, are some example Gen Z sentences, their scores, and the explanation for their scores. Analyse these to help guide your scoring. In the second set, called New, are new sentences. Please provide the scores and explanation for each sentence in the New set in the following JSON format. ONLY score the sentences in the New set.
    """
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
  )

  response = model.generate_content([
    "Examples:",
    "input: watched barbie last night, 😳 margot robbie really ate that role 🔥",
    "output1: 95.5",
    "output2: The sentence includes two cultural references - the 2023 movie Barbie and actress Margot Robbie. It also uses two emojis. It also uses a Gen Z slang word - \"ate\".",
    "input: had a nice and quiet day, everything was peaceful 🌸",
    "output1: 23.8",
    "output2: As the tone of this sentence is not very similar to Gen-Z sentences, the score is on the lower end. However, it does look like a messaging app-text, and uses an emoji, thus the score.",
    "input: The weather today is pleasant, and I look forward to a productive day at work.",
    "output1: 0.5",
    "output2: The sentence uses correct, formal grammatical structure. The subject of the sentence is not very reminiscent of Gen-Z and it does not use any emojis, it does not use any Gen-Z lingo, and does not include any cultural references.",
    "input: omg, just saw the cutest puppy 🐶",
    "output1: 79.2",
    "output2: The use of the emoji, and the lack of capital letters lends itself to the style of Gen-Z sentences. The use of \"omg\" also indicates a use of a slang word. The tone is also casual and informal However, it does not include too many slang terms, it does not include cultural references, there is also only a single emoji, hence a score that is not extremely high.",
    "input: omg you totally ate that look 👏, slay queen",
    "output1: 95",
    "output2: This sentence is extremely Gen-Z in nature. It makes use of three slang words - \"ate\", \"slay\", and \"queen\", uses informal language and grammar (lack of punctuation, lack of capital letters), and is similar to a message on a social media app.",
    "input: bruh, you seriously ghosted me? 😳 smh 🤦‍♂️",
    "output1: 98.5",
    "output2: The sentence uses Gen-Z slang words - \"bruh\" and \"ghosted\". It uses three emojis, and is informal in its structure, as well as its tone. It is also very similar to a message one might find on a social media app, and the subject of the sentence is very Gen-Z in nature. Hence the high score.",
    "input: the day went by without any major issues or concerns 👍",
    "output1: 10.2",
    "output2: The sentence does use an emoji. However, that is the only aspect of the sentence that is remotely Gen-Z in nature. The sentence is grammatically correct and formal in nature, and its meaning is not very representative of Gen-Z. Thus, the score is extremely low.",
    "New:",
    f"input: {sentence}",
    "output1: ",
    "output2: "
  ])

  text = response.text
  print(text)
  json_text = json.loads(text)
  return json_text

st.set_page_config(page_title="")
style = "<style>h1 {text-align: center;} h4 {text-align: center;}</style>"
st.markdown(style, unsafe_allow_html=True)
st.title("Gen Z Sentence Scorer")
st.write("### Enter a sentence! We will rate it on how Gen-Z it is:")
user_sentence = st.text_input("Your sentence:", label_visibility="collapsed")

if user_sentence:
  with st.spinner("Calculating..."):
    result = process(user_sentence)

  with st.columns(3)[1]:
    st.write(f"# :orange[{result['score']}%]")
  st.write(f"#### {result['explanation']}")
  