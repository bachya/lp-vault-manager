# LP Vault Manager

**[DOWNLOAD](http://www.bachyaproductions.com/wp-assets/uploads/2014/12/lp-vault-manager.alfredworkflow)**

LP Vault manager is an [Alfred 2](http://www.alfredapp.com/) workflow to interact with a LastPass vault.

![Workflow Screenshot](https://github.com/bachya/lp-vault-manager/blob/master/support/readme-images/screenshot.png)

It currently carries the following functionality:

* Searching an individual vault
* Copying a vault item's username
* Copying a vault item's password
* Generating a random password

## Initializing the Workflow

The engine that drives the ability to interact with LastPass remotely is [LastPass' own lastpass-cli command line tool](https://github.com/LastPass/lastpass-cli). Therefore, the first step is to ensure that this is installed on your machine. Helpful hint: [the Homebrew method](https://github.com/LastPass/lastpass-cli) is my recommended method.

By default, laspass-cli requires you to execute the command:

```bash
/usr/local/bin/lpass login <USERNAME>
```

...and input the vault's master password. As expected, lastpass-cli requires this to happen after a certain time interval; since this can cause the Alfred workflow to stop working at various points, it is recommended that you prevent the credentials from timing out:

```bash
# The following sets the timeout cancellation for
# the current shell; you can always put this in
# ~/.bashrc, ~/.profile, ~/.zshrc, etc. to make
# it permanent.
export LPASS_AGENT_TIMEOUT=0
```

At some point, I'll figure out a way to re-login via the workflow so that security-conscious individuals can be satisfied. :)

## Interacting with a Vault

## Password Generation
