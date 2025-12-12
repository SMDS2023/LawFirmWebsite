# Setup Scheduled Task for Blog Topic Generator
# Run this script as Administrator to create the scheduled task

$taskName = "LotterLaw Blog Topic Generator"
$batPath = "C:\Users\jeff\OneDrive\Documents\LotterLaw\Website\scripts\run_blog_generator.bat"
$workDir = "C:\Users\jeff\OneDrive\Documents\LotterLaw\Website"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$taskName' already exists. Removing and recreating..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create the action
$action = New-ScheduledTaskAction -Execute $batPath -WorkingDirectory $workDir

# Create the trigger (daily at 6:00 AM)
$trigger = New-ScheduledTaskTrigger -Daily -At "6:00AM"

# Create settings
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Daily blog topic suggestions based on calendar and case files"

Write-Host ""
Write-Host "Scheduled task '$taskName' created successfully!"
Write-Host "  Trigger: Daily at 6:00 AM"
Write-Host "  Script: $batPath"
Write-Host ""
Write-Host "To test the task, run:"
Write-Host "  schtasks /run /tn `"$taskName`""
