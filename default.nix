{ pkgs
, lib
, cudaSupport ? false
}:
let
  # makes it easer to overwrite the python version from the outside
  python = pkgs.python3Packages;
in
python.buildPythonPackage rec {

  pname = "whisper_bench";
  version = "1.0.0";

  src = ./.;

  propagatedBuildInputs = with python; [
    openai-whisper
    torch
  ];

}
