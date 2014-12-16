# LP Vault Manager

**[DOWNLOAD](http://www.bachyaproductions.com/wp-assets/uploads/2014/12/lp-vault-manager.alfredworkflow)**

LP Vault manager is an [Alfred 2](http://www.alfredapp.com/) workflow to interact with a [LastPass](http://www.lastpass.com) vault.

It currently carries the following functionality:

* Searching an individual vault
* Copying a vault item's username
* Copying a vault item's password
* Generating a random password

## Initializing the Workflow

The engine that drives the ability to interact with LastPass remotely is [LastPass' own lastpass-cli command line tool](https://github.com/LastPass/lastpass-cli). Therefore, the first step is to ensure that this is installed on your machine. Helpful hint: [the Homebrew method](https://github.com/LastPass/lastpass-cli#installing-on-os-x) is my recommended method.

By default, laspass-cli requires you to execute the command:

`/usr/local/bin/lpass login <USERNAME>`

...and input the vault's master password. As expected, lastpass-cli requires this to happen after a certain time interval; since this can cause the Alfred workflow to stop working at various points, it is recommended that you prevent the credentials from timing out:

```bash
# The following sets the timeout cancellation for
# the current shell; you can always put this in
# ~/.bashrc, ~/.profile, ~/.zshrc, etc. to make
# it permanent.
export LPASS_AGENT_TIMEOUT=0
```

If that offends a security-conscious mind, no pressure; just keep in mind that you'll have to periodically rerun:

`/usr/local/bin/lpass login <USERNAME>`

...to get it working again (with no warning, mind you – you'll only know because the workflow stops working).

## Searching a Vault

`lpvs <SITE NAME TO SEARCH FOR>`

![Workflow Screenshot](https://github.com/bachya/lp-vault-manager/blob/master/support/readme-images/lpvs-screenshot.png)

* Select an item to copy its password to the system clipboard.
* ⌘-select an item to copy its username to the system clipboard.

### Configuration

Configuration occurs within the Ruby script (found inside the `lpvs` Script Filter):

```ruby
LPASS_PATH = "/usr/local/bin/lpass"
```

Make sure you change `LPASS_PATH` to point to the location of your installed lastpass-cli.

## Password Generation

`lppg <OPTIONAL PASSWORD LENGTH>`

![Workflow Screenshot](https://github.com/bachya/lp-vault-manager/blob/master/support/readme-images/lppg-screenshot.png)

Select an item to copy the generated password to the system clipboard.

### Configuration

Configuration occurs within the Ruby script (found inside the `lppg` Script Filter):

```ruby
LPASS_PATH = "/usr/local/bin/lpass"
```

Make sure you change `LPASS_PATH` to point to the location of your installed lastpass-cli.

Within this same script, you can configure the following options:

* The number of passwords that the `lppg` keyword should generate.
* The default password length (which can be overridden by passing an optional integer argument to the keyword).
* Whether the passwords should use numbers (and which numbers should be considered).
* Whether the symbols should use numbers (and which symbols should be considered).
* Whether ambiguous characters should be avoided.

# Bugs and Feature Requests

To report bugs with or suggest features/changes for LP Vault Manager, please use
the [Issues Page](https://github.com/bachya/lp-vault-manager/issues).

Contributions are welcome and encouraged. To contribute:

* [Fork LP Vault Manager](http://github.com/bachya/lp-vault-manager/fork).
* Create a branch for your contribution (`git checkout -b new-feature`).
* Commit your changes (`git commit -am 'Added this new feature'`).
* Push to the branch (`git push origin new-feature`).
* Create a new [Pull Request](http://github.com/bachya/lp-vault-manager/compare/).

# License

(The MIT License)

Copyright © 2014 Aaron Bach <bachya1208@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the 'Software'), to deal in the
Software without restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

