# What to remove when cleaning
push @generated_exts, "cb";
push @generated_exts, "lodiagram";
push @generated_exts, "cb2";
push @generated_exts, "spl";
push @generated_exts, "nav";
push @generated_exts, "snm";
push @generated_exts, "nmo";
push @generated_exts, "brf";
push @generated_exts, "nlg";
push @generated_exts, "nlo";
push @generated_exts, "nls";
push @generated_exts, "acn";
push @generated_exts, "acr";
push @generated_exts, "ist";
push @generated_exts, "alg";
push @generated_exts, "fls";
push @generated_exts, "synctex.gz";
push @generated_exts, "tex.latexmain";
push @generated_exts, "run.xml";

# Remove .bbl files after compilation
$bibtex_use = 2;

# Handle glossaries
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');

sub run_makeglossaries {
  if ( $silent ) {
    system "makeglossaries -q '$_[0]'";
  }
  else {
    system "makeglossaries '$_[0]'";
  };
}
