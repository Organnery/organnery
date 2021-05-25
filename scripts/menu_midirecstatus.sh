#!/bin/bash
if [[ `pgrep -f arecordmidi` ]]; then
	echo "<openbox_pipe_menu>";
	echo "  <item label=\"Currently Recording\">";
	echo "    <action name=\"Execute\">";
	echo "      <execute>";
	echo "      </execute>";
	echo "    </action>";
	echo "  </item>";
	echo "</openbox_pipe_menu>";
    exit 1
else
	echo "<openbox_pipe_menu>";
	echo "  <item label=\"NOT Recording\">";
	echo "    <action name=\"Execute\">";
	echo "      <execute>";
	echo "      </execute>";
	echo "    </action>";
	echo "  </item>";
	echo "</openbox_pipe_menu>";
    exit 0
fi
