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
