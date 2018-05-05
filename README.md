# Django - CAE Home App

## Description

A group of Django Apps to function as the "core"" for future CAE Center projects.

Intended to be as general as possible.

## Notes

* Title tag templating:
    * The title is in format of [ Page | App | Site ], which seems to be the standard that google, stack overflow,
    django, and other major sites currently go by.
    * To be as generic as possible, the "Site" part of the title is set to default to "CAE Center". Where appropriate,
    this should be overridden to be the website name.
    
* User model separation:
    * Currently, the user model is technically split into two parts. It has the "User" which essentially contains fields
    relevant to authentication. Then it has a one-to-one "Profile" which contains all other user model values.
