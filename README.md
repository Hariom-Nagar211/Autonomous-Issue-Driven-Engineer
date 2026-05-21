## 🚀 Autonomous Issue Driven Engineer

AI agent that automatically fixes GitHub issues and opens pull requests.

## 🧠 Tech Stack
FastAPI • LangChain • RAG • LLM Agents • Docker • GitHub API

## 🔥 Demo
- Input: GitHub Issue
- Output: Auto-generated fix + Draft PR

## 📸 Demo Walkthrough

### 1. Github File Error(Syntax erro in line 5, 10 and 13)
![Error File](assets/Image1.png)

### 2. Issue Input
![Issue](assets/Image2.png)

### 3. Agent Planning
![Plan](assets/Image3.png)

### 4. Code Fix
![Fixing](assets/Image4.png)

### 5. PR Creation
![PR](assets/Image5.png)

### 6. Fixed Code Review
![Code Review](assets/Image6.png)

### 7. Merged PR and Issue Closed
![Merged PR](assets/Image7.png)

### 8. Fixed Code Task Complete
![Fixed Code](assets/Image8.png)


## ✨ Key Features

- 🔍 Intelligent code retrieval using RAG
- 🤖 Autonomous agent loop (plan → edit → validate-> self healing)
- 🔧 Automatic bug fixing from GitHub issues
- 🔁 Draft PR generation with commits
- ⚡ Supports multiple LLM providers

## 💡 Why This Project?

Modern software development is moving towards AI-assisted workflows.
This project demonstrates how LLM agents can:
- Understand large codebases
- Fix real-world issues
- Integrate with developer tools like GitHub

## What It Does

The live GitHub flow looks like this:

1. A developer opens a GitHub issue.
2. GitHub sends an `issues` webhook to AIDE.
3. Clones the repository locally.
4. Parses the repository and builds a retrieval index.
5. Finds relevant files and creates a repair plan.
6. Edits the likely file(s), validates syntax, and runs tests when present.
7. Creates a branch, pushes the fix, and opens a draft PR.
8. Comments back on the issue with the result.

## Project Structure

```text
api/                    FastAPI app and GitHub webhook entrypoint
backend/agents/         retriever, Planner, coder, fixer, critic, self healer, orchestration
backend/rag/            Parser, retriever, vector store
backend/services/       execution helpers, llm service, github service
scripts/                Manual test and exploration scripts
tests/                  Automated tests for the live autonomous flow
repos/                  Cloned target repositories and job workspaces
```

## Supported LLM providers

The project supports 4 LLM providers (in priority order):

- `openai` - OpenAI GPT models
- `anthropic` - Anthropic Claude models
- `gemini` - Google Gemini models
- `ollama` - Local Ollama (default)

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Autonomous-Issue-Driven-Engineer
```

### 2. Create a .env file

Example : 

```env
GITHUB_TOKEN=your_github_token
GITHUB_WEBHOOK_SECRET=your_random_webhook_secret

LLM_PROVIDER=Your chosen provider - openai, anthropic, gemini or ollama.
LLM_MODEL=Your chosen model name for that provider, e.g. qwen2.5-coder:7b
OPENAI_API_KEY=your_key  // If using OpenAI
ANTHROPIC_API_KEY=your_key  // If using Anthropic
GOOGLE_API_KEY=your_key // If using Google Gemini
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

#### How to get github token
1. Go to GitHub -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens -> Generate new token
2. Set permissions: Repository permissions -> Contents, Issues, Pull requests (Read and write)
3. Copy the generated token and paste it into `.env` as `GITHUB_TOKEN`

#### How to get github webhook secret
Generate a strong random string (e.g. with Python `import secrets; print(secrets.token_hex(32))`) and paste it into `.env` as `GITHUB_WEBHOOK_SECRET`. Use the same value when configuring the GitHub webhook.

#### If using OpenAI, Anthropic, or Google Gemini, create API keys on their respective platforms and add them to `.env` as `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GOOGLE_API_KEY`.

#### If using Ollama :  
1. make sure to set `LLM_PROVIDER=ollama` and `OLLAMA_BASE_URL=http://host.docker.internal:11434` in `.env`. 
2. Install Ollama on your host machine from https://ollama.com/.
3. Pull the model you want to use, for example:

```bash
ollama pull qwen2.5-coder:7b
```

#### Also as we are going to use Docker :
1. Install Docker desktop from https://www.docker.com/products/docker-desktop and 
2. Run Docker desktop so that you can use Docker commands and Docker Compose to run the project.

### 3. Exposing the API with a tunnel and GitHub Webhook Setup
To allow GitHub to send webhooks to your local development server, you need to expose it to the internet using a tunnel. Cloudflare Tunnel is a great option for this.

1. Install Cloudflare Tunnel (cloudflared) from https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/downloads/
2. Run the tunnel to expose your local API:

```bash 
cloudflared tunnel --url http://localhost:8000
```
3. Cloudflare will provide you with a public URL like `https://your-random-name.trycloudflare.com`. This is the URL GitHub will use to send webhooks.
4. In your GitHub repository, go to `Settings -> Webhooks -> Add webhook` and configure it with:
- Payload URL: `https://your-random-name.trycloudflare.com/api/webhook/github`
- Content type: `application/json`
- Secret: same value as `GITHUB_WEBHOOK_SECRET` in `.env`
- Events: select `Issues`       
- Active: enabled

Note : Keep the tunnel running in a seprate terminal while you are developing and testing, so GitHub can reach your local API.

### 5. Running the project

1. Start the Ollama server ina separate terminal (if using Ollama):

```bash
ollama serve
```

2. Now build docker image and run the project with Docker Compose in seprate terminal:

```bash 
docker compose build
docker compose up
```

Now you can open a new GitHub issue to trigger the flow. Keep an eye on the terminal running Docker Compose to see the logs and results.


## Future Improvements

1. **Intelligent Testing Pipeline**
- Automatically generate and run tests to validate fixes before PR creation.
2. **CI/CD and DevOps Automation** 
- Automated Docker optimization and Kubernetes deployment generation.
- Integrate GitHub Actions pipelines for continuous integration. 
3. **Memory and Learning System**
- Implement a long-term memory system for the agent to learn from past issues and fixes.
- Use vector databases to store and retrieve past issue contexts and solutions.
- Store reusable engineering patterns and architectural decisions.
4. **Human-in-the-Loop Collaboration**
- Allow developers to approve, reject, or modify agent-generated plans.
5. **Multi-Modal Engineering Support**
- Support for diagram understanding, UI screenshots, and architecture images.
- Enable code generation directly from whiteboard designs or flowcharts.


## License

This project is licensed under the MIT License.
