with import <nixpkgs> {};
with python35.pkgs;

let 
  djangosemanticuiform = buildPythonPackage rec {
    pname = "django-semanticui-form";
    version = "0.0.1";

    src = fetchPypi {
      inherit pname version;
      sha256 = "0fpbz977md2zmpdbcn2380acnbnyl77r4w07v25f9pzs9bzda21a";
    };

    propagatedBuildInputs = [ django ];

    doCheck = false;
  };  

  djangomathfilters = buildPythonPackage rec {
    pname = "django-mathfilters";
    version = "0.4.0";

    src = fetchPypi {
      inherit pname version;
      sha256 = "1s63mj97n3sxfwqjfl5488zisllsa0xsjri0zhjl3m9dm49y2w75";
    };

    propagatedBuildInputs = [ django ];

    doCheck = false;
  };  

  djangouseraccounts = buildPythonPackage rec {
    pname = "django-user-accounts";
    version = "2.0.0";

    src = fetchPypi {
      inherit pname version;
      sha256 = "09chn2gwyi1cmvacsn3d29mppq15lvjb7xifm6byc3n09kjmh9al";
    };

    propagatedBuildInputs = [ django django_appconf ];

    doCheck = false;
  };  

  partuniverse = buildPythonPackage rec {
    pname = "partuniverse";
    version = "git";

    src = "./";

    meta = {
      homepage = "https://github.com/frlan/partuniverse";
      description = "keep track of replacement parts and other fixtures.";
    };
};
in
(python35.withPackages (ps: with ps; [ django 
                                       djangorestframework
                                       djangomathfilters
                                       djangosemanticuiform
                                       djangouseraccounts
                                       pillow ])).env