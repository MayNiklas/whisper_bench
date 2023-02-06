{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs
          {
            inherit system;
            # needed for CUDA support
            config = {
              # allowUnfree = true;
              # cudaSupport = true;
            };
          };
      in
      rec {
        # Use nixpkgs-fmt for `nix fmt'
        formatter = pkgs.nixpkgs-fmt;
        defaultPackage = packages.whisper_bench;

        packages = flake-utils.lib.flattenTree rec {

          whisper_bench = with pkgs.python310Packages;
            buildPythonPackage rec {
              pname = "whisper_bench";
              version = "1.0.0";
              src = self;
              propagatedBuildInputs = [
                openai-whisper
                torch
              ];
              doCheck = false;
            };

        };
      });
}
