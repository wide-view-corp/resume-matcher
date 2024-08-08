llm_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints.py
│   │   └── resume_endpoints.py
│   │   └── chat_endpoints.py 
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   └── resume_processor.py
│   │   └── faiss_optimizer.py
│   │   └── chatbot.py
│   └── db/
│       ├── __init__.py
│       └── database.py
├── tests/
│   ├── test_api.py
│   └── test_resume_processor.py
├── .env
├── Dockerfile
├── docker-compose.yml
└── requirements.txt