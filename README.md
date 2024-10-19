# Airbnb Data Query & Visualization System

This project is a web application that allows users to query and visualize data from the **Airbnb dataset** stored in **MongoDB Atlas**. The application uses the **LangChain** library along with the **Ollama** model `gemma2` to process natural language queries and return relevant information from the database.

## Features

- **Natural Language Querying**: Users can ask questions about the Airbnb data in natural language.
- **Data Visualization**: Authorized users can generate visualizations for selected fields, such as price distribution.
- **Email Authentication**: Access to visualization features is restricted to approved email IDs.

## Technologies Used

- **Python**: The main programming language for the application.
- **Streamlit**: A framework for building web applications quickly.
- **MongoDB**: NoSQL database used to store and query the Airbnb dataset.
- **LangChain**: Library for integrating language models with various tools and APIs.
- **Ollama**: Language model serving, specifically using the `gemma2` model for processing queries.

## Dataset

This application uses the **Airbnb listings and reviews** dataset from MongoDB Atlas's sample dataset. The data can be queried for various attributes like price, number of guests, and room types.

