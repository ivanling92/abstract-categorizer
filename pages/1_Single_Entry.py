import streamlit as st
from groq import Groq




#Set up
client = Groq(api_key = st.secrets["GROQ"])


sysPrompt_string = """
Given the following tracks: Micro-nanofabrication and Characterization, Nanodevices, Systems and Applications, Sustainable Technology. I want you to read the abstracts that I will be sending to you, and reply with only the closest matching track name. Say "OK" if you understand what needs to be done.
Each of the tracks will be classified as follow:

Micro-nanofabrication and Characterization = {Processes, Design, Characterisation}
Nanodevices={Electronics, Photonics and Phononics, Biodevices, Micro-Nano Systems, Flexible Devices}
Systems and Applications = {Sensors, Heterogeneous Integration, Information and Communication Technologies, Machine Learning}
Sustainable Technology = {Alternative Fabrication Processes, Circular Processes, Energy, Environmental Monitoring}

I need you to return in the following format: {Track, Sub-Track}. E.g. {Micro-nanofabrication and Characterization, Design}
"""

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
        "content": "Title: "+paper_title+"  Abstract: " + abstract,
    }

    messageLog.append(userPrompt)

    chat_completion = client.chat.completions.create(
            messages=messageLog,
            model="llama3-70b-8192", temperature = 0.1
        )
    return chat_completion.choices[0].message.content

# Display the track when "Submit" is clicked
if st.button("Submit"):
    selected_track = determine_track(abstract)
    st.subheader("Submission Summary")
    st.write("**Title:**", paper_title)
    st.write("**Abstract:**", abstract)
    st.write("### Assigned Track:")
    st.markdown(f"<h1 style='color:blue;'>{selected_track}</h1>", unsafe_allow_html=True)
