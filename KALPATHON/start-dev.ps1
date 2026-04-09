$ErrorActionPreference = "Stop"

Write-Host "Starting backend (uvicorn) and frontend (vite)..." -ForegroundColor Cyan

function Stop-ProcessOnPort {
  param([int]$Port)

  try {
    $connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($connections) {
      $pids = $connections | Select-Object -ExpandProperty OwningProcess -Unique
      foreach ($pid in $pids) {
        if ($pid -and $pid -ne 0) {
          try {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process $pid on port $Port" -ForegroundColor Yellow
          }
          catch {
          }
        }
      }
    }
  }
  catch {
  }
}

Stop-ProcessOnPort -Port 8000
Stop-ProcessOnPort -Port 5173

$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
$pythonExe = if (Test-Path $venvPython) { $venvPython } else { "python" }

$backend = Start-Process -FilePath $pythonExe `
  -ArgumentList "-m uvicorn backend_api:app --host 127.0.0.1 --port 8000 --reload" `
  -WorkingDirectory $PSScriptRoot `
  -PassThru

$backendReady = $false
for ($i = 0; $i -lt 20; $i++) {
  if ($backend.HasExited) {
    throw "Backend process exited unexpectedly."
  }

  try {
    $resp = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 2
    if ($resp.StatusCode -eq 200) {
      $backendReady = $true
      break
    }
  }
  catch {
  }

  Start-Sleep -Milliseconds 500
}

if (-not $backendReady) {
  if ($backend -and !$backend.HasExited) {
    Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
  }
  throw "Backend did not become healthy on http://127.0.0.1:8000/health"
}

Write-Host "Backend is healthy on port 8000" -ForegroundColor Green

try {
  Set-Location $PSScriptRoot
  npm run dev
}
finally {
  if ($backend -and !$backend.HasExited) {
    Write-Host "Stopping backend..." -ForegroundColor Yellow
    Stop-Process -Id $backend.Id -Force
  }
}
