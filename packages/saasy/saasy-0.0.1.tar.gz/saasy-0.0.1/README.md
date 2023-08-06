[pixelpassion]: https://www.pixelpassion.io/
[saasy]: https://saasy.pixelpassion.io/
[doc]: https://saasy.pixelpassion.io/docs
[api_doc]: https://saasy.pixelpassion.io/api/docs


[![pixelpassion.io](https://img.shields.io/badge/made%20by-pixelpassion.io-blue.svg)](https://www.pixelpassion.io/)

# `🦑 SaaSy`

## Overview

Welcome to [SaaSy][saasy], the ultimative [Pixelpassion][pixelpassion] API wrapper tool! 
For more informations read the official [Documentation][doc].

## Table of contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Emails](#emails)
  - [Get started](#get-started)
  - [Send your first email](#send-your-first-email)
  - [POST](#post-request)
    - [Create & send a mail](#create-and-send)
    - [Using drafts](#using-drafts)
    - [Errors](#errors)
  - [GET](#get-request)
    - [Retrieve all emails](#retrieve-all-emails)
    - [Use filters](#use-filters)

# Installation

Use the below code to install the wrapper:

``` bash
(sudo) pip install saasy
```

## Authentication

The tool uses your API key and Secret key for authentication.

```bash
export SASSY_API_KEY_='your api key'
```

Initialize the client:

```python
import os
from client import Client

API_KEY = os.environ['SAASY_API_KEY']

saasy = Client(auth_token=API_KEY, debug=True)

```

## Emails

### Get started

Go to SaaSy to setup the following items:

- Your default FROM Address
- Setup a Template, you want to use
- Choose an email provider you want to use

### Create & send your first email

```python
mail = saasy.create_mail({
    "to_address": "john.doe@gmail.com",
    "context": {
        "SIGN_UP_VERIFICATION_URL": "https://www.google.de"
    },
    "job": "email-verification"
})

saasy.send_mail(mail["id"])

```

It will automatically use your defined from-address.

### POST Request

#### Create and send

#### Using drafts

#### Errors

### GET request

#### Retrieve all emails

#### Use filters


