# Configuration HPC and CEE

## HPC

Getting started with Sculpt application on the Chewie HPC machines.  

* On the SNL local Mac, connect with the GlobalProtect application (virtual private network).
* From a terminal:

```bash
$ ssh chewie.sandia.gov
```

Clone the `sibl-dev` repo:

```bash
chovey@chewie-login6:~$ git clone git@github.com:hovey/sibl-dev.git
Cloning into 'sibl-dev'...
Warning: Permanently added the RSA host key for IP address '140.82.113.4' to the list of known hosts.
Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
chovey@chewie-login6:~$

chovey@chewie-login6:~$ cd .ssh/
chovey@chewie-login6:~/.ssh$ ll
total 16
-rw------- 1 chovey chovey  743 Sep  6  2019 authorized_keys
-rw------- 1 chovey chovey 3239 Sep  6  2019 id_rsa
-rw------- 1 chovey chovey  739 Sep  6  2019 id_rsa.pub
-rw------- 1 chovey chovey 3502 Jul 20 17:17 known_hosts
chovey@chewie-login6:~/.ssh$
```

Copy the existing `id_rsa.pub` into the SSH keys / Add new webpage on GitHub.
That doesn't work because an *OpenSSH* key pair is need instead.  
See https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
page.

Generate a `chewie-ecdsa` key pair using `ssh-keygen -t ed25519 -C "your_email@example.com"` as follows:

```bash
ssh-keygen -t ed25519 -C "chovey@sandia.gov"

chovey@chewie-login6:~/.ssh$ ll

total 24
-rw------- 1 chovey chovey  743 Sep  6  2019 authorized_keys
-rw------- 1 chovey chovey  411 Jul 20 17:24 id_ed25519
-rw------- 1 chovey chovey   99 Jul 20 17:24 id_ed25519.pub
-rw------- 1 chovey chovey 3239 Sep  6  2019 id_rsa
-rw------- 1 chovey chovey  739 Sep  6  2019 id_rsa.pub
-rw------- 1 chovey chovey 3502 Jul 20 17:17 known_hosts
chovey@chewie-login6:~/.ssh$
```

Copy the new `id_ed25519.pub` into the SSH keys / Add new webpage on GitHub, 
name it `chewie-ed` in the **Title:** field.

Start the ssh-agent in the background with `$ eval "$(ssh-agent -s)"` e.g.,

```bash
chovey@chewie-login6:~/.ssh$ eval "$(ssh-agent -s)"

Agent pid 186616
```

Add the ssh key to the ssh-agent with `$ ssh-add ~/.ssh/id_ed25519`, e.g.,

```bash
chovey@chewie-login6:~/.ssh$ ssh-add ~/.ssh/id_ed25519

Identity added: /ascldap/users/chovey/.ssh/id_ed25519 (chovey@sandia.gov)
chovey@chewie-login6:~/.ssh$
```

Test the connection with `$ ssh -T git@github.com`

```bash
chovey@chewie-login6:~/.ssh$ ssh -T git@github.com

Warning: Permanently added the RSA host key for IP address '140.82.114.4' to the list of known hosts.
Hi hovey! You've successfully authenticated, but GitHub does not provide shell access.
chovey@chewie-login6:~/.ssh$
```

*[Second attempt]:* Clone the `sibl-dev` repo:

```bash
cd ~

chovey@chewie-login6:~$ git clone git@github.com:hovey/sibl-dev.git

Cloning into 'sibl-dev'...
remote: Enumerating objects: 138, done.
remote: Counting objects: 100% (67/67), done.
remote: Compressing objects: 100% (57/57), done.
remote: Total 138 (delta 14), reused 62 (delta 10), pack-reused 71
Receiving objects: 100% (138/138), 224.30 MiB | 34.34 MiB/s, done.
Resolving deltas: 100% (29/29), done.
Updating files: 100% (80/80), done.
chovey@chewie-login6:~$ cd sibl-dev/

chovey@chewie-login6:~/sibl-dev$ ls
admin  cya  mathematica  notes  present  README.md  refs
chovey@chewie-login6:~/sibl-dev$
```

## Autotwin/mesh

```bash
cd ~/autotwin
git clone git@github.com:autotwin/mesh.git

cd mesh
python -m venv .venv
source .venv/bin/activate       # for bash shell

module load aue/anaconda3 # loads Python 3.11.5
pip install -e .  # install in dev mode, with editable

<-- snip -->
  WARNING: The script pygmentize is installed in '/ascldap/users/chovey/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  WARNING: The scripts atmesh, atmeshinfo, cubit_inp_to_quality_csv, npy_to_mesh, sculpt_stl_to_inp and version are installed in '/ascldap/users/chovey/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
<-- snip -->
```

Update paths:

```bash
(.venv) ~/autotwin/mesh $ PATH="/ascldap/users/chovey/.local/bin:${PATH}"
(.venv) ~/autotwin/mesh $ export PATH
(.venv) ~/autotwin/mesh $ PATH="/ascldap/users/chovey/.local/bin:${PATH}"
(.venv) ~/autotwin/mesh $ export PATH
(.venv) ~/autotwin/mesh $ echo $PATH
```

Test the installation was successful by echoing the command line interface
documentation:

```bash
atmesh

------
atmesh
------

This is the command line interface help.

atmesh

    (this command) Echos the command line interface.

atmeshinfo

    Prints the module's dependencies.

cubit_inp_to_quality_csv <input_file.yml>

    Given an input file with schema of version 1.6,
    converts ABAQUS .inp file to a quality metric,
    e.g., minimum scaled Jacobian file, in comma
    separated value (.csv) format.

npy_to_mesh <input_file.yml>

    Given a semantic segmentation consisiting of non-zero integers
    to designate a unique material (and integer 0 to denote
    void surrounding the materials), saved in .npy format,
    converts the recipe in <input_file.yml> to an all-hexahedral
    finite element mesh in the Exodus .e format.

sculpt_stl_to_inp <input_file.yml>

    Given an input file with schema of version 1.6,
    converts a STL file, containing an isosurface, to an
    all-hex solid in ABAQUS mesh format.

version

    Prints the version of the yml input file schema, and
    prints the semantic version of the autotwin mesh module.

```

## CEE

```bash
# This template is intended for a blade machine on the CEE lan
cd ${remote.dir}
source /etc/bashrc

export NO_SUBMIT=true

# If input deck was created on Windows, hidden characaters might break the awk command
dos2unix ${input.deck.name}

# If required, decompose input mesh
if grep -q input_mesh "${input.deck.name}"; then
   module load sierra
   input_mesh=$(awk -F'input_mesh = ' '{print $2}' ${input.deck.name})
   decomp -p ${num.processors} ${input_mesh}
fi

/projects/cubit/sculpt64-beta  -j ${num.processors} -i ${input.deck.name} > ${timestamp}.log

# The exodus_file base name might be different to input file base name,
# so grab the name and use it for epu
exodus_file=$(awk -F 'exodus_file = ' '{print $2}' ${input.deck.name})

if [ "${num.processors}" == "1" ]
then
   mv ${exodus_file}.e.1.0 ${exodus_file}.e
else
   module load sierra
   epu -p ${num.processors} ${exodus_file}
   rm -rf ${exodus_file}.e.*
fi
```
