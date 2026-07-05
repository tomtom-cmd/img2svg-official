# ==========================================
# FORCE ADMINISTRATOR ELEVATION
# ==========================================
$IsAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (!$IsAdmin) {
    Write-Host "Requesting Administrator privileges..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# ==========================================
# AUTOMATED PATH DISCOVERY
# ==========================================
$ScriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$SourceExe = Join-Path -Path $ScriptDir -ChildPath "img2svg.exe"
$TargetFolder = "C:\Program Files\img2svg-tools"

if (!(Test-Path $SourceExe)) {
    Write-Error "Source file img2svg.exe not found alongside the installation package!"
    Start-Sleep -Seconds 5
    Exit 1
}

# ==========================================
# 1. COPY FILE TO PROGRAM FILES
# ==========================================
Write-Host "Creating installation directory..." -ForegroundColor Cyan
if (!(Test-Path $TargetFolder)) {
    New-Item -ItemType Directory -Force -Path $TargetFolder | Out-Null
}

Write-Host "Copying executable..." -ForegroundColor Cyan
Copy-Item -Path $SourceExe -Destination $TargetFolder -Force

# ==========================================
# 2. ADD TO SYSTEM PATH
# ==========================================
Write-Host "Configuring Environment PATH..." -ForegroundColor Cyan
$CurrentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
if ($CurrentPath -notlike "*$TargetFolder*") {
    $NewPath = "$CurrentPath;$TargetFolder"
    [System.Environment]::SetEnvironmentVariable("Path", $NewPath, "Machine")
    Write-Host "Successfully added to System PATH." -ForegroundColor Green
}

# ==========================================
# 3. SET UP POWERSHELL ALIAS
# ==========================================
Write-Host "Configuring PowerShell Alias..." -ForegroundColor Cyan
$PsProfileDir = Split-Path $PROFILE -Parent
if (!(Test-Path $PsProfileDir)) { New-Item -ItemType Directory -Force -Path $PsProfileDir | Out-Null }
if (!(Test-Path $PROFILE)) { New-Item -ItemType File -Force -Path $PROFILE | Out-Null }

$PsAliasBlock = @"

# Custom Image Tool Alias
function Invoke-Img2Svg {
    # $args automatically forwards everything you type after the alias
    img2svg.exe $args
}
if (!(Get-Alias i2s -ErrorAction SilentlyContinue)) {
    Set-Alias i2s Invoke-Img2Svg
}

"@

$ProfileContent = Get-Content $PROFILE -Raw -ErrorAction SilentlyContinue
if ($ProfileContent -notlike "*Invoke-Img2Svg*") {
    Add-Content -Path $PROFILE -Value $PsAliasBlock
    Write-Host "PowerShell alias written to profile." -ForegroundColor Green
}

# ==========================================
# 4. SET UP CMD ALIAS
# ==========================================
Write-Host "Configuring CMD Alias..." -ForegroundColor Cyan
$MacroFolder = "C:\tools"
$MacroFile = "$MacroFolder\macros.txt"

if (!(Test-Path $MacroFolder)) { New-Item -ItemType Directory -Force -Path $MacroFolder | Out-Null }
if (!(Test-Path $MacroFile)) { New-Item -ItemType File -Force -Path $MacroFile | Out-Null }

# We just map the wildcard token directly
$CmdAliasLine = "i2s=img2svg.exe $*"
$MacroContent = Get-Content $MacroFile -ErrorAction SilentlyContinue
if ($MacroContent -notcontains "i2s=img2svg.exe $*") {
    Add-Content -Path $MacroFile -Value $CmdAliasLine
}

# FIX: Check for and create the registry key if it does not exist
$RegistryPath = "HKCU:\Software\Microsoft\Command Processor"
if (!(Test-Path $RegistryPath)) {
    New-Item -Path "HKCU:\Software\Microsoft" -Name "Command Processor" -Force | Out-Null
}
Set-ItemProperty -Path $RegistryPath -Name "Autorun" -Value "doskey /macrofile=`"$MacroFile`"" -Force

Write-Host "CMD alias macro mapped via Registry Autorun." -ForegroundColor Green
Write-Host "`nInstallation Completed Successfully!" -ForegroundColor Magenta
Start-Sleep -Seconds 3
