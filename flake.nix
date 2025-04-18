{
  description = "sudosubin/pre-commit-image";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable-small";
  };

  outputs =
    { self, nixpkgs }:
    let
      inherit (nixpkgs.lib) genAttrs platforms;
      forAllSystems = f: genAttrs platforms.unix (system: f (import nixpkgs { inherit system; }));

    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          buildInputs = with pkgs; [
            libheif
            uv
          ];

          shellHook = ''
            # pillow-heif: fix libheif.h not found
            export CFLAGS="$(echo $NIX_CFLAGS_COMPILE | sed -e "s/-isystem /-I/g") -Wno-error=deprecated-ofast"
          '';
        };
      });
    };
}
