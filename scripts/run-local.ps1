# Run Django API locally (from repo root: .\scripts\run-local.ps1)
$ErrorActionPreference = "Stop"
$serverRoot = Join-Path (Join-Path $PSScriptRoot "..") "server" | Resolve-Path
Set-Location $serverRoot

if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    python -m venv .venv
}
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created server/.env from .env.example - edit SECRET_KEY for non-local use." -ForegroundColor Yellow
}
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
Write-Host ""
Write-Host "Starting Django at http://127.0.0.1:8000/ - serve client/ over http (e.g. Live Server)." -ForegroundColor Green
python manage.py runserver 127.0.0.1:8000
