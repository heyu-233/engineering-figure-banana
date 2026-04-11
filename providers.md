# Provider Compatibility

This project is intentionally provider-neutral, but it is not provider-agnostic in the sense of hiding all differences. Users still need to set the correct endpoint, auth mode, and model names for their own backend.

## Recommended Public Stance

- treat the official Google Gemini endpoint as the reference setup in public docs
- treat relays and custom providers as optional compatibility paths
- never hardcode a personal relay endpoint or private billing setup into shared instructions

## Quick Compatibility Table

| Provider type | Typical base URL | Typical auth mode | Third-party flag | High-res model handling |
| --- | --- | --- | --- | --- |
| Official Google Gemini | `https://generativelanguage.googleapis.com` | `google` | not needed | optional `NANOBANANA_HIGHRES_MODEL` |
| Gemini-compatible relay | provider-specific | usually `bearer` | usually required | provider-specific model name |
| Custom internal endpoint | internal endpoint | provider-specific | usually required | provider-specific model name |

## What Usually Changes Between Providers

- `NANOBANANA_BASE_URL`
- model naming conventions
- auth mode (`google` vs `bearer`)
- whether a separate high-resolution model exists
- rate limits, quotas, and billing behavior
- how closely the provider follows the official API behavior

## Official Google Reference Pattern

```env
NANOBANANA_BASE_URL=https://generativelanguage.googleapis.com
NANOBANANA_DEFAULT_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_HIGHRES_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_AUTH_MODE=google
```

## Third-Party Relay Pattern

```env
NANOBANANA_BASE_URL=https://your-relay.example.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
```

## Safety Notes

- only enable `NANOBANANA_ALLOW_THIRD_PARTY=1` when you intentionally trust the relay
- verify how the provider handles uploaded files, prompts, and API keys before sending sensitive material
- if high-resolution output matters, confirm the provider really exposes a distinct high-res model instead of assuming the default model is enough
