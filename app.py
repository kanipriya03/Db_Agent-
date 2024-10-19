import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from bson.decimal128 import Decimal128
import streamlit as st
from langchain.llms import Ollama
from langchain.agents import initialize_agent, Tool
from langchain.prompts import PromptTemplate

# Replace this with your MongoDB Atlas URI
uri = "mongodb+srv://kanipriya2003:DE9vHv887zWSMHta@cluster0.1uqyl.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client['sample_airbnb']
collection = db['listingsAndReviews']

# Sample approved email IDs (for demonstration purposes)
approved_emails = ["user1@example.com", "user2@example.com"]  # Add your approved email IDs here

# Function to fetch data from MongoDB
def fetch_data():
    result = collection.find().limit(100)  # Fetching the first 100 documents
    return pd.DataFrame(list(result))

# Function to convert Decimal128 to float in DataFrame
def convert_decimal_columns(df):
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: float(x.to_decimal()) if isinstance(x, Decimal128) else x)
    return df

# Function to visualize data
def visualize_data(df, plot_type='histogram', field='price', bins=50):
    df = convert_decimal_columns(df)  # Convert Decimal128 to float
    plt.figure(figsize=(10, 6))
    
    if plot_type == 'histogram':
        df[field].hist(bins=bins)
        plt.title(f'{field.capitalize()} Distribution')
        plt.xlabel(field.capitalize())
        plt.ylabel('Frequency')
        
    elif plot_type == 'boxplot':
        df.boxplot(column=field)
        plt.title(f'{field.capitalize()} Boxplot')
        plt.ylabel(field.capitalize())
        
    st.pyplot(plt)  # Display the plot in Streamlit

# Langchain & Ollama Integration
# Initialize Ollama with the 'gemma2' model
ollama = Ollama(model="gemma2")

# Create a simple prompt template
prompt = PromptTemplate(
    input_variables=["query"],
    template="""
    You are an agent for MongoDB queries. The user asks: {query}.
    Fetch relevant data from MongoDB and return the results.
    """
)

# Example tool for querying MongoDB
def query_mongodb(query: str):
    # Here you would write logic to query MongoDB based on the user's query
    # For now, we return a mocked result
    # Example of querying MongoDB based on the user's natural language query
    results = collection.find({"address.market": {"$regex": query, "$options": "i"}}).limit(5)
    return pd.DataFrame(list(results)).to_string()

# Define the toolset
tools = [
    Tool(
        name="query_mongodb",
        func=query_mongodb,
        description="Query the MongoDB database"
    )
]

# Initialize agent
agent = initialize_agent(tools, ollama, agent_type="zero-shot-react-description", verbose=True)

# Streamlit UI components
st.title("Airbnb Data Query & Visualization System")

# Query Section
st.subheader("Natural Language Query to MongoDB")
query = st.text_input("Ask a question about the Airbnb data:")

if st.button("Submit Query"):
    if query:
        response = agent.run(query)
        st.write("Query Result:")
        st.write(response)

        # Visualization option appears *after* query is shown
        st.subheader("Data Visualization (Available for Authorized Users)")
        
        # Ask for email authentication for visualization
        email = st.text_input("Enter your email ID to access data visualization:")
        
        if email:
            is_authorized = email in approved_emails
            if is_authorized:
                st.success("You are authorized for data visualization.")
                
                # Widgets for user input for visualization
                plot_type = st.selectbox("Select Plot Type:", ['histogram', 'boxplot'])
                field = st.selectbox("Select Field to Visualize:", ['price', 'accommodates', 'bedrooms', 'bathrooms'])
                bins = st.slider("Select Number of Bins:", min_value=1, max_value=100, value=50)

                # Fetch data and visualize based on user input
                if st.button("Generate Visualization"):
                    df = fetch_data()
                    visualize_data(df, plot_type, field, bins)
            else:
                st.error("Unauthorized user. You do not have access to the data visualization feature.")
    else:
        st.warning("Please enter a query.")