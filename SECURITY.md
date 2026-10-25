# Security Policy

## Reporting a vulnerability

Please do not open public issues for secrets or exploitable vulnerabilities.
Contact the repository owner privately through GitHub's security reporting feature.

## Secret handling

- Never commit `.env`, access tokens, AWS credentials, or customer data.
- Use environment variables or an approved secret manager.
- Use least-privilege AWS IAM credentials and rotate any exposed credentials.
- Treat model output and API responses as untrusted input.
