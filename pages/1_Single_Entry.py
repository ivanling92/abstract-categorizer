import streamlit as st
from groq import Groq




#Set up
client = Groq(api_key = st.secrets["GROQ"])

tracks_keywords = {
    "Micro-nanofabrication and Characterization": ["fabrication", "processes", "design", "characterisation"],
    "Nanodevices": ["electronics", "photonics", "phononics", "biodevices", "micro-nano systems", "flexible devices"],
    "Systems and Applications": ["sensors", "integration", "information", "communication", "machine learning"],
    "Sustainable Technology": ["alternative fabrication", "circular processes", "energy", "environmental monitoring"],
    "Error":["Irrelevant", "Unknown Format", "Wrong Language"]
}



sysPrompt_string = """
You are a virtual editor for the Micro-Nano Engineering Conference, and you need to classify papers into tracks. All the papers here are already related in micro-nano engineering, but with specific specialization. Take note of that when classifying.

Match papers to the closest related field rather than putting everything into nanodevices, as they are all related to micro-nano technologies somehow.

Given the following tracks: Micro-nanofabrication and Characterization, Nanodevices, Systems and Applications, Sustainable Technology. I want you to read the abstracts that I will be sending to you, and reply with only the closest matching track name.
Each of the tracks and sub-tracks will be classified as follow:

{}

I need you to return in the following format: Track, Sub-Track. E.g. Micro-nanofabrication and Characterization, Design
""".format(str(tracks_keywords))


sysPrompt = {
        "role": "system",
        "content": sysPrompt_string,
    }

messageLog = [sysPrompt]


# Title of the app
st.title("Conference Paper Submission")


# Input for the title of the paper
paper_title = st.text_input("Title of the Paper")

# Text area for the abstract
abstract = st.text_area("Abstract", height=200)

# Logic to determine the track (can be customized as needed)
# For demonstration, this assigns tracks based on keywords in the abstract
def determine_track(abstract_text):

    userPrompt = {
        "role": "user",
        "content": "Here's the paper to be categorized: Title: "+paper_title+"  Abstract: " + abstract + " Return based on my specified format, with no explanations.",
    }

    messageLog.append(userPrompt)

    chat_completion = client.chat.completions.create(
            messages=messageLog,
            model="llama3-70b-8192", temperature = 0.3
        )
    return chat_completion.choices[0].message.content

def parse_loose_response(response):
    response_lower = response.lower()  # Normalize to lowercase for case-insensitive matching
    best_match = None
    best_score = 0

    # Check each track and its associated keywords
    for track, keywords in tracks_keywords.items():
        for keyword in keywords:
            if keyword in response_lower:  # Loose match based on keywords
                match_score = response_lower.count(keyword)  # Score by keyword frequency
                if match_score > best_score:
                    best_match = (track, keyword.capitalize())  # Capitalize the sub-track for uniformity
                    best_score = match_score

    return best_match if best_match else ("No match", "No match")



# Display the track when "Submit" is clicked
if st.button("Submit"):
    aiOuput = determine_track(abstract)
    track, subtrack = parse_loose_response(aiOuput)
    st.subheader("Submission Summary")
    st.write("**Title:**", paper_title)
    st.write("**Abstract:**", abstract)
    st.write("### Assigned Track:")
    st.markdown(f"<h1 style='color:blue;'>{track}</h1>", unsafe_allow_html=True)
    st.write("### Sub Track:")
    st.markdown(f"<h1 style='color:blue;'>{subtrack}</h1>", unsafe_allow_html=True)
