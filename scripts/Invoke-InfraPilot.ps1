<#
.SYNOPSIS
Runs InfraPilot with Python. It only reads local diagnostic information.
#>
param(
    [string]$Output = "reports\\infrapilot-report.json"
)

python -m infrapilot.cli --output $Output
