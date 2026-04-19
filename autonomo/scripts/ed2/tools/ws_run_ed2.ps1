param(
    [ValidateSet("bootstrap","update","diag","phase1","phase2","full","verify","package","shell")]
    [string]$Action = "diag",

    [string]$BaseDir = "C:\Users\Civil\Documents\taha",
    [string]$RepoDirName = "ucn_adse",
    [string]$RepoUrl = "",
    [string]$Branch = "master",
    [string]$PythonExe = "python",
    [switch]$CreateIfMissing,
    [switch]$InstallComtypes,
    [string]$ModelName = "Edificio2_parte1_oficial.edb",
    [string]$TransferTag = "preliminar_ws"
)

$ErrorActionPreference = "Stop"

function Step($msg) {
    Write-Host ""
    Write-Host "==> $msg" -ForegroundColor Cyan
}

function Resolve-RepoPaths {
    $repoDir = Join-Path $BaseDir $RepoDirName
    $ed2Dir = Join-Path $repoDir "autonomo\scripts\ed2"
    $modelPath = Join-Path (Join-Path $BaseDir "models") $ModelName

    [pscustomobject]@{
        RepoDir = $repoDir
        Ed2Dir = $ed2Dir
        ModelPath = $modelPath
    }
}

function Ensure-BaseDir {
    if (-not (Test-Path $BaseDir)) {
        Step "Creating base dir $BaseDir"
        New-Item -ItemType Directory -Path $BaseDir | Out-Null
    }
}

function Ensure-Python {
    Step "Checking Python"
    & $PythonExe --version
}

function Ensure-Comtypes {
    Step "Checking comtypes"
    & $PythonExe -c "import importlib.util, sys; spec = importlib.util.find_spec('comtypes'); print('installed' if spec else 'missing'); sys.exit(0 if spec else 1)"
    if ($LASTEXITCODE -ne 0) {
        if (-not $InstallComtypes) {
            throw "comtypes no esta instalado. Repite agregando -InstallComtypes."
        }
        Step "Installing comtypes"
        & $PythonExe -m pip install --upgrade pip
        & $PythonExe -m pip install comtypes
    }
}

function Ensure-Repo {
    param($paths)

    if (-not (Test-Path (Join-Path $paths.RepoDir ".git"))) {
        if ([string]::IsNullOrWhiteSpace($RepoUrl)) {
            throw "No existe repo local y no se entrego -RepoUrl."
        }
        Step "Cloning repo into $($paths.RepoDir)"
        git clone --branch $Branch $RepoUrl $paths.RepoDir
    }
    else {
        Step "Repo already exists"
        Write-Host $paths.RepoDir
    }
}

function Update-Repo {
    param($paths)

    if (-not (Test-Path (Join-Path $paths.RepoDir ".git"))) {
        throw "No existe repo local en $($paths.RepoDir). Corre bootstrap primero."
    }
    Step "Updating repo"
    Push-Location $paths.RepoDir
    try {
        git fetch --all --prune
        git checkout $Branch
        git pull --ff-only
    }
    finally {
        Pop-Location
    }
}

function Invoke-Ed2Python {
    param(
        $paths,
        [string]$ScriptName,
        [string[]]$ScriptArgs = @()
    )

    if (-not (Test-Path $paths.Ed2Dir)) {
        throw "No existe carpeta Ed.2: $($paths.Ed2Dir)"
    }

    $env:ED2_RUNTIME_ROOT = $BaseDir
    Push-Location $paths.Ed2Dir
    try {
        & $PythonExe $ScriptName @ScriptArgs
    }
    finally {
        Pop-Location
    }
}

function Run-Diag {
    param($paths)

    $args = @()
    if ($CreateIfMissing) {
        $args += "--create-if-missing"
    }
    Invoke-Ed2Python -paths $paths -ScriptName "diag.py" -ScriptArgs $args
}

function Run-Phase1 {
    param($paths)

    $args = @("--phase", "1", "--model", $paths.ModelPath)
    if ($CreateIfMissing) {
        $args += "--create-if-missing"
    }
    Invoke-Ed2Python -paths $paths -ScriptName "run_pipeline_ed2.py" -ScriptArgs $args
}

function Run-Phase2 {
    param($paths)

    $args = @("--phase", "2", "--model", $paths.ModelPath)
    if ($CreateIfMissing) {
        $args += "--create-if-missing"
    }
    Invoke-Ed2Python -paths $paths -ScriptName "run_pipeline_ed2.py" -ScriptArgs $args
}

function Run-Full {
    param($paths)

    $args = @("--model", $paths.ModelPath)
    if ($CreateIfMissing) {
        $args += "--create-if-missing"
    }
    Invoke-Ed2Python -paths $paths -ScriptName "run_pipeline_ed2.py" -ScriptArgs $args
}

function Run-Verify {
    param($paths)
    Invoke-Ed2Python -paths $paths -ScriptName "verify_ed2.py"
}

function Run-Package {
    param($paths)
    Invoke-Ed2Python -paths $paths -ScriptName "package_transfer_ed2.py" -ScriptArgs @("--tag", $TransferTag)
}

Ensure-BaseDir
Ensure-Python
Ensure-Comtypes

$paths = Resolve-RepoPaths

if ($Action -in @("diag","phase1","phase2","full","verify","package")) {
    if (-not (Test-Path (Join-Path $paths.RepoDir ".git"))) {
        throw "No existe repo local en $($paths.RepoDir). Corre bootstrap primero."
    }
}

switch ($Action) {
    "bootstrap" {
        Ensure-Repo -paths $paths
        Step "Bootstrap complete"
        Write-Host "RepoDir:   $($paths.RepoDir)"
        Write-Host "ED2 dir:   $($paths.Ed2Dir)"
        Write-Host "ModelPath: $($paths.ModelPath)"
        Write-Host "Runtime:   $BaseDir"
    }
    "update" {
        Update-Repo -paths $paths
    }
    "diag" {
        Run-Diag -paths $paths
    }
    "phase1" {
        Run-Phase1 -paths $paths
    }
    "phase2" {
        Run-Phase2 -paths $paths
    }
    "full" {
        Run-Full -paths $paths
    }
    "verify" {
        Run-Verify -paths $paths
    }
    "package" {
        Run-Package -paths $paths
    }
    "shell" {
        Step "Environment"
        Write-Host "RepoDir:   $($paths.RepoDir)"
        Write-Host "ED2 dir:   $($paths.Ed2Dir)"
        Write-Host "ModelPath: $($paths.ModelPath)"
        Write-Host "Runtime:   $BaseDir"
    }
}
