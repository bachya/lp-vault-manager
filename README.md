# LastPass Vault Manager

**[DOWNLOAD](https://github.com/bachya/lp-vault-manager/releases/download/v3.1/LastPass.Vault.Manager.alfredworkflow)**

LP Vault manager is an [Alfred 2](http://www.alfredapp.com/) workflow to interact with a [LastPass](http://www.lastpass.com) vault.

![LastPass Vault Manager in action](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/lpvm.gif)

With it, you can:

* search a vault by query
* search a vault by your browser's front-most tab
* launch a vault URL in the default browser
* copy a vault item's username
* copy vault item's password
* generate random passwords
* manage many different configuration options
* much more!

# Initializing the Workflow

## Installing lastpass-cli

The engine that drives the ability to interact with LastPass remotely is [LastPass' own lastpass-cli command line tool](https://github.com/LastPass/lastpass-cli). Therefore, the first step is to ensure that this is installed on your machine. Helpful hint: [the Homebrew method](https://github.com/LastPass/lastpass-cli#installing-on-os-x) is my recommended method. *Make sure the version you install has the ability to run `lpass export` – not all versions do!*

## Logging In To LastPass

Use `lpsettings` command and select "Modify LastPass Settings >> Log In To LastPass" to log into LastPass.

![Logging In To LastPass](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/lp-login-screenshot.png)

## Preventing Future Master Login Requests

The `lpsettings` command executes the following behind the scenes:

`/usr/local/bin/lpass login <USERNAME>`

Once executed, you will be asked to input the vault's master password. As expected, lastpass-cli requires this to happen after a certain time interval; since this can cause the Alfred workflow to stop working at various points, it is recommended that you prevent the credentials from timing out:

```bash
# The following sets the timeout cancellation for
# the current shell; you can always put this in
# ~/.bashrc, ~/.profile, ~/.zshrc, etc. to make
# it permanent.
export LPASS_AGENT_TIMEOUT=0
```

If that offends a security-conscious mind, don't feel pressure to disable the timeout. The workflow is smart enough to notify you if you need to log in again:

![Please re-login](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/relogin-screenshot.png)

# Commands

## Searching a Vault (based on query)

**Command:** `lpvs <QUERY>`

![`lpvs` Screenshot](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/lpvs-screenshot.png)

**Description:** Searches the associated LastPass vault (more specifically, searches the URL and Hostname fields of all vault items) for the provided query.

**Default Action:** Open URL in default browser

**Modifiers:**

* ⌘-Click an item to copy its password to the system clipboard.
* Shift-Click an item to copy its username to the system clipboard.

## Searching a Vault (based on current URL)

**Command:** `lpbrowser`

![`lpbrowser` Screenshot](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/lpbrowser-screenshot.png)

**Description:** Searches the associated LastPass vault (more specifically, searches the URL of all vault items) for the URL of the front-most tab in the user's default browser (set by the `lpsetbrowser` command).

**Default Action:** Open URL in default browser

**Modifiers:**

* ⌘-Click an item to copy its password to the system clipboard.
* Shift-Click an item to copy its username to the system clipboard.

## Generating Random Passwords

**Command:** `lppg`

![`lppg` Screenshot](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/lppg-screenshot.png)

**Description:** Generates a number of random passwords.

**Default Action:** Copy the password to the system clipboard.

## Re-Caching Data

**Command:** `lpdd`

![`lpdd` Screenshot](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/lpdd-screenshot.png)

**Description:** Destroys the cached LastPass metadata and re-downloads it.

**Default Action:** N/A

**Relevant Configuration Options:** N/A

## Setting Configuration Options

**Command:** `lpsettings`

![`lpsettings` Screenshot](https://raw.githubusercontent.com/bachya/lp-vault-manager/master/support/readme-images/lpsettings-screenshot.png)

**Description:** A nice, guided approach to managing the various settings that LastPass Vault Manager exposes.

**Settings:**

* Set Default Browser (for use in `lpbrowser`)
* Modify LastPass Settings
    * Log in to LastPass
    * Log out from LastPass
    * Set LastPass Username
    * Set Cache Timeout
    * Set `lpass` Filepath
* Modify Password Settings
    * Set number of passwords
    * Set password length
* Edit Config File (in case you want to do it the power-user way)
* View Repository

# Q&A and Common Issues

## Q: You mention data caching in several places. What exactly is cached? I'm concerned that my LastPass data is being stored insecurely.
A: I take security considerations very seriously. At the same time, I want this workflow to provide a speedy user experience. With that said, here's how caching works:

1. LastPass Vault Manager caches data from the results of `lpass export`.
2. ***Of the data that `lpass export` returns, only the URL and Hostname fields are stored in the local cache. All other data is thrown away immediately.***
3. LastPass Vault Manager searches across the URL and Hostname fields, either via query (if using `lpvs`) or the URL of the default browser's front-most tab (if using `lpbrowser`).
4. LastPass Vault Manager uses `lpass show <HOSTNAME>` to grab other fields for use in the workflow. ***None of these additional fields are ever stored to disk.***

Again, I am committed to being secure with your data. If you have further concerns, please reach out to me via the [Issues Page](https://github.com/bachya/lp-vault-manager/issues).

## Q: I'm noticing something strange: when I type a query into `lpvs`, it seems as though other results appear for a split second before the correct ones do. Sometimes, the "loading" result appears more than once. What's going on?

Check out [this discussion on the Alfred forum](http://www.alfredforum.com/topic/991-anyway-to-delay-script-filter-from-running-ie-wait-until-user-has-stopped-typing-or-at-least-paused/). Long story short, Alfred processes every key press when running a Script Filter *and doesn't kill previous iterations of that script*. Sounds like it'll be addressed in Alfred 2.6.

## Q: How come Firefox/Opera/etc. isn't an option when I try to set my default browser (for `lpbrowser`)?
A: Since I use Applescript for the application-level scripting necessary to grab the URL from the browser's tab, I need a browser that has Applescript support for that activity. Unfortunately, many browsers – including Firefox – don't support it. See [this Alfred forum topic](http://www.alfredforum.com/topic/2013-how-to-get-frontmost-tab%E2%80%99s-url-and-title-of-various-browsers/) for more info.

If there is a particular browser that I don't yet support, but does have the requisite Applescript capabilities, let me know via the [Issues Page](https://github.com/bachya/lp-vault-manager/issues).

## Q. I'm getting a `ValueError: No JSON object could be decoded` error when I run the workflow. What's going on?
A. Check out [issue #5](https://github.com/bachya/lp-vault-manager/issues/5) – long story short, you're probably saving raw Unicode characters in your config file.

## Q: Didn't this project used to be Ruby-based? Why does it now use Python?
A: During initial development, I found myself tackling a number of fairly common challenges: data caching, fuzzy searching, configuration management, and more. As I looked at other Alfred workflows, I noticed that several developers had started to write libraries to work with Alfred in their preferred language. I decided to do the same.

After some tinkering, I ran across [Alfred-Workflow](https://github.com/deanishe/alfred-workflow), a Python library designed to manage all of my challenges and more. It was too beautiful not to try; plus, it gives me the opportunity to get better at Python.

# Bugs and Feature Requests

To report bugs with or suggest features/changes for LP Vault Manager, please use
the [Issues Page](https://github.com/bachya/lp-vault-manager/issues).

Contributions are welcome and encouraged. To contribute:

* [Fork LP Vault Manager](http://github.com/bachya/lp-vault-manager/fork).
* Create a branch for your contribution (`git checkout -b new-feature`).
* Commit your changes (`git commit -am 'Added this new feature'`).
* Push to the branch (`git push origin new-feature`).
* Create a new [Pull Request](http://github.com/bachya/lp-vault-manager/compare/).

# Credits and Thanks

* [LastPass](https://lastpass.com/) for their great product and for allowing me to use their iconography.
* [Dean Jackson](https://github.com/deanishe) for his excellent [Alfred-Workflow](https://github.com/deanishe/alfred-workflow) Python library.
* [IcoMoon](https://icomoon.io/), [flaticon](http://www.flaticon.com/search/password), and [Simple Icon](http://simpleicon.com/) for the lovely icons.

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

