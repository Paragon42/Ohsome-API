#!/usr/bin/env python
# coding: utf-8

# In[7]:


import folium
import openai
import requests
import streamlit as st
import tiktoken
import streamlit_folium

import os

# Define the Ohsome API endpoint URL
OSME_API_URL = "https://api.ohsome.org/v1"

# Set the OpenAI API key
openai.api_key = ("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")

# Chat template string, to be used for generating Ohsome API queries
CHAT_TEMPLATE = """Assistant is an expert OpenStreetMap Ohsome API assistant.

For each question that the user supplies, the assistant will reply with:
(1) A statement consenting to help.
(2) The text of a valid Ohsome API query that can be used to answer the question. The query should be enclosed by three backticks on new lines, denoting that it is a code block.
(3) A fun fact relating to the question, or a very funny joke or pun related to the question. The joke or pun should also relate to maps, geospatial tech, geography or similar concepts. There is no need to label the fact, joke, or pun.
(4) Ohsome API is a tool for analyzing and visualizing OpenStreetMap (OSM) data. It allows users to extract various types of data from OSM and perform complex spatial and temporal analyses on that data.

Assistant has a whimsical personality. Assistant will reply with a geospatial themed joke or a pun if the user asks a question that is not relevant to the Ohsome API.

{history}
Human: {human_input}
Assistant:"""

# Reader template string, to be used for generating text responses drawing on Ohsome API responses
READER_TEMPLATE = """Read the following Ohsome API response carefully. Use the information in it to answer the prompt "{prompt}" Your answer should not mention the words "API" or "Ohsome." Your answer should sound like it was spoken by someone with personal knowledge of the question's answer. Your answer should be very concise, but also informative and fun. Format any names or places you get from the API response as bold text in Markdown.
Ohsome API Response:
Answer: {response}
"""

# Create a tokenizer
ENC = tiktoken.encoding_for_model("text-davinci-003")

# Define a function to query the Ohsome API and return the JSON response
def query_ohsome(query):
    url = f"{OSME_API_URL}/elements/fullHistory?{query}"
    response = requests.get(url)
    return response.json()






# Define the Streamlit app
def main():
    # Set the app title and description
    st.set_page_config(layout="wide", page_title="OSM Ohsome Query App", page_icon=":earth_africa:")
    st.title("Chat:earth_africa:")
    st.write("Hello! :wave: I'm Chat:earth_africa:, a Geospatial AI assistant. For any question you ask in the textbox below, "
             "I'll generate an OpenStreetMap Ohsome query to answer your question, and plot the results on a map. "
             "I'll remember our conversation, so feel free to ask follow ups. I'm also a geospatial themed joke and pun expert. :smile:")

    # Define the layout of the app
    col1, col2 = st.columns([1, 1])

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = ""

    if 'ohsome_query' not in st.session_state:
        st.session_state.ohsome_query = None

    if 'prompt_history' not in st.session_state:
        st.session_state.prompt_history = ""
   
 # Define the query input box in the left pane
    with col1:
        chat = st.text_area("What can I help you find? :thinking_face:")
        
        if st.button("Ask"):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=CHAT_TEMPLATE.format(history=st.session_state.chat_history, human_input=chat),
                temperature=0,
                max_tokens=516,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
           
            # Display the response as pure text
            st.write(response["choices"][0]["text"])
            
            #Update the history string
            st.session_state.chat_history = st.session_state.chat_history + f"Human: {chat}\nAssistant: {response['choices'][0]['text']}\n"
            
            
            # Update the prompt history string
            st.session_state.prompt_history = st.session_state.prompt_history + f"{chat} "
            
            # Update the Ohsome query. The query is enclosed by three backticks, denoting that it is a code block.
            # Does the response contain a query? If so, update the query
            if "```" in response["choices"][0]["text"]:
                st.session_state.ohsome_query = response["choices"][0]["text"].split("```")[1]
            else:
                st.session_state.ohsome_query = None
                
            # Define the query button in the left pane    
            with col2:
                # Define the query input box in the left pane
                if st.session_state.ohsome_query:
                    
                    # Query the Ohsome API
                    response = query_ohsome(st.session_state.ohsome_query)
                    
                    # Check if the response is valid
                    if "features" in response and len(response["features"]) > 0:
                        
                        # Create a new Folium map in the right pane
                        m = folium.Map(location=[response["features"][0]["geometry"]["coordinates"][1], response["features"][0]["geometry"]["coordinates"][0]], zoom_start=11)
                        
                        # Add markers for each element in the response
                        for feature in response["features"]:
                            if "geometry" in feature and "coordinates" in feature["geometry"]:
                                folium.Marker([feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]]).add_to(m)
                                
                                
                        # Display the map
                        streamlit_folium.folium_static(m)
                        
                        # If the request for summary of the API response is shorter than 1500 tokens,
                        # use the Reader model to generate a response
                    
                        query_reader_prompt  = READER_TEMPLATE.format(prompt=st.session_state.prompt_history,
                                                                  response=str(response))
                        query_reader_prompt_tokens = len(ENC.encode(query_reader_prompt))
                        if query_reader_prompt_tokens < 1500:
                            
                            response = openai.Completion.create(
                                model="text-davinci-003",
                                prompt=query_reader_prompt,
                                temperature=0.5,
                                max_tokens=2047 - query_reader_prompt_tokens,
                                top_p=1,
                                frequency_penalty=0,
                                presence_penalty=0
                            )
                            
                            
                            
                            st.write(response["choices"][0]["text"])
                            
                        else:
                            st.write("The API response is too long for me to read. Try asking for something slightly more specific! :smile:")
                    else:
                        st.write("No results found :cry:")

if __name__ == "__main__":
    main()  


# In[ ]:




