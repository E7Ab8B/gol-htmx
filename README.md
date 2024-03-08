<h1 style="text-align: center;">gol-htmx</h1>

This s a personal project which implements the Game of Life. This implementation serves as a playground to explore and learn about integrating htmx and SSE (Server-Sent Events) into Django applications.

## Game of Life

Game of Life, a cellular automaton devised by the British mathematician John Horton Conway in 1970. The game is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input.

## Project Structure

The project follows a Django application structure. The main application is located in [src/apps/gol](/src/apps/gol). Within this directory:

- The game logic resides in [src/apps/gol/game](/src/apps/gol/game)
- Tests are available in [src/apps/gol/tests](/src/apps/gol/tests)

## Why htmx and SSE?

For dynamic and real-time updates of the grid for each generation, this project utilizes htmx along with Server-Sent Events (SSE).

- **htmx**: Facilitates seamless and dynamic updates to the user interface for each generation of the Game of Life. It eliminates the need for full page reloads and extensive JavaScript code, making UI updates smooth and efficient.
- **Server-Sent Events (SSE)**: Enables real-time updates from the server to the client, ensuring that the grid is updated instantly as new generations are computed. This ensures a responsive and interactive user experience.

## Getting Started

To get started with this project, ensure Python and Docker are installed on your machine.

1. Clone the repository
2. Navigate to the project directory
3. Build the Docker image using the provided Dockerfile and docker-compose.yaml files:

```sh
docker compose build
```

4. Run the Docker container:

```sh
docker compose up
```

## Running Tests

Tests are written using pytest. To run the tests, use the following command:

```sh
docker compose run django pytest
```

## Settings

The Django settings are organized in the [settings](/src/gol_htmx/settings) directory.

- [base.py](/src/gol_htmx/settings/base.py) contains the base settings.
- Environment-specific settings are stored in:
  - [local.py](/src/gol_htmx/settings/local.py)
  - [test.py](/src/gol_htmx/settings/test.py)
