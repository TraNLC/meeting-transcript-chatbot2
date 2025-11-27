#!/usr/bin/env pwsh
# Run Meeting Analyzer App with auto-setup

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "  MEETING ANALYZER PRO - STARTUP" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# 1. Setup ffmpeg PATH
$currentDir = Get-Location
$ffmpegPath = Join-Path $currentDir "ffmpeg-8.0.1-essentials_build\bin"

if (Test-Path $ffmpegPath) {
    $env:PATH = "$ffmpegPath;$env:PATH"
    Write-Host "✅ ffmpeg PATH configured" -ForegroundColor Green
} else {
    Write-Host "⚠️  ffmpeg not found (recording features may not work)" -ForegroundColor Yellow
}

# 2. Check Python
Write-Host "✅ Checking Python..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   $pythonVersion" -ForegroundColor White
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    exit 1
}

# 3. Check dependencies
Write-Host "✅ Checking dependencies..." -ForegroundColor Green
$packages = @("gradio", "whisper", "openai")
foreach ($pkg in $packages) {
    try {
        python -c "import $pkg" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✓ $pkg" -ForegroundColor Gray
        } else {
            Write-Host "   ✗ $pkg (missing)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   ✗ $pkg (missing)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "  STARTING APPLICATION" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 Starting Meeting Analyzer Pro..." -ForegroundColor Cyan
Write-Host "📍 URL: http://localhost:7779" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# 4. Run the app
python src/ui/app_v2.py
