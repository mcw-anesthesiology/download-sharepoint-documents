Simple script used to fetch documents from a SharePoint directory en masse.

SharePoint host must be passed via environment variable `HOST`
and should be of the form
`https://<HOSTNAME>/sites/<SITE ID>/_layouts/<DIRECTORY ID>/download.aspx`.

NTLM domain, username, and password must be passed via environment variables
`DOMAIN`, `USERNAME`, and `PASSWORD`.

Dependencies are managed using [poetry](https://python-poetry.org/).
