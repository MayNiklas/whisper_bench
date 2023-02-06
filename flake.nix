{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      rec {
        # Use nixpkgs-fmt for `nix fmt'
        formatter = pkgs.nixpkgs-fmt;
        defaultPackage = packages.whisper_bench;

        packages = flake-utils.lib.flattenTree rec {

          whisper_bench = pkgs.callPackage ./default.nix {
            cudaSupport = pkgs.config.cudaSupport or false;
          };

          whisper_bench_withCUDA =
            let
              # needed for CUDA support
              pkgs = import nixpkgs {
                inherit system;
                config = {
                  allowUnfree = true;
                  cudaSupport = true;
                };
              };
            in
            pkgs.callPackage ./default.nix
              {
                cudaSupport = true;
              };

        };
      });
}
