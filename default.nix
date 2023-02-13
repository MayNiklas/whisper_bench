{ pkgs
, lib
, cudaSupport ? false
}:
let
  # makes it easer to overwrite the python version from the outside
  python = pkgs.python3Packages;

  # # The Python interpreters are by default not built with optimizations enabled,
  # # because the builds are in that case not reproducible.
  # # The following lines are completely optional and only enable optimizations!
  # # Will lead to way longer build times, but will make the resulting Python interpreter faster.
  # # Simply comment out the following lines if you don't want to enable optimizations.
  # python3Optimized = pkgs.python3.override {
  #   enableOptimizations = true;
  #   reproducibleBuild = false;
  #   self = python3Optimized;
  # };
  # python = python3Optimized.pkgs;
in
python.buildPythonPackage rec {

  pname = "whisper_bench";
  version = "1.0.0";

  src = ./.;

  propagatedBuildInputs = with python; [
    openai-whisper
    psutil
    torch
  ];

}
