{ config, lib, options, pkgs, ... }:

{
  options.services.idle-shutdown.enable = lib.mkEnableOption "idle-shutdown";

  config = lib.mkIf config.services.idle-shutdown.enable {
    systemd.services.idle-shutdown = {
      description = "Shut down after being idle for some timeout.";
      wantedBy = [ "default.target" ];
      path = with pkgs; [
        # See the comment in idle-shutdown.py as to why tmux is not currently included.
        # tmux
        utillinux
      ];
      serviceConfig = {
        ExecStart = pkgs.writers.writePython3 "idle-shutdown.py"
          {
            flakeIgnore = [ "E501" ];
          } ./idle-shutdown.py;
        Restart = "always";
        RestartSec = "0";
      };
    };
  };
}
