

##From "Blender – Interplanety" website tutorials: 
##https://b3d.interplanety.org/en/creating-multifile-add-on-for-blender/
##https://b3d.interplanety.org/en/debugging-multifile-blender-add-on-by-quick-reinstall/

##Their scripts should be used inside the multifile addon folders when they are installed in blender. You don't replace the __init__.py of your master branch code, leave it. However, do replace the __init__.py of the user addon folder for the addon using their scripts, since it just needs to work inside there

##Maybe, to use it with GitHub and Git, create a separate branch called "Debug" where the addon folder is installed for Blender, just use .gitignore to ignore the compiled python code
##This way, you can have two separate branches, and be able to commit and push your changes to Git with the Debug __init__.py






##For Visual Studio Code
##Step By Step Tutorial Website: (This is the one I used, and it worked)
https://b3d.interplanety.org/en/using-microsoft-visual-studio-code-as-external-ide-for-writing-blender-scripts-add-ons/

Make sure to have the setting of Update/Reload Addon when saved, for the Extension to easily reload when the addon is changed.

You must install the Extension for Visual Studio Code by Jacque Luckes: 
Youtube Video: https://www.youtube.com/watch?v=WbHN8w7GbJ0&feature=youtu.be

Use a Linter (For autocomplete for typing faster), https://pypi.org/project/fake-bpy-module-2.82/
Just download the folder for the most recent blender version
