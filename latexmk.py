import os,sys

latexmk_name = "latexmk"

def year_twentytwenty():
    global latexmk_name
    with open(latexmk_name, "w+") as writer:
        writer.write("""
# Settings
$xdvipdfmx = "xdvipdfmx -z 6 -o %D %O %S";

# Workaround to allow pstricks transparency (https://github.com/overleaf/issues/issues/3449)
$dvipdf = "dvipdf -dNOSAFER -dALLOWPSTRANSPARENCY %O %S %D";

###############################
# Post processing of pdf file #
###############################

# assume the jobname is 'output' for sharelatex
my $ORIG_PDF_AGE = -M "output.pdf"; # get age of existing pdf if present

END {
    # Do nothing if pdf file doesn't exist or wasn't updated
    my $NEW_PDF_AGE = -M "output.pdf";
    return if !defined($NEW_PDF_AGE);
    return if defined($ORIG_PDF_AGE) && $NEW_PDF_AGE == $ORIG_PDF_AGE;

    # Figure out where qpdf is
    $qpdf //= "/usr/bin/qpdf";
    $qpdf = $ENV{QPDF} if defined($ENV{QPDF}) && -x $ENV{QPDF};
    return if ! -x $qpdf;
    $qpdf_opts //= "--linearize --newline-before-endstream";
    $qpdf_opts = $ENV{QPDF_OPTS} if defined($ENV{QPDF_OPTS});

    # Run qpdf
    my $qpdf_exit_code;
    {
        # Restore the original exit code from latexmk at the end of this block
        local $?;
        system($qpdf, split(' ', $qpdf_opts), "output.pdf", "output.pdf.opt");
        $qpdf_exit_code = ($? >> 8);
        print "qpdf exit code=$qpdf_exit_code\n";
    }

    # Replace the output file if qpdf was successful
    # qpdf returns 0 for success, 3 for warnings (output pdf still created)
    return if !($qpdf_exit_code == 0 || $qpdf_exit_code == 3);
    print "Renaming optimised file to output.pdf\n";
    rename("output.pdf.opt", "output.pdf");

    {
        # Restore the original exit code from latexmk at the end of this block
        local $?;
        print "Extracting xref table for output.pdf\n";
        system("$qpdf --show-xref output.pdf > output.pdfxref");
        $qpdf_xref_exit_code = ($? >> 8);
        print "qpdf --show-xref exit code=$qpdf_xref_exit_code\n";
    }
}
##############
# Glossaries #
##############
add_cus_dep( 'glo', 'gls', 0, 'glo2gls' );
add_cus_dep( 'acn', 'acr', 0, 'glo2gls'); # from Overleaf v1
sub glo2gls {
    system("makeglossaries $_[0]");
}

#############
# makeindex #
#############
@ist = glob("*.ist");
if (scalar(@ist) > 0) {
    $makeindex = "makeindex -s $ist[0] %O -o %D %S";
}

################
# nomenclature #
################
add_cus_dep("nlo", "nls", 0, "nlo2nls");
sub nlo2nls {
    system("makeindex $_[0].nlo -s nomencl.ist -o $_[0].nls -t $_[0].nlg");
}

#########
# Knitr #
#########
my $root_file = $ARGV[-1];

add_cus_dep( 'Rtex', 'tex', 0, 'rtex_to_tex');
add_cus_dep( 'Rnw', 'tex', 0, 'rnw_to_tex');
sub rtex_to_tex {
    do_knitr("$_[0].Rtex");
}

sub rnw_to_tex {
    do_knitr("$_[0].Rnw");
}

sub do_knitr {
    my $dirname = dirname $_[0];
    my $basename = basename $_[0];
    system("Rscript -e \"library('knitr'); setwd('$dirname'); knit('$basename')\"");
}

my $rtex_file = $root_file = ̃ s/\.tex$/.Rtex/r;
my $rnw_file = $root_file = ̃ s/\.tex$/.Rnw/r;
unless (-e $root_file) {
    if (-e $rtex_file) {
        do_knitr($rtex_file);
    }
    elsif (-e $rnw_file) {
        do_knitr($rnw_file);
    }
}

##########
# feynmf #
##########
push(@file_not_found, 'ˆfeynmf: Files .* and (.*) not found:$');
add_cus_dep("mf", "tfm", 0, "mf_to_tfm");
sub mf_to_tfm { system("mf '\\mode:=laserjet; input $_[0]'"); }

push(@file_not_found, 'ˆfeynmf: Label file (.*) not found:$');
add_cus_dep("mf", "t1", 0, "mf_to_label1");
sub mf_to_label1 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t1"); }
add_cus_dep("mf", "t2", 0, "mf_to_label2");
sub mf_to_label2 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t2"); }
add_cus_dep("mf", "t3", 0, "mf_to_label3");
sub mf_to_label3 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t3"); }
add_cus_dep("mf", "t4", 0, "mf_to_label4");
sub mf_to_label4 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t4"); }
add_cus_dep("mf", "t5", 0, "mf_to_label5");
sub mf_to_label5 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t5"); }
add_cus_dep("mf", "t6", 0, "mf_to_label6");
sub mf_to_label6 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t6"); }
add_cus_dep("mf", "t7", 0, "mf_to_label7");
sub mf_to_label7 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t7"); }
add_cus_dep("mf", "t8", 0, "mf_to_label8");
sub mf_to_label8 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t8"); }
add_cus_dep("mf", "t9", 0, "mf_to_label9");
sub mf_to_label9 { system("mf '\\mode:=laserjet; input $_[0]' && touch $_[0].t9"); }

##########
# feynmp #
##########
push(@file_not_found, 'ˆdvipdf: Could not find figure file (.*); continuing.$');
add_cus_dep("mp", "1", 0, "mp_to_eps");
sub mp_to_eps {
    system("mpost $_[0]");
    return 0;
}

#############
# asymptote #
#############
sub asy {return system("asy \"$_[0]\"");}
add_cus_dep("asy","eps",0,"asy");
add_cus_dep("asy","pdf",0,"asy");
add_cus_dep("asy","tex",0,"asy");

#############
# metapost # # from Overleaf v1
#############
add_cus_dep('mp', '1', 0, 'mpost');
sub mpost {
    my $file = $_[0];
    my ($name, $path) = fileparse($file);
    pushd($path);
    my $return = system "mpost $name";
    popd();
    return $return;
}

##########
# chktex #
##########
unlink 'output.chktex' if -f 'output.chktex';
if (defined $ENV{'CHKTEX_OPTIONS'}) {
    use File::Basename;
    use Cwd;

    # identify the main file
    my $target = $ARGV[-1];
    my $file = basename($target);

    if ($file = ̃ /\.tex$/) {
        # change directory for a limited scope
        my $orig_dir = cwd();
        my $subdir = dirname($target);
        chdir($subdir);
        # run chktex on main file
        $status = system("/usr/local/bin/run-chktex.sh", $orig_dir, $file);
        # go back to original directory
        chdir($orig_dir);

        # in VALIDATE mode we always exit after running chktex
        # otherwise we exit if EXIT_ON_ERROR is set

        if ($ENV{'CHKTEX_EXIT_ON_ERROR'} || $ENV{'CHKTEX_VALIDATE'}) {
            # chktex doesn't let us access the error info via exit status
            # so look through the output
            open(my $fh, "<", "output.chktex");
            my $errors = 0;
            {
                local $/ = "\n";
                while(<$fh>) {
                    if (/ˆ\S+:\d+:\d+: Error:/) {
                        $errors++;
                        print;
                }
                }
            }
            close($fh);
            exit(1) if $errors > 0;
            exit(0) if $ENV{'CHKTEX_VALIDATE'};
        }
    }
}
""")


default_year="2020"
years = {
    "2020":year_twentytwenty,
}

argz = " ".join(sys.argv);written=False
for key,value in years.items():
    if key in argz:
        value()
        written=True
        break
if not written:
    years[default_year]()
