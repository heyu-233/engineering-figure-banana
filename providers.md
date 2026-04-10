# Provider Compatibility

This skill is designed to be provider-neutral and compatible with multiple Gemini-style image backends.

## Supported Provider Patterns

- Official Google Gemini API
- Third-party Gemini-compatible relays
- Custom internal or hosted providers that expose a Gemini-like image endpoint

## What Usually Changes Between Providers

- `NANOBANANA_BASE_URL`
- model naming conventions
- auth mode (`google` vs `bearer`)
- whether a separate high-resolution model exists
- rate limits, quotas, and billing behavior
- how closely the provider follows the official API behavior

## Official Google Reference Pattern

Typical configuration:

```env
NANOBANANA_BASE_URL=https://generativelanguage.googleapis.com
NANOBANANA_DEFAULT_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_HIGHRES_MODEL=gemini-3.1-flash-image-preview
NANOBANANA_AUTH_MODE=google
```

Use this as the reference configuration in public docs unless there is a strong reason not to.

## Third-Party Relay Pattern

Typical configuration:

```env
NANOBANANA_BASE_URL=https://your-relay.example.com
NANOBANANA_DEFAULT_MODEL=<your-default-image-model>
NANOBANANA_HIGHRES_MODEL=<your-highres-image-model>
NANOBANANA_AUTH_MODE=bearer
NANOBANANA_ALLOW_THIRD_PARTY=1
```

Notes:

- Keep relay examples generic in public repositories
- Do not present a personal or private relay as the canonical default
- Users must replace the endpoint and model names with values from their own provider

## Publishing Recommendation

For a public repository:

- treat official Google as the reference setup
- treat third-party relays as optional compatibility paths
- keep secrets and private endpoints out of version control
- explain that provider-specific model names may differ

## Safety Recommendation

This skill intentionally requires explicit opt-in for non-official endpoints when user files or keys are involved.

If you use a relay:

- make sure you trust the provider
- set `NANOBANANA_ALLOW_THIRD_PARTY=1` only when intended
- review provider data handling before sending sensitive inputs
