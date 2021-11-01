Simple script used to fetch documents from a SharePoint directory en masse.

SharePoint host must be passed via environment variable `HOST`
and should be of the form
`https://<HOSTNAME>/sites/<SITE ID>/_layouts/<DIRECTORY ID>/download.aspx`.

NTLM domain, username, and password must be passed via environment variables
`DOMAIN`, `USERNAME`, and `PASSWORD`.

Document listing CSV must be provided via stdin. Obtain using SharePoint
"Export to Excel" item in the Library tab, and save as CSV. Rows must contain
the following columns: `Name`, `Path`, `Item Type`.

The exported CSV will likely have a UTF8 BOM at the beginning, use
`strip-boms.py` to remove it, overwriting all file paths passed as arguments:

`$ python strip-boms.py file1.csv file2.csv`

Dependencies are managed using [poetry](https://python-poetry.org/).
