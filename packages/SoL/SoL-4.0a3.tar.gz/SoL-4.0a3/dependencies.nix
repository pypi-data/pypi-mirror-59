# -*- coding: utf-8 -*-
# :Project:   SoL -- Derivations for some non packaged dependencies
# :Created:   sab 04 ago 2018 22:57:25 CEST
# :Author:    Alberto Berti <alberto@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2018 Alberto Berti
#

{ pkgs ? import <nixpkgs> {},
  pypkgs ? pkgs.python3Packages }: rec {

  calmjs_parse = pypkgs.buildPythonPackage rec {
    pname = "calmjs.parse";
    version = "1.2.0";
    format = "wheel";
    src = pypkgs.fetchPypi {
      inherit pname version format;
      python = "py3";
      sha256 = "d90dceda51d5c6c4ebb9b9b61e0c04e7da9914d7c2eee0c0bc5d77bdbb870940";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      ply
    ];
  };

  alembic = pypkgs.buildPythonPackage rec {
    pname = "alembic";
    version = "1.2.1";

    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "9f907d7e8b286a1cfb22db9084f9ce4fde7ad7956bb496dc7c952e10ac90e36a";
    };

    buildInputs = with pypkgs; [ pytest pytestcov mock coverage ];
    propagatedBuildInputs = with pypkgs; [
      Mako sqlalchemy13 python-editor
      dateutil setuptools
    ];

    # no traditional test suite
    doCheck = false;

    meta = with pkgs.lib; {
      homepage = https://bitbucket.org/zzzeek/alembic;
      description = "A database migration tool for SQLAlchemy";
      license = licenses.mit;
    };
  };

  mp_extjs_desktop =
    let
      extjs = pkgs.fetchzip {
        url = "http://cdn.sencha.com/ext/gpl/ext-4.2.1-gpl.zip";
        sha256 = "0lp9yrl4ply0xkfi0dx1vy381aj3l758vmfx2vpmfa90d7h7vgbd";
      };
    in
      pypkgs.buildPythonPackage rec {
        inherit extjs;
        pname = "metapensiero.extjs.desktop";
        version = "1.40";
        src = pypkgs.fetchPypi {
          inherit pname version;
          sha256 = "60924079f684dd8449b2c5059d3b6f9e2d6620459ff606bdb349d2af6fd963ee";
        };
        doCheck = false;
        buildInputs = with pypkgs; [
          setuptools
        ];
        patches = [
          ./nixos/fix_desktop_compressor_cmd.patch
        ];
        preBuild = ''
          mkdir -p src/metapensiero/extjs/desktop/assets/extjs
          cp -a $extjs/resources $extjs/src $extjs/ext-dev.js src/metapensiero/extjs/desktop/assets/extjs
          substituteInPlace MANIFEST.in --replace "prune src/metapensiero/extjs/desktop/assets/extjs" "recursive-include src/metapensiero/extjs/desktop/assets/extjs *.gif *.png *.jpg *.js *.css"
          substituteAllInPlace src/metapensiero/extjs/desktop/scripts/minifier.py
        '';
        propagatedBuildInputs = [
          pkgs.yuicompressor
          pypkgs.ply
        ];
        yuicompressorBin = pkgs.yuicompressor + "/bin/yuicompressor";
      };

  mp_sa_dbloady = pypkgs.buildPythonPackage rec {
    pname = "metapensiero.sqlalchemy.dbloady";
    version = "2.9";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "d1737c56bd66b77b49b07d99b548d5be6ac69b11d699e87c9e514c6616a20e8e";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy13 progressbar2 ruamel_yaml
    ];
  };

  mp_sa_proxy = pypkgs.buildPythonPackage rec {
    pname = "metapensiero.sqlalchemy.proxy";
    version = "5.12";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "18e9f21f3da585c1704e32dd4d56c8a3dfad417d85eb7c99bcea904c3242d0d2";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy13
    ];
  };

  pycountry = pypkgs.buildPythonPackage rec {
    pname = "pycountry";
    version = "19.8.18";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "3c57aa40adcf293d59bebaffbe60d8c39976fba78d846a018dc0c2ec9c6cb3cb";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
    ];
  };

  pygal = let
    cairocffi = pypkgs.cairocffi.overridePythonAttrs (old: {
      doCheck = false;
      buildInputs = [ pypkgs.pytestrunner ];
    });
    cairosvg = pypkgs.cairosvg.overridePythonAttrs (old: {
      doCheck = false;
      buildInputs = [ pypkgs.pytestrunner ];
       propagatedBuildInputs = [ cairocffi ] ++
        (with pypkgs; [ cssselect2 defusedxml pillow tinycss2 ]);
    });
    in pypkgs.pygal.overridePythonAttrs (old: {
      patches = [ ./nixos/py3.7fixes.patch ];
      doCheck = false;
     propagatedBuildInputs = [ cairosvg ] ++
        (with pypkgs; [ tinycss cssselect lxml ]);
    });

  pygal_maps_world = pypkgs.buildPythonPackage rec {
    pname = "pygal_maps_world";
    version = "1.0.2";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "8987fcf7f067b56f40f2f83b4f87baf9456164bbff0995715377020fc533db0f";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pygal
    ];
  };

  python_rapidjson = pypkgs.buildPythonPackage rec {
    pname = "python_rapidjson";
    version = "0.8.0";
    src = pypkgs.fetchPypi {
      inherit version;
      pname = "python-rapidjson";
      sha256 = "9753c657d65550d9ad634cf11743e7e68d295b9290a997ee08a9538d57f1cf8d";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      pkgs.rapidjson
    ];
  };

  pyramid_tm = pypkgs.buildPythonPackage rec {
    pname = "pyramid_tm";
    version = "2.2.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "fde97db9d92039a154ca6afffdd2485874c7d3e7a6432adb51b7a60810bad422";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pyramid transaction
    ];
  };

  pyramid_mailer = pypkgs.buildPythonPackage rec {
    pname = "pyramid_mailer";
    version = "0.15.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "ec0aff54d9179b2aa2922ff82c2016a4dc8d1da5dc3408d6594f0e2096446f9b";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      pyramid transaction repoze_sendmail
    ];
  };

  repoze_sendmail = pypkgs.buildPythonPackage rec {
    pname = "repoze.sendmail";
    version = "4.4.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "096ln02jr2afk7ab9j2czxqv2ryqq7m86ah572nqplx52iws73ks";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      transaction zope_interface
    ];
  };

  # This is disabled as of 19.09 because of compilation issues brought
  # in by the dependency of sphinx on SQLAlchemy (and the dependency
  # of pyramid on sphinx). This has to be re-evaluated for 20.03.
  #
  # See also:
  # - https://github.com/NixOS/nixpkgs/issues/76593
  # - https://github.com/NixOS/nixpkgs/issues/76602
  #
  # sqlalchemy13 = pypkgs.buildPythonPackage rec {
  #   pname = "SQLAlchemy";
  #   version = "1.3.8";
  #   src = pypkgs.fetchPypi {
  #     inherit pname version;
  #     sha256 = "2f8ff566a4d3a92246d367f2e9cd6ed3edeef670dcd6dda6dfdc9efed88bcd80";
  #   };
  #   doCheck = false;
  # };

  sqlalchemy13 = pypkgs.sqlalchemy;

  zope_sqlalchemy = pypkgs.buildPythonPackage rec {
    pname = "zope.sqlalchemy";
    version = "1.1";
    src = pypkgs.fetchPypi {
      inherit pname version;
      sha256 = "81554c5b03fbf924c4144ef835b7900271fbd85cfe81cb6bd95e3ab7aa85189f";
    };
    doCheck = false;
    buildInputs = with pypkgs; [
      setuptools
    ];
    propagatedBuildInputs = with pypkgs; [
      sqlalchemy13
      transaction
      zope_interface
    ];
  };

  system_deps = with pypkgs; [
    Babel
    itsdangerous
    pillow
    pynacl
    pyramid
    pyramid_mako
    reportlab
    ruamel_yaml
    setuptools
    transaction
    waitress
    XlsxWriter
 ];
  local_deps = [
    alembic
    calmjs_parse
    mp_extjs_desktop
    mp_sa_proxy
    pycountry
    pygal_maps_world
    pyramid_mailer
    pyramid_tm
    python_rapidjson
    sqlalchemy13
    zope_sqlalchemy
  ];
  test_deps = [
    mp_sa_dbloady
    pypkgs.pytest
    pypkgs.pytestcov
    pypkgs.webtest
  ];
  all_deps = local_deps ++ system_deps ++ test_deps;
}
