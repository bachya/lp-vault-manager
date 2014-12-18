# LP Vault Manager

**[DOWNLOAD](https://github.com/bachya/lp-vault-manager/releases/download/v1.0/LP.Vault.Manager.alfredworkflow)**

LP Vault manager is an [Alfred 2](http://www.alfredapp.com/) workflow to interact with a [LastPass](http://www.lastpass.com) vault.

With it, you can:

* search an individual vault.
* launch a vault URL in the default browser.
* copy a vault item's username.
* copy vault item's password.
* generate a random password.

## Initializing the Workflow

### Install lastpass-cli

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

### Storing the Path to lastpass-cli

Since Alfred doesn't give an easy ability to store workflow-wide variables, the `LPASS_PATH` environment variable
can be used:

```bash
export LPASS_PATH=/usr/local/bin/lpass
```

If this variable isn't set, LP Vault Manager will attempt to automagically deduce its location. But that takes a microsecond
longer, so if speed is the name of your game, make sure to set the `LPASS_PATH` variable.

## Caching Data

Alfred Script Filters have [a strange quirk](http://goo.gl/JS1BUK) that must be worked around:

1. A Script Filter is executed regularly as the user types.
2. Each time it is run, a new process is spun up and the previous processes continuing running.
3. If the `lpass` command is slow, the Script Filter results will change while the workflow is running.

This leads to a less-than-ideal user experience. Therefore, I made a hard decision: in order to speed
up the process, I cache your vault data to your local filesystem. It should be perfectly safe there, but
as I cannot fully verify the veracity of that statement, you should be aware.

The first time data is requested from LastPass, the data is cached automatically. You always have the option
to force download it:

`lpdd`

![lpdd Screenshot](https://github.com/bachya/lp-vault-manager/blob/master/support/readme-images/lpdd-screenshot.png)

## Searching a Vault

`lpvs <QUERY>`

![lpvs Screenshot](https://github.com/bachya/lp-vault-manager/blob/master/support/readme-images/lpvs-screenshot.png)

The query is run against vault item names and URLs. When results appear, there are several actions you can take on them:

* Select an item to launch its URL in the default browser.
* ⌘-Click an item to copy its password to the system clipboard.
* Shift-Click an item to copy its username to the system clipboard.

## Password Generation

`lppg <OPTIONAL PASSWORD LENGTH>`

![lppg Screenshot](https://github.com/bachya/lp-vault-manager/blob/master/support/readme-images/lppg-screenshot.png)

Select an item to copy the generated password to the system clipboard.

### Configuration

Configuration occurs within the Ruby script (`lpvm.rb`, found inside the workflow folder):

```ruby
### CONSTANTS ###
NUM_PASSWORDS = 10         # The number of passwords to generate
DEFAULT_PASSWORD_LEN = 20  # The default length (if no arg is specified)
USE_NUMBERS = true         # Whether the password should include numbers
USE_SYMBOLS = true         # Whether the passwork should include symbols
AVOID_AMBIGUOUS = true     # Whether ambiguous chars should be ignored
```

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

