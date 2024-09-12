llm_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── containers.py
│   ├── api/
│   │   ├── chat_endpoints.py
│   │   └── resume_endpoints.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   ├── dao/
│   │   ├── dao.py
│   │   └── database.py
│   ├── database/
│   │   └── resume_data.db
│   ├── models/
│   │   ├── chunks.py
│   │   ├── index.py
│   │   └── resume.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm.py
│   │   └── resume_processor.py
│   │   └── faiss_optimizer.py
│   │   └── index_manager.py
│   └── db/
│       ├── __init__.py
│       └── database.py
├── tests/
│   ├── __init__.py
│   ├── cv_test_i
│   ├── test_function_i.py
│   └── test-api.py
├── .env
├── Dockerfile
├── docker-compose.yml
└── requirements.txt