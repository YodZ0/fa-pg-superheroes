## SuperHero API

### Installation

Clone repository:

```commandline
git clone https://github.com/YodZ0/fa-pg-superheroes.git
```

### Preparations

1. Get [SuperHero API](https://superheroapi.com) access token
2. Create `.env` file according to `.env.template`

### Create venv
```commandline
poetry install
```

### Run application

Create and build Docker container:
```commandline
docker compose -f docker-compose.yml up -d --build
```
or
```commandline
make build
```

See the Doc on [localhost](http://localhost:8000/docs)
