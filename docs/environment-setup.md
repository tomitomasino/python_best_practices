# Environment Configuration Guide

## GitHub Repository Configuration

### Variables (Non-sensitive)
Set these in GitHub repository settings under "Variables":

For each environment (development/staging/production):
1. Go to Settings > Environments > Select environment
2. Add environment variables:
   - APP_NAME: "IKEA API"
   - DATABASE_POOL_SIZE: "5"
   - MAINTENANCE_MODE: "false"
   - DEPLOYMENT_ENABLED: "true"
   - FEATURE_NEW_UI: "true/false"
   - FEATURE_BETA_API: "true/false"

### Secrets (Sensitive)
Set these in GitHub repository settings under "Secrets":

For each environment:
1. Go to Settings > Environments > Select environment
2. Add secrets:
   - DATABASE_URL
   - API_KEYS
   - OTHER_SENSITIVE_DATA

## Local Development
1. Copy `.env.example` to `.env`
2. Update values for local development
3. Never commit `.env` file

## Environment Variable Precedence
1. GitHub Environment Secrets (highest)
2. GitHub Environment Variables
3. Repository Secrets
4. Repository Variables
5. Default values in code (lowest)
