# AI-Powered Document Management System

## Overview

This project is an AI-powered document management system built with React. It features a dashboard, dataset manager, and an AI chatbot for interacting with your documents. The application uses a modern, responsive design with Chakra UI and supports both light and dark modes.

## Features

- User authentication
- Dashboard with activity overview
- Dataset manager for uploading and managing documents
- AI chatbot for document interaction
- Responsive design with light and dark mode support

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Node.js (v14.0.0 or later)
- npm (v6.0.0 or later)

## Installation

To install the application, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-document-management.git
   ```

2. Navigate to the project directory:
   ```
   cd ai-document-management
   ```

3. Install the dependencies:
   ```
   npm install
   ```

4. Create a `.env` file in the root directory and add the following environment variables:
   ```
   REACT_APP_API_URL=http://your-api-url.com
   ```

## Running the Application

To run the application in development mode, use the following command:

```
npm start
```

The application will be available at `http://localhost:3000`.

## Building for Production

To create a production build, run:

```
npm run build
```

This will create a `build` directory with the production-ready files.

## Docker Support

This project includes Docker support for easy deployment. To build and run the Docker container:

1. Build the Docker image:
   ```
   docker build -t ai-document-management .
   ```

2. Run the Docker container:
   ```
   docker run -p 8080:80 ai-document-management
   ```

The application will be available at `http://localhost:8080`.

## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

If you have any questions or feedback, please contact [Your Name] at [your.email@example.com].