Set-ExecutionPolicy Bypass -Scope Process

Add-WindowsFeature web-server
Add-WindowsFeature web-webserver
Add-WindowsFeature web-mgmt-tools
Add-WindowsFeature web-common-http
Add-WindowsFeature web-appinit
Add-WindowsFeature web-asp
Add-WindowsFeature web-mgmt-compat
Add-WindowsFeature web-net-ext
Add-WindowsFeature web-net-ext45
Add-WindowsFeature web-asp-net
Add-WindowsFeature web-asp-net45
Add-WindowsFeature web-isapi-ext
Add-WindowsFeature web-isapi-filter
Add-WindowsFeature web-mgmt-console
Add-WindowsFeature net-framework-features
Add-WindowsFeature net-framework-core
Add-WindowsFeature net-framework-45-features
Add-WindowsFeature net-framework-45-core
Add-WindowsFeature net-http-activation
Add-WindowsFeature net-non-http-activ
Add-WindowsFeature net-framework-45-aspnet
Add-WindowsFeature net-wcf-services45
