# Todo React App

This is a simple Todo application built with React and TypeScript. It allows users to manage their tasks and categorize them.

## Features

- User authentication (login/logout)
- Create, read, update, and delete tasks
- Create and read categories
- Filter tasks by category

## Getting Started

To get started with this project, follow the instructions below.

### Prerequisites

Make sure you have the following installed:

- Node.js (version 17 or higher is recommended)
- npm (comes with Node.js)
- The `todo-api` server running.

### Installation

1.  Navigate to the `todo-ui` directory:

    ```
    cd todo-ui
    ```

2.  Install the dependencies:

    ```
    npm install
    ```

### Running the Application

To start the development server, run:

```
npm start
```

This will start the application and open it in your default web browser at `http://localhost:3000`. The app will automatically reload if you make edits.

### Building for Production (NOT WORKING FOR NOW)

To create a production build of the application, run:

```
npm run build
```

This will generate a `build` folder containing the optimized application.

### Folder Structure

-   `public/`: Contains the static files, including `index.html`.
-   `src/`: Contains the source code for the application.
    -   `components/`: Contains reusable React components.
    -   `contexts/`: Contains React context providers.
    -   `hooks/`: Contains custom React hooks.
    -   `pages/`: Contains the main pages of the application (`HomePage`, `LoginPage`).
    -   `services/`: Contains services for interacting with the API.
    -   `types/`: Contains TypeScript types and interfaces.
    -   `App.tsx`: The main application component, which handles routing.
    -   `index.tsx`: The entry point for the React application.
-   `package.json`: Lists the project dependencies and scripts.
-   `tsconfig.json`: TypeScript configuration file.

### License

This project is licensed under the MIT License.
