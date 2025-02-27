{pkgs}: {
  deps = [
    pkgs.freetype
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.glibcLocales
  ];
}
