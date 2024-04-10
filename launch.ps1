[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [String[]] $envFile = @(
        "${PSScriptRoot}/atest/env/default.env",
        "${PSScriptRoot}/atest/env/default.secret.env"
    )
)

<#
.SYNOPSIS
    Source environment variables from local .env files.
.NOTES
    Inspired by: https://www.powershellgallery.com/packages/dotenv/0.1.0/Content/dotenv.psm1
#>
Function Import-Dotenv {
    [CmdletBinding(SupportsShouldProcess = $true)]
    [OutputType([System.Object[]])]
    param(
        [switch] $Recurse,
        [string] $Path = ".env",
        [switch] $PassThru
    )
    [hashtable[]] $dotenvAddedVariables = @() # a special var that tells us what we added
    $lineCursor = 0

    $content = Get-Content $Path -ErrorAction SilentlyContinue
    $content.foreach{
        [string] $line = $_.trim()
        if ($line -like "#*") {
            Write-Verbose "Found comment $line $lineCursor. discarding"
        }
        elseif ($line -eq "") {
            Write-Verbose "Found a blank line at line $lineCursor, discarding"
        }
        else {
            $eq = $line.IndexOf('=')
            $fq = $eq + 1
            $key = $line.Substring(0, $eq).trim()
            $value = $line.substring($fq, $line.Length - $fq).trim()
            Write-Verbose "Found [$key=$value]"

            if ($value -match "`'|`"") {
                Write-Verbose "`tQuoted value found, trimming quotes"
                $value = $value.trim('"').trim("'")
                Write-Verbose "`tValue is now $value"
            }

            [System.Environment]::SetEnvironmentVariable($key, $value, "Process")

            $dotenvAddedVariables += @{ $key = $value }
        }
        $lineCursor++
    }

    if ($PassThru) {
        Write-Verbose "PassThru was specified, returning the array of found vars"
        return $dotenvAddedVariables
    }
}

$envFile.foreach{
    Write-Verbose "Sourcing file $_"
    Import-Dotenv -Path $_
}
Invoke-Expression "code workspace.code-workspace"
