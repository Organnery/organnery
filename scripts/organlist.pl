#!/usr/bin/perl
# Openbox menu to recursively list directories and files.
#use warnings;
#use strict;
use Cwd 'abs_path';

sub say { print "$_\n" for @_; }
sub item;
sub menu;

########################################## CONFIGURATION #########################################

# base dir without trailing slash
my $dir = "/home/user/stops/";

##################################################################################################

# get folder content
opendir DIR,$dir;
my @dir = readdir(DIR);
close DIR;

# iterate and build menu
say "<openbox_pipe_menu>";

my @sorted_dirs = sort @dir;

my @exclude = ("\.","\.\.","\.cache","lost+found","waves","midi_recordings","audio_recordings");

foreach(@sorted_dirs){
# $dir is the base dir
# $_ is the current item
    if ( $_ ~~ @exclude ) {
        	next;
    };
    # replace the underscore with a double underscore in the label to
    # prevent openbox from interpreting it as a keyboard accelerator
    # $_ =~ s/_/__/g;

    my $organdir = $dir . "/" . $_ ;
    if (( -d $organdir ) and ( -f $organdir . "/" . "definition" )) {
    # it is a folder, with an organ definition...
        menu $_;
    }
}

say "</openbox_pipe_menu>";
exit 0;

########################################### SUBROUTINES ##########################################

# print a menu for directory
sub menu {
  my $label = shift;
  my $id = $label . "_menuid";
#  say "<menu id=\"$label\" label=\"$label\" execute=\"/home/user/organchange.sh $label\" />";
  say "<menu id=\"$id\" label=\"$label\">";
  say "  <item label=\"Switch to this organ now and set as default\">";
  say "    <action name=\"Execute\">";
  say "      <execute>";
  say "        organnery-config organ-switch $label";
  say "      </execute>";
  say "    </action>";
  say "  </item>";
  say "  <item label=\"Set this organ as default for next reboot\">";
  say "    <action name=\"Execute\">";
  say "      <execute>";
  say "        organnery-config organ-set $label";
  say "      </execute>";
  say "    </action>";
  say "  </item>";
  say "</menu>";

# check env $INSTRUMENT_NAME
#--results
# is currently active > item only
#or
# switch to this organ > action : set env $INSTRUMENT and kill aeolus
#and
# set as startup default > action : change in organnery.conf
}


