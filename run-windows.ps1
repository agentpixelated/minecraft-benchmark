$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "[setup] Installing uv..."
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

& uv run benchmark.py @args
$code = $LASTEXITCODE
if ($code -ne 0) {
    Write-Host ""
    Write-Host "Benchmark exited with code $code" -ForegroundColor Red
}
exit $code
