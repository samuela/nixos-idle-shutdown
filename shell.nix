# This is only used in development.
let
  # Last updated: 2022-02-18. Check for new commits at status.nixos.org.
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/19574af0af3ffaf7c9e359744ed32556f34536bd.tar.gz") { };
in
pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    tmux
    utillinux
    yapf
  ];
}
