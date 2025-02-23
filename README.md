# acx
Create an Audacity Nyquist audio plugin using Python or LISP that will adjust audio t omeet  the standard for audiobooks in Amazon Audible
Plugin should be compliant with the following standards: https://help.acx.com/s/article/what-are-the-acx-audio-submission-requirements 
Script should be able to take an MP3 audio file and then make it mono, then elminate the background noise, while leaving some, and adjust volume levels and so on to meet the ACX standards.
The audio software we are suing is Audacity: https://www.audacityteam.org/ and here is a link about dveloping plugins https://plugins.audacityteam.org/contributing/developing-your-own-plugins-and-scripts
And the plugin will be a Nyquist plugin for Audacity and we hope to contribute it to the open-source community under an appropriate license. 



# Resources

Explore plug-in examples and Nyquist programming at [**AudioNyq.com**](https://audionyq.com).

For an existing plugin that checks ACX standards, see the ACX Check at [Audacity Plugin Library](https://plugins.audacityteam.org/analyzers/analysis-plugins#acx-check). This resource is useful for comparing and understanding script configurations for Nyquist plugins.

Explore advanced scripting and tool integration for Audacity with Steve Daulton's work, which includes the enhanced `pipeclient.py`, a Python module for controlling Audacity. This repository offers valuable insights and code that could be instrumental in developing Python scripts for audio processing tasks. Check out the repository [here](https://github.com/SteveDaulton).
