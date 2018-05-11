# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os
import datetime
import subprocess
import flask

class Robo_screenshotPlugin(octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin,
                            octoprint.plugin.BlueprintPlugin
                            ):
    
    def __init__(self, *args, **kwargs):
        super(Robo_screenshotPlugin, self).__init__(*args, **kwargs)

        #get raspi2png path
        self.root_dir = os.path.dirname(os.path.realpath(__file__))
        self.raspi2png_path = os.path.normpath(self.root_dir + "/bin/raspi2png")
        self.USB = "/home/pi/.octoprint/uploads/USB/"

    @octoprint.plugin.BlueprintPlugin.route("/take_screenshot", methods=['GET'])
    def take_screenshot(self):
        # setup USB
        if not self.setup_USB():
            return flask.make_response("Error. USB is not attached correctly", 500)

        # Create name
        date = datetime.datetime.now().strftime('%b-%d-%G-%I-%M-%S.%f-%p')
        filename = "/%s.png" % date

        dest = os.path.normpath(self.USB_path + filename)

        # Take Screenshot
        command = [self.raspi2png_path, "-p", "\"%s\"" % dest]

        retvals = self.call_subprocess_all_output(command)

        if retvals['p_status'] != 0:
            return flask.make_response("Error. Screenshot was not succesful", 500)

        return flask.make_response("Made screenshot at {}".format(dest), 200)

    def is_USB_connected(self):
        # Check that the USB mount point is there
        if not os.path.exists(self.USB):
            return False

        if not os.path.ismount(self.USB):
            return False

        return True

    def setup_USB(self):
        if not self.is_USB_connected():
            return False

        self.USB_path = os.path.normpath(self.USB + "/Robo_Screenshots/")

        if not os.path.isdir(self.USB_path):
            # hopefully we have access
            try:
                os.makedirs(self.USB_path)
            except Exception as e:
                import traceback
                self._logger.info("Error!: {}".format(e))
                self._logger.info(traceback.format_exc())
                return False

        return True
            

    def call_subprocess_all_output(self, command):
        com = ""
        if type(command) == str:
            com = command
        elif type(command) == list:
            com = " ".join(command)
    
        self._logger.info("Calling command {}".format(com))
        temp_p = subprocess.Popen(com,
                                  stdout=subprocess.PIPE,
                                  shell=True
        )
        output, error = temp_p.communicate()
        p_status = temp_p.wait()
    
        return {
            'output': output,
            'error': error,
            'p_status': p_status
        }
    
    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/robo_screenshot.js"],
            css=["css/robo_screenshot.css"],
            less=["less/robo_screenshot.less"]
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            robo_screenshot=dict(
                displayName="Robo_screenshot Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="Robo3D",
                repo="Robo_Screenshot",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/Robo3D/Robo_Screenshot/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Robo_screenshot"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Robo_screenshotPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

