param(
    [string]$SecretsDir = "$HOME/.codex/secrets",
    [string]$SkillDir = "$HOME/.codex/skills/engineering-figure-banana"
)

$ErrorActionPreference = "Continue"

function Write-Check($status, $message) {
    switch ($status) {
        "PASS" { Write-Host "[PASS] $message" -ForegroundColor Green }
        "WARN" { Write-Host "[WARN] $message" -ForegroundColor Yellow }
        "FAIL" { Write-Host "[FAIL] $message" -ForegroundColor Red }
        default { Write-Host "[$status] $message" }
    }
}

$failed = $false

Write-Host "Engineering Figure Banana setup check"
Write-Host "SkillDir   : $SkillDir"
Write-Host "SecretsDir : $SecretsDir"
Write-Host ""

if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version 2>&1
    Write-Check "PASS" "Python detected: $pythonVersion"
} else {
    Write-Check "FAIL" "Python not found in PATH"
    $failed = $true
}

if (Test-Path $SkillDir) {
    Write-Check "PASS" "Skill directory exists"
} else {
    Write-Check "FAIL" "Skill directory missing: $SkillDir"
    $failed = $true
}

$requiredFiles = @(
    "SKILL.md",
    "agents/openai.yaml",
    "scripts/generate_image.py",
    "scripts/load_nanobanana_env.ps1",
    "references/engineering-figure-templates.json"
)

foreach ($rel in $requiredFiles) {
    $path = Join-Path $SkillDir $rel
    if (Test-Path $path) {
        Write-Check "PASS" "Found $rel"
    } else {
        Write-Check "FAIL" "Missing $rel"
        $failed = $true
    }
}

$envFile = Join-Path $SecretsDir "nanobanana.env"
$keyFile = Join-Path $SecretsDir "nanobanana_api_key.txt"

if (Test-Path $envFile) {
    Write-Check "PASS" "Found nanobanana.env"
    $envMap = @{}
    Get-Content -Path $envFile | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $envMap[$parts[0].Trim()] = $parts[1].Trim()
        }
    }

    foreach ($name in @("NANOBANANA_BASE_URL", "NANOBANANA_DEFAULT_MODEL", "NANOBANANA_AUTH_MODE")) {
        if ($envMap.ContainsKey($name) -and $envMap[$name]) {
            Write-Check "PASS" "$name is set"
        } else {
            Write-Check "WARN" "$name is not set in nanobanana.env"
        }
    }

    if ($envMap.ContainsKey("NANOBANANA_BASE_URL")) {
        $baseUrl = $envMap["NANOBANANA_BASE_URL"]
        if ($baseUrl -eq "https://generativelanguage.googleapis.com") {
            Write-Check "PASS" "Official Google endpoint configured"
        } else {
            Write-Check "WARN" "Third-party or custom endpoint configured: $baseUrl"
            if (($envMap["NANOBANANA_ALLOW_THIRD_PARTY"] -ne "1")) {
                Write-Check "WARN" "NANOBANANA_ALLOW_THIRD_PARTY is not set to 1"
            }
        }
    }
} else {
    Write-Check "FAIL" "Missing nanobanana.env: $envFile"
    $failed = $true
}

if (Test-Path $keyFile) {
    $key = (Get-Content -Raw -Path $keyFile).Trim()
    if (-not $key) {
        Write-Check "FAIL" "nanobanana_api_key.txt is empty"
        $failed = $true
    } elseif ($key -eq "REPLACE_WITH_YOUR_CURRENT_VALID_NANOBANANA_API_KEY") {
        Write-Check "FAIL" "nanobanana_api_key.txt still contains the placeholder value"
        $failed = $true
    } else {
        Write-Check "PASS" "Found non-placeholder API key file"
    }
} else {
    Write-Check "FAIL" "Missing nanobanana_api_key.txt: $keyFile"
    $failed = $true
}

Write-Host ""
if ($failed) {
    Write-Host "Setup check finished with errors." -ForegroundColor Red
    exit 1
}

Write-Host "Setup check finished successfully." -ForegroundColor Green
exit 0
