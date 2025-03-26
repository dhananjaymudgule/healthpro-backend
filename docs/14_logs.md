
# logs


```logs/
├── app.log       # General application logs
├── db.log        # Database operations
├── chatbot.log   # Chatbot logs
├── user.log      # User authentication & management logs
├── patient.log   # Patient-related logs
```

```
healthpro-backend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging_config.py   #  Centralized logging setup
│   │   ├── db/
│   │   │   ├── repositories/
│   │   ├── modules/
│   │   ├── main.py
```


```
healthpro-backend/
├── logs/                   #  Logs will be created here (outside src/)
│   ├── app.log             # General application logs
│   ├── db.log              # Database operation logs
│   ├── chatbot.log         # Chatbot-specific logs
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── logging_config.py  # Logging setup
│   │   ├── db/
│   │   ├── modules/
│   │   ├── main.py
├── .gitignore              #  You should add /logs to .gitignore
```