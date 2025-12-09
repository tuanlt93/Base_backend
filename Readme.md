project/
│── main.py
│── core/
│     ├── config.py
│     ├── security.py
│     ├── cache.py          # Redis
│     ├── mq.py             # Kafka/RabbitMQ
│     └── db.py             # DB read/write split
│
├── routers/
├── schemas/
├── crud/
├── database/
│     ├── base.py
│     ├── models.py
│     └── migrations/
│
├── scripts/
│     ├── start.sh          # start uvicorn multi-workers
│     └── seed_admin.py     # init admin
│
└── deploy/
      ├── nginx.conf
      ├── docker-compose.yml
      └── supervisor.conf
