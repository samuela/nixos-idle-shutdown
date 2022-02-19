# nixos-idle-shutdown

A NixOS service that automatically shuts down the system after a period of inactivity. This is useful in cloud environments where the system should be shut down when no one is currently logged in. Current behavior is to automatically shut down after an hour of inactivity.

Note that nixos-idle-shutdown currently does not respect tmux sessions due to https://github.com/NixOS/nixpkgs/issues/155446.

## Usage

In your `/etc/nixos/configuration.nix`:

```nix
imports = [
  (fetchTarball "https://github.com/samuela/nixos-idle-shutdown/tarball/main")
];
```
