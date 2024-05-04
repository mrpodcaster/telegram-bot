# Mr.Podcaster Telegram bot

## Developing

- Create new feature/<branch_name>
- Make changes
- Merge dev to your branch
- Make migrations if needed and make sure your migrations don't break anything
- Make Pull Request in GitHub
- Call @mrmamongo

## Local Environment

This project uses dockerised environment. Mandatory infrastructure is loaded in docker compose

1. Build your project
```shell
docker compose build
```

2. Setup infrastructure

```shell
docker compose up -d postgres redis
```

3. Migrate (make sure you have DJANGO_DB_URL set to local)

```shell
export DJANGO_DB_URL=postgres://yourpostgreshost
python ./manage.py migrate
```

4. Create superuser (if it not exists)

```shell
python ./manage.py createsuperuser
```

5. Load service

```shell
docker compose up web
```