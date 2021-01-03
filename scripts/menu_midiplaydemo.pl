#!/usr/bin/perl
#use warnings;
#use strict;
use Cwd 'abs_path';

sub say { print "$_\n" for @_; }
sub item;
sub menu;

########################################## CONFIGURATION #########################################

# base dir without trailing slash
my $dir = "/usr/share/organnery/data/midi";

##################################################################################################

# get folder content
opendir DIR,$dir;
my @dir = readdir(DIR);
close DIR;

# iterate and build menu
say "<openbox_pipe_menu>";

my @sorted_dirs = sort @dir;

foreach(@sorted_dirs){
# $dir is the base dir
# $_ is the current item
    if (($_ eq "\.") or ($_ eq "\.\.")) {
        next;
    };
    # replace the underscore with a double underscore in the label to
    # prevent openbox from interpreting it as a keyboard accelerator
    # $_ =~ s/_/__/g;

    if (-f $dir . "/" . $_ ){
    # it is a file
        item $_, $dir;
    }

    elsif(-d $dir . "/" . $_){
    # it is a folder
        menu $dir, $_, $dir;
    }

    else{
        print $_,"   : UNKNOWN\n";
    }
}

say "</openbox_pipe_menu>";
exit 0;

########################################### SUBROUTINES ##########################################

# print a menu for directory
sub menu {
  my $id = shift;
  my $label = shift;
  my $dir = shift;
  say "<menu id=\"$id\" label=\"$label\" execute=\"cdh $dir\" />";
}
 
# print a menu item
sub item {
  my $file = shift;
  my $dir = shift;
  say "  <item label=\"$file\">";
  say "    <action name=\"Execute\">";
  say "      <execute>";
  say "        /home/user/midiplaystart.sh $dir"."/"."$file";
  say "      </execute>";
  say "    </action>";
  say "  </item>";
}


