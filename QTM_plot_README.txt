LDQM_GUI_plot uses general_plotting_vICFO to plot. This uses the data from ICFO
QTM_plot_v1 uses general plotting, and is the original version
QTM_plot_v2 uses general_plotting_v2 and is a version in which some of the plotting parameters changed because the data was somehow
different. 


In order to start the programme it calls template_GUI and labels_GUI. These two txt
files have therefore to be in the same folder as the code in another folder called 
QTM_templates. The code also calls general_plotting code, so this is also needed to be 
in the same folder as the QTM_plot code. The size and postion of the window can also be 
changed in the template_GUI

- Template_GUI provides the initial conditions for the different options
on the GUI. This can be modified by the user by changing template_GUI.txt values
The txt is loaded as a dictionary, such that the first and second column must be 
separated by a tab. The main parameters to be tuned for convenience are the data,template
and customized directories. If left blank eveytime a load file button is clicked the 
menu will go back to the last place from which a file was opened. If the directories
are set somewhere then each button will go to that directory. For example,
if 'data_directory' is 'C://Users/someone/data' then the dataset button will always be opened
at that directory and if 'template_directory' is 'C://Users/templates' then that would be the 
opened directory when 'load template is called'. Recommended option for 'customized directory'
is to make a folder inside the data folder being used, so it is very convenient to open
and check the graphs made. 

- Labels_GUI provides the options that appear in the labels for the x,y,z axis
By adding more columns to the txt these label options can be increased. 

- In addition extra templates can be added by the user by clicking the save template
button on the GUI. Then by loading a template this would be given to the graph shown. This
could be useful if for different data types different colormaps are prefered for example. 

- Then some png files also come in this folder. These are useful for the error messages. They 
have to be stored in QTM_images 