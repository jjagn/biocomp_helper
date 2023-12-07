import PyInstaller.__main__
import os
    
PyInstaller.__main__.run([  
     'name-%s%' % 'biocomp_buddy',
     '--onefile',
     '--windowed',
     os.path.join('./', 'biocomp_helper.py'), """your script and path to the script"""                                        
])