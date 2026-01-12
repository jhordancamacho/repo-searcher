# Repo Searcher API

This project is a backend API designed to facilitate GitHub repository searching, integrating user authentication and chat functionalities.

## Description

The system is built modularly with the following main features:
- **Auth**: User management and authentication.
- **Github Search**: Repository search and information management.
- **Chat**: Chat interface (possibly for interacting with search results or support).

## Initial Configuration

Before starting the project, you need to configure the environment variables:

1. Create a `.env` file in this directory (`back`) using the provided template:
   ```bash
   cp .template.env .env
   ```
2. Make sure to adjust the values in the `.env` file as needed for your local environment.

## Running with Docker

The project is containerized for easy execution. Use the following commands:

1. Build the containers:
   ```bash
   docker compose build
   ```

2. Start the services:
   ```bash
   docker compose up
   ```

## Documentation and Testing (Bruno)

To test the API endpoints, we recommend using the **Bruno** application.

- **Endpoints Collection**: You will find the Bruno collection ready to import in the `docs` folder (located in the project root, one level up from this folder).

### 🚀 Getting Started

To interact with most protected endpoints, **the first mandatory step is to create a user**.

1. Open the collection in Bruno.
2. Execute the **`/auth/register`** endpoint to register and obtain your credentials/token.
3. Once registered, you will be able to use the rest of the system's functionalities.
