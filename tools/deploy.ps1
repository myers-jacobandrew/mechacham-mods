<#
.SYNOPSIS
  Copies a freshly-cooked DLC plugin's outputs into the Steam Workshop staging
  folder and (optionally) runs steamcmd to upload via the vdf.

.DESCRIPTION
  Run this AFTER cooking the DLC profile in UE's Project Launcher.

  It will:
    1. Copy .pak/.ucas/.utoc and AssetRegistry.bin from the plugin's
       Saved/StagedBuilds + Saved/Cooked into the workshop folder.
    2. Bump the changenote in the vdf (if -ChangeNote is supplied).
    3. Run steamcmd +login +workshop_build_item +quit (if -Upload is set).

.PARAMETER ModName
  Plugin folder name. e.g. "Windfall". Must match exactly.

.PARAMETER ProjectDir
  Root of the UE project, e.g. "C:\MechaCham Maps\MecchaCModKit_Load".

.PARAMETER WorkshopDir
  Workshop staging folder, e.g. "C:\Steamworkshop\Windfall".

.PARAMETER SteamCmdPath
  Path to steamcmd.exe. Defaults to C:\Steamworkshop\SteamCmd\steamcmd.exe.

.PARAMETER SteamUser
  Steam username (required if -Upload). steamcmd will reuse cached creds
  if you've logged in there before; otherwise it'll prompt interactively.

.PARAMETER ChangeNote
  Optional. New value for the vdf "changenote" field. Quote it.

.PARAMETER Upload
  If set, runs steamcmd to push to the Workshop after copying. Otherwise
  just stages the files locally.

.EXAMPLE
  # Stage files only (no upload).
  .\deploy.ps1 -ModName Windfall

.EXAMPLE
  # Stage + upload + bump changenote.
  .\deploy.ps1 -ModName Windfall -SteamUser hinko13 -ChangeNote "v1.0.7 - more polish" -Upload
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)]
  [string]$ModName,

  [string]$ProjectDir   = "C:\MechaCham Maps\MecchaCModKit_Load",
  [string]$WorkshopDir,
  [string]$SteamCmdPath = "C:\Steamworkshop\SteamCmd\steamcmd.exe",
  [string]$SteamUser,
  [string]$ChangeNote,
  [switch]$Upload
)

$ErrorActionPreference = "Stop"

if (-not $WorkshopDir) { $WorkshopDir = "C:\Steamworkshop\$ModName" }

$pakBase = "$ModName" + "MecchaCModKit_Load-Windows"
$srcPaks = Join-Path $ProjectDir "Plugins\$ModName\Saved\StagedBuilds\Windows\MecchaCModKit_Load\Plugins\$ModName\Content\Paks\Windows"
$srcAR   = Join-Path $ProjectDir "Plugins\$ModName\Saved\Cooked\Windows\MecchaCModKit_Load\Plugins\$ModName"

# Sanity check sources
$pakSrc  = Join-Path $srcPaks "$pakBase.pak"
$ucasSrc = Join-Path $srcPaks "$pakBase.ucas"
$utocSrc = Join-Path $srcPaks "$pakBase.utoc"
$arSrc   = Join-Path $srcAR   "AssetRegistry.bin"

foreach ($f in @($pakSrc, $ucasSrc, $utocSrc, $arSrc)) {
  if (-not (Test-Path $f)) {
    throw "Missing cook output: $f. Did the cook finish successfully?"
  }
}
if (-not (Test-Path $WorkshopDir)) {
  throw "Workshop folder not found: $WorkshopDir"
}

# Copy
Write-Host "Copying cook outputs to $WorkshopDir..." -ForegroundColor Cyan
Copy-Item -Force $pakSrc, $ucasSrc, $utocSrc, $arSrc $WorkshopDir
$ucasSize = [math]::Round((Get-Item (Join-Path $WorkshopDir "$pakBase.ucas")).Length / 1MB, 2)
Write-Host "  staged. ucas = $ucasSize MB" -ForegroundColor Green

# Bump changenote in vdf
$vdf = Join-Path $WorkshopDir "$ModName.vdf"
if (-not (Test-Path $vdf)) { throw "vdf not found: $vdf" }

if ($ChangeNote) {
  Write-Host "Bumping changenote in $vdf..." -ForegroundColor Cyan
  $text = Get-Content $vdf -Raw
  $escaped = $ChangeNote -replace '"', '\"'
  $text = [regex]::Replace($text, '"changenote"\s*"[^"]*"', "`"changenote`"`t`t`"$escaped`"")
  Set-Content -NoNewline -Path $vdf -Value $text
  Write-Host "  done." -ForegroundColor Green
}

# Upload
if ($Upload) {
  if (-not $SteamUser) { throw "-Upload requires -SteamUser" }
  if (-not (Test-Path $SteamCmdPath)) { throw "steamcmd not found: $SteamCmdPath" }

  Write-Host "Running steamcmd upload..." -ForegroundColor Cyan
  & $SteamCmdPath "+login" $SteamUser "+workshop_build_item" $vdf "+quit"
  if ($LASTEXITCODE -ne 0) {
    Write-Warning "steamcmd exited with code $LASTEXITCODE"
  } else {
    Write-Host "Upload finished. Check the workshop page to confirm." -ForegroundColor Green
  }
} else {
  Write-Host "Done. Run with -Upload -SteamUser <name> to push to Workshop." -ForegroundColor Yellow
  Write-Host "Or manually: `"$SteamCmdPath`" then 'workshop_build_item `"$vdf`"'" -ForegroundColor Yellow
}
