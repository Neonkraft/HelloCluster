# Setting up the repo
1. Clone this repository in the remote machine
2. Set up [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
3. Create a new environment:
   *    `conda create env --name hello_cluster_env python=3.9`
4. Activate the new environment and install the requirements:
   * `conda activate hello_cluster_env`
   * `pip install -r requirements.txt`
5. You should now be able to run the code as follows:
   * `python main.py --<cmd-line-arguments> <values>`

**IMPORTANT:** Remember, you are **not** supposed to run your python scripts this way on the clusters. Scripts should always be submitted as jobs (see next section). The *login nodes* should never be used for any kind of *compute* (not even, say, to run *Tensorboard*). Step 4 is only for local installations on your computer.

In the KI-SLURM (Meta) cluster, your account will be penalized by limiting your CPU usage for a while if you run compute-intensive processes on login nodes.

# Running the code on KI-SLURM (Meta)

There are two ways to run scripts on the cluster:
1. Submit a job using `sbatch`
2. Run your code in a SLURM interactive session using `srun`

Let's begin by looking at `sbatch`. First, you need to know which partitions you have access to.

## Finding out partitions you have access to
You can use `sinfo` to find this information.  A sample output might look like this:

| PARTITION     |   AVAIL  | TIMELIMIT  | NODES | STATE | NODELIST      |
| ------------  |     ---  | ---------  | ----- | ----- | ------------- |
| partitionXYZ  |      up  | 2-00:00:00 |   1   | idle  | xyzgpu[0-6]   |
| partitionABC  |      up  | 01:00:00   |   1   | idle  | xyzgpu[10, 20]|

## Submitting jobs with sbatch
See `./scripts/meta/run.sh` for an example of a job script. To submit a job:
1.  Edit `run.sh`:
       * Add the partition you want to run the job on
       * Adjust the path to your miniconda installation
2.  Create the directories required for the logs
3.  `sbatch scripts/meta/run.sh`

## See your submitted jobs
   * `squeue` # See all the jobs in the queue
   * `squeue -u user`  # See only user's jobs

## Cancel your submitted jobs
   * `scancel -u my_user`  # Cancel all your jobs
   * `scancel <jobid>`  # Cancel a specific job


## See summary of the current status of the cluster
   * `sfree`
## Running an interactive session
You can run an interactive session using `srun`. You can specify the parameters of the job using the same switches seen in `run.sh`. You only require an additional `--pty bash` to start a bash session.

   * `srun --partition <your_partition> --mem 6GB --job-name HelloClusterInteractiveSession --pty bash`

You will see that you are now logged into a compute node. From here, you may run python scripts as usual:
   * `python main.py --device cuda`

*Remember that you should only do this from a *compute node* that you acquired using `srun`, never a login node.*

# Debugging on KI-SLURM

We will use [VSCode](https://code.visualstudio.com/) and Simon Schrodi's scripts to debug the code that is running on the cluster. There are two parts to setting this up:
1. Install `Remote - SSH` extension on VSCode
2. Clone [Simon's repository](https://github.com/infomon/vscode_remote_debugging) and configure the debugging setup
## Remote access via VSCode

For developing code that sits on remote systems, it is convenient to use VSCode with Remote - SSH extension.

1. Bring up the Extensions view (Ctrl+Shift+X / Cmd+Shift+X). Or, `View` > `Extensions`
2. Install `Remote - SSH` extension (Extension ID: ms-vscode-remote.remote-ssh)
3. `View` > `Command Palette` > `Remote-SSH: Connect to Host...` > `+ Add New SSH Host` > `ssh <your_user>@kislogin2.xx.xx.xxxxxx`
4. Once you're connected to remote, you should be able to navigate to the directory of your repo in the Explorer (Ctrl+Shift+E / Cmd+Shift+E / `View` > `Explorer`)

## Configuring the Debug Setup
1. Clone [Simon's repository](https://github.com/infomon/vscode_remote_debugging) in your remote machine, in this repository directory, i.e., inside `/path/to/HelloCluster/`.
2. Change the following line in `vscode_remote_debugging/init.sh`:
      * From:  `python debug/_init.py --ip $ip --port $PORT --path $LAUNCH_JSON`
      * To:  `python vscode_remote_debugging/_init.py --ip $ip --port $PORT --path $LAUNCH_JSON`
3. Follow the instructions in his repo for the one-time setup.

Your configured `config.conf` should look something like this

```
WORKDIR /path/to/HelloCluster
PORT 4242
LAUNCH_JSON .vscode/launch.json
CONDA_SOURCE /path/to/miniconda3/bin/activate
CONDA_ENV hello_cluster_env
```

Your `.vscode/launch.json` should look like this (comments and `pathMappings` removed):
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            }
        }
    ]
}
```

Don't worry about the mismatch between the port numbers in `launch.json` and `config.conf`. That will be fixed by `init.sh` in the next part.
## Debugging
1. Start an interactive session:
   * `srun -p <partition_name> --pty bash`
2. Initialize `launch.json` with the details from `config.conf`
   *  `bash vscode_remote_debugging/init.sh`
3. Start the debugging session
   * `bash ./scripts/meta/debug.sh`
4. The code waits until the client is attached to run.
   * `View` > `Run` > `Python: Remote Attach`
5. Debug as if the code is running on your local machine!

