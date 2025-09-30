# Copilot Instructions for Smart Tourism AI Project

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Smart Tourism AI project for Hong Kong with:
- **Backend**: FastAPI with LangChain and Google Gemini 2.0/2.5
- **Frontend**: React PWA with camera integration
- **Features**: RAG-based Q&A, AI itinerary planning, real-time translation

## Tech Stack
- Backend: FastAPI, LangChain, Google Gemini, ChromaDB, Pydantic
- Frontend: React, TypeScript, Tailwind CSS, PWA capabilities
- Deployment: AWS Lambda (backend), AWS Amplify (frontend)
- AI: Google Gemini 2.0/2.5 (free tier), vector embeddings for RAG

## Code Standards
- Use TypeScript for frontend
- Use type hints for Python backend
- Follow RESTful API conventions
- Implement proper error handling
- Use environment variables for API keys
- Follow PWA best practices for offline functionality

## Key Components
- RAG system for Hong Kong tourism knowledge
- Camera integration for real-time translation
- Responsive mobile-first design
- Vector database for similarity search
- AWS deployment configuration

## Specific Instructions
- When generating FastAPI code, use proper dependency injection
- For React components, use functional components with hooks
- Implement proper loading states and error boundaries
- Use Tailwind CSS utility classes for styling
- Follow AWS Lambda deployment patterns
- Use LangChain abstractions for AI model interactions
