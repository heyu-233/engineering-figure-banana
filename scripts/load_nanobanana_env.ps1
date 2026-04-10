param(
    [string]$SecretsDir = "$HOME/.codex/secrets"
)

$envFile = Join-Path $SecretsDir 'nanobanana.env'
$keyFileDefault = Join-Path $SecretsDir 'nanobanana_api_key.txt'

if (-not (Test-Path $envFile)) {
    throw "Secrets file not found: $envFile"
}

Get-Content -Path $envFile | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith('#')) { return }
    $parts = $line -split '=', 2
    if ($parts.Count -ne 2) { return }
    $name = $parts[0].Trim()
    $value = $parts[1].Trim()
    [Environment]::SetEnvironmentVariable($name, $value, 'Process')
}

$keyFile = $env:NANOBANANA_API_KEY_FILE
if (-not $keyFile) {
    $keyFile = $keyFileDefault
    [Environment]::SetEnvironmentVariable('NANOBANANA_API_KEY_FILE', $keyFile, 'Process')
}

if (-not (Test-Path $keyFile)) {
    throw "API key file not found: $keyFile"
}

$key = (Get-Content -Path $keyFile -Raw).Trim()
if (-not $key -or $key -eq 'REPLACE_WITH_YOUR_CURRENT_VALID_NANOBANANA_API_KEY') {
    throw "API key file is missing a real key: $keyFile"
}

[Environment]::SetEnvironmentVariable('NANOBANANA_API_KEY', $key, 'Process')

Write-Host "Loaded NANOBANANA_* env vars from $SecretsDir"
Write-Host "NANOBANANA_BASE_URL=$env:NANOBANANA_BASE_URL"
Write-Host "NANOBANANA_DEFAULT_MODEL=$env:NANOBANANA_DEFAULT_MODEL"
Write-Host "NANOBANANA_HIGHRES_MODEL=$env:NANOBANANA_HIGHRES_MODEL"
Write-Host "NANOBANANA_AUTH_MODE=$env:NANOBANANA_AUTH_MODE"
