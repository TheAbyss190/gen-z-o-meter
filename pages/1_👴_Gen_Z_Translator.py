import streamlit as st
import os
import google.generativeai as genai

st.set_page_config("Gen Z Translator", "👴")
st.header("Welcome to the Gen Z Translator!")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def process(sentence):

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
        "You are working as a linguist, attempting to understand and translate \"Gen-Z\" speech (the slang used by youth, mostly on the Internet) into more regular English. Gen-Z speech and slang are governed by many criteria, of which some are listed below:\n\n1. punctuation/grammar - Gen-Z sentences often do not use completely correct grammatical structure, are informal, do not start with capital letters etc.\n2. use of emoji - Gen-Z sentences often use emojis such as 😂, 🤓, 😎, 😩, 😭, 😳, 🥵, 🥶, 👺, 💀, ☠️, 👁️👄👁️, 🔥,  and 💯 throughout the sentence.\n3. use of Gen-Z slang - Gen-Z sentences make use of various slang words, some of which are below: \nAf/Asf Asl Ate Aura Banger Based Basic BDE Bestie Bet Bffr Big yikes Blud Body count Boujee Brainrot Bruh Bussin' Bussy Cap Caught in 4K Cook Cooked Clapback Dab Dank Ded Delulu Drip Era Extra Fanum tax Fire Fit/Fit check Flex Gagged Girlboss Ghost Glaze Glow-up GOAT Gucci Gyat Hits different Ick IJBOL I oop iPad kid It's giving Iykyk Jit Karen Lit Looksmaxxing Main character Mew Mid Moot/Moots Netflix and chill NPC OK Boomer Oomf Oof Opp Out of pocket Owned Periodt Pick-me Pluh Pookie Queen Ratio Ratio Red flag Rizz Roman Empire Salty Secure the bag Sheesh Shook Sigma Simp Situationship Sksksk Skibidi Slaps Slay Sleep on Snatched Stan Sus Tea Touch grass Tweaking Understood the assignment UwU Valid Vibe check VSCO girl Wig Yap Yeet Zesty\n4. Cultural references - Gen-Z sentences sometimes include cultural references, such as recent events, names of celebrities etc.\n5. Tone and Conciseness - Gen-Z sentences are, at times, self-deprecating and nihilistic, though not always. They are often shorter in length, similar to texts on messaging apps and social media platforms.\n\nGiven a sentence written in a style reminiscent of Gen Z, translate the sentence, retaining its intended meaning, into a more standard form of English that all generations can easily understand.\n\nHere are some Gen Z sentences, and example translations:",
        "input: watched barbie last night, 😳 margot robbie really ate that role 🔥",
        "output: I watched Barbie last night. Margot Robbie was amazing in her role!",
        "input: new kicks are so fire 🔥",
        "output: Those new shoes look amazing!",
        "input: lowkey missing summer vibes",
        "output: I miss how the summer was a little bit, frankly.",
        "input: brb, grabbing coffee",
        "output: Give me a second, I'm going to go get some coffee.",
        "input: new hoodie, who dis",
        "output: I got a new hoodie. What do you guys think?",
        "input: got the squad together",
        "output: I got my friends together.",
        f"input: {sentence}",
        "output: ",
        ])

        return response.text
    except Exception as e:
        st.error(e)
        return False

input_sentence = st.text_input("Enter a Gen Z sentence:")

if input_sentence:
    response = process(input_sentence)

    if response:
        st.write(f"{response}")


