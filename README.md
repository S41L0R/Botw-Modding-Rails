#BotW Rails

Hi! If you want to use this tool, here are some steps:

(Note: In Ice-Spear, you probably want to lay out some placeholder objects just to grab the coords from.)

1. Run the program.

2. Enter your first point into the boxes. 

3. Clicking "New Point" will add a point to your rail. You can edit that point by clicking "Next".

4. Once you're all done editing the points in your rail, make sure to specify the HashID you want your rail to have, 
its RailType (this is just the shape it will take), and its IsClosed value (This is just whether you want the last point to be connected to the first), 
as well as the path of the file you want to edit.

5. Click "Insert Rail", and you're pretty much all set. All you have to do now is link it to your actor in Ice-Spear. (Via the HashId)

NOTE: When the "Insert Rail" button is clicked, a backup of the original map file is saved into the "backup" folder in Botw Rails' root directory.

#Important!
Make sure to set the path to which you want to start at when selecting the file you want to edit. You can do this by editing DefaultPath.txt.
