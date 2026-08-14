# BoloUp API (Python FastAPI)

BoloUp-style Live Streaming + Voice Room backend starter.

## Features
- JWT Authentication
- User system + Coins
- Voice/Video Rooms
- Gift system
- WebSocket real-time room chat

## Setup

```bash
git clone <your-repo>
cd boloup-api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python run.py
