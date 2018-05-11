/*
 * View model for Robo_Screenshot
 *
 * Author: Matt Pedler
 * License: AGPLv3
 */
$(function() {
    function Robo_screenshotViewModel(parameters) {
        var self = this;
        self.robo_server_message = ko.observable('')

        self.take_screenshot = function(){
            console.log("Taking Screenshot!")
            var request = new XMLHttpRequest()
            request.open("GET", "plugin/robo_screenshot/take_screenshot")
            request.setRequestHeader("X-Api-Key", OctoPrint.options.apikey)
            request.onreadystatechange = function() {
                if (request.readyState == XMLHttpRequest.DONE) {
                    console.log(request.response)
                    console.log(request.status)
                    if( request.status != 200){
                        self.showResponse(false, request.response)
                    } else {
                        self.showResponse(true, request.response)
                    }
                }
            }
            request.send()
        }

        self.showResponse = function(success, message) {

          // Bind server message
          self.robo_server_message(message)

          console.log(self.robo_server_message())

          var snackbar = document.getElementById("screenshot_snackbar")

          // Set the color of the snackbar depending the server response
          if (success == true)
            snackbar.style.backgroundColor = 'green'
          else
            snackbar.style.backgroundColor = 'red'

          snackbar.className = "show"

          console.log("Snackbar Activate: " + snackbar.className)
        }
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: Robo_screenshotViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "settingsViewModel"/* "loginStateViewModel", "settingsViewModel" */ ],
        // Elements to bind to, e.g. #settings_plugin_robo_screenshot, #tab_plugin_robo_screenshot, ...
        elements: ["#settings_plugin_robo_screenshot" /* ... */ ]
    });
});
