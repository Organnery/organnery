#!/bin/bash
if [[ `pgrep -f aplaymidi` ]]; then
	echo "<openbox_pipe_menu>";
	echo "  <item label=\"Currently playing\">";
	echo "    <action name=\"Execute\">";
	echo "      <execute>";
	echo "      </execute>";
	echo "    </action>";
	echo "  </item>";
	echo "</openbox_pipe_menu>";
    exit 1
else
	echo "<openbox_pipe_menu>";
	echo "  <item label=\"NOT playing\">";
	echo "    <action name=\"Execute\">";
	echo "      <execute>";
	echo "      </execute>";
	echo "    </action>";
	echo "  </item>";
	echo "</openbox_pipe_menu>";
    exit 0
fi
