%define _build_id_links none

%global __provides_exclude ^((libffmpeg[.]so.*)|(lib.*\\.so.*))$
%global __requires_exclude ^((libffmpeg[.]so.*)|(lib.*\\.so.*)|(ld-linux-aarch64.so.*))$

Name:       heroic-games-launcher-bin
Version:    2.17.2
Release:    1%{?dist}
Summary:    A Native GOG, Amazon and Epic Games Launcher for Linux
ExclusiveArch: x86_64

License:    GPL-3.0-or-later
URL:        https://heroicgameslauncher.com
Source0:    https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/releases/download/v%{version}/Heroic-%{version}-linux-x86_64.rpm
# License file
Source1:    https://raw.githubusercontent.com/Heroic-Games-Launcher/HeroicGamesLauncher/main/COPYING
# Documentation file
Source2:    https://raw.githubusercontent.com/Heroic-Games-Launcher/HeroicGamesLauncher/main/README.md

BuildRequires: desktop-file-utils

Requires:   hicolor-icon-theme
Requires:   python3
## Just tip for future if this will be unbunled one day
# Requires:   legendary

Recommends: gamemode
Recommends: libvkd3d
Recommends: mangohud
Recommends: wine-dxvk
Recommends: wine

%description
Heroic is an Open Source Game Launcher for Linux, Windows and macOS. Right now
it supports launching games from the Epic Games Store using Legendary, GOG
Games using our custom implementation with gogdl and Amazon Games using Nile.

Features available right now

  * Login with an existing Epic Games, GOG or Amazon account
  * Install, uninstall, update, repair and move Games
  * Import an already installed game
  * Play Epic games online [AntiCheat on macOS and on Linux depends on the
    game]
  * Play games using Wine or Proton [Linux]
  * Play games using Crossover [macOS]
  * Download custom Wine and Proton versions [Linux]
  * Access to Epic, GOG and Amazon Games stores directly from Heroic
  * Search for the game on ProtonDB for compatibility information [Linux]
  * Show ProtonDB and Steam Deck compatibility information [Linux]
  * Sync installed games with an existing Epic Games Store installation
  * Sync saves with the cloud
  * Custom Theming Support
  * Download queue
  * Add Games and Applications outside GOG, Epic Games and Amazon Games


%prep
rpm2cpio %{SOURCE0} | cpio -idmv
sed -i 's|/opt/Heroic/heroic|%{_libdir}/%{name}/heroic|' \
    %{_builddir}/usr/share/applications/heroic.desktop


%install
mkdir -p %{buildroot}%{_libdir}/%{name}/
cp -a opt/Heroic/* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/
cp -a usr/share/* %{buildroot}%{_datadir}/

mkdir -p %{buildroot}%{_bindir}/
ln -sf %{_libdir}/%{name}/heroic %{buildroot}%{_bindir}/heroic

install -D -p -m 0644 %{SOURCE1} -t %{buildroot}%{_licensedir}/%{name}/
install -D -p -m 0644 %{SOURCE2} -t %{buildroot}%{_docdir}/%{name}/

strip -s %{buildroot}%{_libdir}/%{name}/*.so
strip -s %{buildroot}%{_libdir}/%{name}/{heroic,chrome-sandbox}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%{_bindir}/heroic
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_docdir}/%{name}/
%{_libdir}/%{name}/
%{_licensedir}/%{name}/
%attr(4755,root,root) %{_libdir}/%{name}/chrome-sandbox
