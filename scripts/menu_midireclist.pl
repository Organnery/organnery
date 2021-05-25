#!/usr/bin/perl
#use warnings;
#use strict;
use Cwd 'abs_path';

sub say { print "$_\n" for @_; }
sub item;
sub menu;

########################################## CONFIGURATION #########################################

# base dir without trailing slash
my $dir = "/home/user/stops/midi_recordings";
# TODO FIX we should get the ENV variable for exact folder

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

say "  <menu id=\"All files\"  label=\"--All files\">";
say "    <item label=\"Delete All midi recordings\">";
say "      <action name=\"Execute\">";
say "        <prompt>WARNING : Are you sure you want to delete All midi recordings ?</prompt>"
say "        <execute>";
say "          rm $dir"."/"."*.mid";
say "        </execute>";
say "      </action>";
say "    </item>";
say "    <item label=\"Copy All midi recordings to usb key DATA partition\">";
say "      <action name=\"Execute\">";
say "        <execute>";
say "          cp $dir"."/"."*.mid" $dir"."../../usb/";
say "        </execute>";
say "      </action>";
say "    </item>";
say "  </menu>";

say "</openbox_pipe_menu>";
exit 0;

########################################### SUBROUTINES ##########################################

# print a menu for directory
sub menu {
  my $id = shift;
  my $label = shift;
  my $dir = shift;
  say "<menu id=\"$id\" label=\"$label\" execute=\"\" />";
}
 
# print a menu item
sub item {
  my $file = shift;
  my $dir = shift;

  say "  <menu id=\"$file\"  label=\"$file\">";
  say "    <item label=\"Play now\">";
  say "      <action name=\"Execute\">";
  say "        <execute>";
  say "          /usr/share/organnery/scripts/midiplaystart.sh $dir"."/"."$file";
  say "        </execute>";
  say "      </action>";
  say "    </item>";
  say "    <item label=\"Delete\">";
  say "      <action name=\"Execute\">";
  say "        <prompt>WARNING : Are you sure you want to delete $file ?</prompt>"
  say "        <execute>";
  say "          rm $dir"."/"."$file";
  say "        </execute>";
  say "      </action>";
  say "    </item>";
  say "    <item label=\"Copy to usb DATA partition\">";
  say "      <action name=\"Execute\">";
  say "        <execute>";
  say "          cp $dir"."/"."$file" $dir"."../../usb/"."$file";
  say "        </execute>";
  say "      </action>";
  say "    </item>";
  say "  </menu>";
}
