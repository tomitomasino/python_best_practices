# Environment Variables Management

## Local Development
Use `.env` file ONLY for local development:

```bash
# .env
APP_NAME=IKEA API Local
ENVIRONMENT=local
DATABASE_URL=sqlite:///./local.db
DATABASE_POOL_SIZE=5
FEATURE_NEW_UI=true
```

## GitHub Environments Configuration

### Development Environment
Variables (non-sensitive):
- APP_NAME: "IKEA API Dev"
- ENVIRONMENT: "development"
- DATABASE_POOL_SIZE: "5"
- FEATURE_NEW_UI: "true"

Secrets (sensitive):
- DATABASE_URL: "postgresql://user:pass@dev-db/dev"

### Staging Environment
Variables:
- APP_NAME: "IKEA API Staging"
- ENVIRONMENT: "staging"
- DATABASE_POOL_SIZE: "10"
- FEATURE_NEW_UI: "true"

Secrets:
- DATABASE_URL: "postgresql://user:pass@staging-db/staging"

### Production Environment
Variables:
- APP_NAME: "IKEA API"
- ENVIRONMENT: "production"
- DATABASE_POOL_SIZE: "20"
- FEATURE_NEW_UI: "false"

Secrets:
- DATABASE_URL: "postgresql://user:pass@prod-db/prod"

## Best Practices
1. NEVER commit .env files to Git
2. ALL environment variables for CI/CD should be in GitHub
3. Use .env ONLY for local development
4. Use GitHub Environment Secrets for sensitive data
5. Use GitHub Environment Variables for non-sensitive data

## Running Locally
```bash
# Option 1: Use .env file
cp .env.example .env
# edit .env with your local values
python -m src.main

# Option 2: Use environment variables directly
export DATABASE_URL="sqlite:///./local.db"
export FEATURE_NEW_UI="true"
python -m src.main
```
