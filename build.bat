cd nxtemu
setup.py py2exe>py2exe-emu-log.txt
@echo ---------------------------------------- >> py2exe-emu-log.txt
@echo      nxtemu generated >> py2exe-emu-log.txt
@echo ---------------------------------------- >> py2exe-emu-log.txt

cd ..
cd nxted
setup.py py2exe>py2exe-ed-log.txt
@echo ---------------------------------------- >> py2exe-ed-log.txt
@echo      nxted generated >> py2exe-ed-log.txt
@echo ---------------------------------------- >> py2exe-ed-log.txt
