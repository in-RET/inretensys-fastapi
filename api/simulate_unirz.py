import os
import stat

import paramiko

from .constants import *


def simulate_unirz(configfile, foldername, ftype, file, username, passwd):

    csh_value = {
        'jobname': foldername,
        'foldername': foldername,
        'configuration': os.path.basename(configfile)
    }

    csh_template = \
"""#!/bin/csh
#BSUB -q "BatchXL"
#BSUB -J "simulation_{jobname}"
#BSUB -L /bin/csh
#BSUB -eo logs/%J.err
#BSUB -oo logs/%J.log
#BSUB -n 48
#BSUB -cwd $HOME/work/{jobname}

pwd
module purge

source /usr/app-soft/anaconda3/etc/profile.d/conda.csh

module load python/anaconda3

if [[ $(conda env list) = *"simulation_environment"* ]]; then
   echo "Python environment found... activating..."
   conda activate simulation_environment
else
   echo "Python environment not found... creating..."
   conda env create --file environment.yaml
   conda activate simulation_environment
   exit
fi;

pip install --upgrade InRetEnsys-0.2a4-py3-none-any.whl

module load gurobi/v911
echo $GRB_LICENSE_FILE

setenv GUROBI_HOME /usr/app-soft/gurobi/gurobi911/linux64/
setenv PATH ${{PATH}}:${{GUROBI_HOME}}/bin 
setenv LD_LIBRARY_PATH ${{LD_LIBRARY_PATH}}:${{GUROBI_HOME}}/lib

python main.py -wdir ${{PWD}} {configuration}
""".format(**csh_value)

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(FTP_SERVER, 22, username, passwd)

    with client.open_sftp() as sftp:
        sftp.chdir("work")
        sftp.mkdir(csh_value['jobname'])
        sftp.chdir(csh_value['jobname'])
        with sftp.open("batchscript.csh", "wt") as sftp_file:
            sftp_file.write(csh_template)
            sftp_file.close()
        sftp.chmod("batchscript.csh", stat.S_IRWXU)

        if ftype == FTYPE_JSON:
            sftp_file = sftp.open("config.json", 'wt')
        elif ftype == FTYPE_BINARY:
            sftp_file = sftp.open("config.bin", 'wb')
        sftp_file.write(file)
        sftp_file.close()       
        
        sftp.put(os.path.join(os.getcwd(), "api", "required", "environment.yaml"), "environment.yaml") 
        sftp.put(os.path.join(os.getcwd(), "api", "required", "InRetEnsys-0.2a4-py3-none-any.whl"), "InRetEnsys-0.2a4-py3-none-any.whl")
        sftp.put(os.path.join(os.getcwd(), "api", "required", "main.py"), "main.py")

        sftp.close()
