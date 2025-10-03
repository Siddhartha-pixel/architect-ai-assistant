# Archi-Synth 🤖: AI Architectural Design Assistant

Archi-Synth is a full-stack web application that serves as a creative partner for architects and designers. It transforms textual design briefs into refined visual concepts using a powerful multimodal AI pipeline, complete with a secure user authentication system and design history.

---

## Features

* **AI-Powered Design Generation**: Converts a simple text prompt into a high-quality, photorealistic architectural rendering.
* **Secure User Authentication**: Full registration and login system using JWT (JSON Web Tokens) to secure user data and designs.
* **Design Iteration History**: All generated designs are saved per user. The frontend displays a history of past creations, allowing users to review their work.
* **AI-Generated Narrative**: Alongside the image, the application generates a design narrative and a mock compliance check using a language model.
* **Fully Dockerized Backend**: The FastAPI server and PostgreSQL database are containerized with Docker, ensuring a consistent and easy-to-run development environment.
* **Modern Frontend**: A responsive user interface built with React and Vite.

---

## Tech Stack

* **Frontend**: React, Vite, Axios, Konva.js
* **Backend**: FastAPI (Python), Uvicorn
* **Database**: PostgreSQL
* **AI Services**:
    * **Google Gemini (1.5 Flash & Pro)**: For multimodal analysis and text generation (narrative/compliance).
    * **Stable Diffusion XL (via Replicate API)**: For final image generation.
* **Authentication**: JWT, Passlib (for password hashing)
* **Deployment**: Docker, Docker Compose
* **Database Migrations**: Alembic

---

## Project Journey & Progress

This project was developed as a full-stack challenge, evolving from a core concept to a feature-rich application.

The initial goal was to build the end-to-end AI pipeline. A significant part of the development involved a deep and methodical debugging process to ensure stability across different environments. This included resolving complex issues related to Docker networking, Python dependency conflicts (`bcrypt`, `google-generativeai`), database migration state corruption (Alembic), and frontend library incompatibilities (Vite and React).

After stabilizing the core application, the project was expanded to include a complete, secure user authentication system and a frontend UI for viewing design history. The final result is a robust prototype that successfully demonstrates the integration of multiple modern technologies to solve a creative-architectural problem.

---

## Local Setup and Running the Project

### Prerequisites
* Git
* Docker and Docker Compose (Docker Desktop is recommended)
* Node.js and npm

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd <your-repository-name>