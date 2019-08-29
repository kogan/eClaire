# eClaire Trello printer

eClaire prints Trello cards from a label printer automatically! It's simple and easy, all you need to do as a Trello user is add a "PRINTME" label to your Trello card. 

Having a physical wall and a Trello board is not without it's own pain - we had to keep the two in sync and for months we were typing a card in trello and writing a physical card for the wall and this overhead was not sitting well with us as a fast paced, efficient team.

As a result, eClaire was born on the Kogan.com hackday (May 22nd 2015). 

Now we're making it available for all you Trello lovers out there!

![eClaire Trello Card](https://static1.squarespace.com/static/5664c2f3e4b0957c43aa14f4/t/567b6054c647adf832e5714a/1450926177303/?format=750w)

## Features

- Our very own Claire handwriting font. You can create your own using [myscriptfont.com](http://www.myscriptfont.com/) and/or [FontForge](https://fontforge.github.io/), or use some other ttf font.

## Usage

Just add the `PRINTME` label to your card!

![PRINTME](https://cloud.githubusercontent.com/assets/849426/11989332/21f848f8-aa4f-11e5-85c1-8888db6c20f2.png)

And then wait for the magic to happen

![Notification](https://cloud.githubusercontent.com/assets/849426/11989347/6de5b264-aa4f-11e5-88b4-e7dbbaf2c400.png)

## Installation
Below is the configuration we use in production.

|Type   |Name              |
|-------|------------------|
|OS     |Linux Ubuntu 14.04|
|Printer|Brother QL-570    |
|Labels |DK-22205          |
|Cards  |A6 (105mm X 148mm)|

### Configuring your printer

1. Download and install drivers for your OS at [QL-570 label printer driver](http://support.brother.com/g/b/downloadtop.aspx?c=au&lang=en&prod=lpql570eas):
   - Driver
   - CUPS wrapper (if you are on a Linux)
2. Switch on your printer
3. Verify that your printer appears on [http://localhost:631/](http://localhost:631/) (CUPS admin page):
   - Note down your printer name under `Printers > Queue Name`, e.g. `QL-570`
4. Set up the correct label size by running:

   `sudo brpapertoollpr_ql570 -P QL-570 -n trello -w 62 -h 140`
5. Set other printer options in the printer configuration
   - Page Setup > Orientation: Landscape
   - Finishing > Auto Cut: Cut the medium at the end of the job
   - Advanced > Roll Fed Media: Continuous roll

### Set up Trello labels

eClaire uses labels to find cards to print, so please create the labels `PRINTME` and `PRINTED` to
all of your boards for eClaire to use.

### Set Up eClaire
1. (optional) Create a [virtual env](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and activate it
2. `pip install eclaire`
3. Start creating an `eclaire.yml` from the example below
  - [Setup trello API credentials](#trello-credentials)
  - (optional) [Setup Hipchat notifications](#optional-hipchat-notifications)
  - To find the `id` of your boards, you can use `--list-boards`.
    - eg `eclaire --config eclaire.yml --list-boards`

```yaml
credentials:
  public_key: XXXX
  member_token: XXXXXXXXXXXXXXXXXXXXXXXXX

boards:
  Board1:
    id: 123abc123abc123abc123abc
    printer: QL-570

  Board2:
    id: 123abc123abc123abc123ab2
    printer: QL-570
    notify: false
```

### Trello credentials

1. Go to [https://trello.com/app-key](https://trello.com/app-key) and copy the "Key".
2. Create the `member_token` using the `/connect/` endpoint in your browser
   - `https://trello.com/1/connect?key=...&name=TrelloPrinter&response_type=token&scope=read,write&expiration=never`
   - Replace the `...` with your Key from before.
3. Copy the key and member token into your `eclaire.yml` file.

### (OPTIONAL) Hipchat notifications

If you wish to enable hipchat notifications from eClaire, then add this to your `eclaire.yml` file:

```yaml
hipchat:
  api_key: XXXXXXXXXXXXXXXXXXXXXXXXX
  user: eClaire
  room: Team Room
```

Generate a HipChat API token from your [hipchat account admin](https://www.hipchat.com/admin/api)


## Known issues

- Cards with long titles will be truncated (but this encourages you to be brief).
- Card titles are capitalized which might result in lost meaning for CamelCased words.
- The font provided does not have glyphs for all characters, but should handle most cases for the English alphabet.

## Contributing

We use `pre-commit <https://pre-commit.com/>` to enforce our code style rules
locally before you commit them into git. Once you install the pre-commit library
(locally via pip is fine), just install the hooks::

    pre-commit install -f --install-hooks

The same checks are executed on the build server, so skipping the local linting
(with `git commit --no-verify`) will only result in a failed test build.

Current style checking tools:

- flake8: python linting
- isort: python import sorting
- black: python code formatting

Note:

    You must have python3.6 available on your path, as it is required for some
    of the hooks.

## License

Copyright 2015 KOGAN.COM PTY LTD

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
