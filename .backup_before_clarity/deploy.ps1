# Bluehost FTP Deployment Script
# This script uploads your website files to Bluehost via FTP

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Bluehost Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if deploy-config.json exists
if (-not (Test-Path "deploy-config.json")) {
    Write-Host "ERROR: deploy-config.json not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please create deploy-config.json based on deploy-config-template.json" -ForegroundColor Yellow
    Write-Host "Steps:" -ForegroundColor Yellow
    Write-Host "  1. Copy deploy-config-template.json to deploy-config.json" -ForegroundColor Yellow
    Write-Host "  2. Fill in your Bluehost FTP credentials" -ForegroundColor Yellow
    Write-Host "  3. Run this script again" -ForegroundColor Yellow
    exit 1
}

# Load configuration
$config = Get-Content "deploy-config.json" | ConvertFrom-Json

Write-Host "Configuration loaded:" -ForegroundColor Green
Write-Host "  Host: $($config.host)" -ForegroundColor Gray
Write-Host "  Username: $($config.username)" -ForegroundColor Gray
Write-Host "  Remote Path: $($config.remote_path)" -ForegroundColor Gray
Write-Host ""

# Check if WinSCP is installed
$winscpPath = "C:\Program Files (x86)\WinSCP\WinSCP.com"
if (-not (Test-Path $winscpPath)) {
    Write-Host "WARNING: WinSCP not found at $winscpPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This script uses WinSCP for reliable FTP deployment." -ForegroundColor Yellow
    Write-Host "Download WinSCP from: https://winscp.net/eng/download.php" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative: Use the lftp-based deploy.sh script with Git Bash" -ForegroundColor Yellow
    exit 1
}

# Create WinSCP script
$scriptContent = @"
option batch abort
option confirm off
open ftp://$($config.username):$($config.password)@$($config.host):$($config.port)
cd $($config.remote_path)
option transfer binary
put *.html
put *.css
put -filemask="|.git/" assets/
put -filemask="|.git/" blog/
put -filemask="|.git/" practice-areas/
close
exit
"@

$scriptPath = ".\deploy-script.tmp"
$scriptContent | Out-File -FilePath $scriptPath -Encoding ASCII

Write-Host "Starting deployment..." -ForegroundColor Cyan
Write-Host ""

# Execute WinSCP
& $winscpPath /script=$scriptPath /log="deploy.log"

# Clean up
Remove-Item $scriptPath -ErrorAction SilentlyContinue

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Deployment completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Deployment failed! Check deploy.log for details." -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    exit 1
}
