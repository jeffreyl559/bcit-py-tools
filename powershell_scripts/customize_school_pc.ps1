# Today's date (or any date to test)
$today = Get-Date "2025-11-10"  # Change this to test other dates

# First day of Set 1
$startDate = Get-Date "2025-09-24"

# List of non-class days (holidays and midterms)
$nonClassDays = @(
    Get-Date "2025-09-30",
    Get-Date "2025-10-13",
    Get-Date "2025-10-17",
    Get-Date "2025-10-20",
    Get-Date "2025-10-21",
    Get-Date "2025-11-11"
)

# Last day of classes
$lastClassDate = Get-Date "2025-12-03"

# Check if date is within class period
if ($today -lt $startDate) {
    Write-Output "Classes haven't started yet."
    return
}
if ($today -gt $lastClassDate) {
    Write-Output "Classes have ended."
    return
}

# Total days difference
$totalDays = ($today - $startDate).Days

# Count full weeks and remaining days
$fullWeeks = [math]::Floor($totalDays / 7)
$extraDays = $totalDays % 7

# Count weekdays in full weeks
$weekdayCount = $fullWeeks * 5

# Count weekdays in remaining days
for ($i=0; $i -le $extraDays; $i++) {
    $currentDate = $startDate.AddDays($fullWeeks * 7 + $i)
    if ($currentDate.DayOfWeek -ne 'Saturday' -and $currentDate.DayOfWeek -ne 'Sunday') {
        $weekdayCount++
    }
}

# Subtract any non-class weekdays before or on the target date
$skipped = $nonClassDays | Where-Object { $_ -le $today -and $_.DayOfWeek -ne 'Saturday' -and $_.DayOfWeek -ne 'Sunday' }
$weekdayCount -= $skipped.Count

# Calculate set number (1 → 2 → 3 cycle)
$setNumber = ((($weekdayCount - 1) % 3) + 1)

Write-Output "Date: $today"
Write-Output "Set number: $setNumber"


# Set Combine taskbar buttons - When taskbar is full
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "TaskbarGlomLevel" -Value 1

# Set Combine taskbar buttons on other taskbars - When taskbar is full
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "MMTaskbarGlomLevel" -Value 1

# Set When using multiple displays, show my taskbar apps on - taskbar where window is open
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name MMTaskbarMode -Value 2

# Set Taskbar alignment to Left (0 = Left, 1 = Center)
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "TaskbarAl" -Value 0

# Restart Explorer to apply changes
Write-Host "Applying changes by restarting Explorer..." -ForegroundColor Cyan
Stop-Process -Name explorer -Force
Start-Process explorer

# Install Notion
Invoke-WebRequest -Uri "https://www.notion.so/desktop/windows/download" -OutFile "$env:USERPROFILE\Downloads\NotionSetup.exe"
Start-Process "$env:USERPROFILE\Downloads\NotionSetup.exe"

# Install VSCode
winget install --id  Microsoft.VisualStudioCode -e --accept-package-agreements --accept-source-agreements

# Install Python 3.13.7
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe" -OutFile "$env:TEMP\python-latest.exe"; Start-Process "$env:TEMP\python-latest.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait

$urls = @(
 "https://learn.bcit.ca/",
 "https://chromewebstore.google.com/detail/ublock-origin-lite/ddkjiahejlhfcafbddmgiahcphecmpfh?hl=en"
)

# Open Chrome to open to D2L, Ublock Origin Lite
Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" ("--new-window " + ($urls -join " "))
