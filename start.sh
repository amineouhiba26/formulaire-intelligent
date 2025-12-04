#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Nexus Connected Backend...${NC}\n"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}\n"
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${RED}⚠️  Please edit .env file with your configuration!${NC}"
        echo -e "${RED}   Especially add your GROQ_API_KEY${NC}\n"
    else
        echo -e "${RED}❌ .env.example not found!${NC}"
        exit 1
    fi
fi

# Install/update dependencies
echo -e "${YELLOW}📚 Installing dependencies...${NC}"
pip install -r requirements.txt

# Check if MongoDB is running
echo -e "${YELLOW}🔍 Checking MongoDB connection...${NC}"
if ! nc -z localhost 27017 2>/dev/null; then
    echo -e "${RED}❌ MongoDB is not running on localhost:27017${NC}"
    echo -e "${YELLOW}   Please start MongoDB first:${NC}"
    echo -e "${YELLOW}   brew services start mongodb-community${NC}"
    echo -e "${YELLOW}   or: mongod${NC}\n"
    exit 1
fi
echo -e "${GREEN}✅ MongoDB is running${NC}\n"

# Start the server
echo -e "${GREEN}🎯 Starting FastAPI server...${NC}"
echo -e "${GREEN}📡 API will be available at: http://localhost:8000${NC}"
echo -e "${GREEN}📚 API docs at: http://localhost:8000/docs${NC}\n"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
