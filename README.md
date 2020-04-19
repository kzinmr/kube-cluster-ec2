# kube-cluster-ec2
Ansible playbooks that provision Kubernetes cluster on AWS EC2

## Prerequisites
### Install Ansible and Docker
- `./local_init.sh`

### SSH keygen for Kubernetes
- `ssh-keygen -t rsa -b 4096 -f ~/.ssh/my_aws_key`
- `ssh-add ~/.ssh/my_aws_key`

### Create a vault file to store credential information
- `mkdir -p group_vars/all`
- `ansible-vault create group_vars/all/pass.yml`
   - this enables: ansible-playbook *.yml --ask-vault-pass
   - if you don't want to type passwd each times:
      - `openssl rand -base64 2048 > vault.pass`
      - `ansible-vault create group_vars/all/pass.yml --vault-password-file vault.pass`
- input into the pass.yml like:
```
ec2_access_key: AAAAAAAAAAAAAABBBBBBBBBBBB
ec2_secret_key: afjdfadgf$fgajk5ragesfjgjsfdbtirhf
docker_hub_username: kzinmr
docker_hub_password: hogehoge
docker_hub_email: example@gmail.com
```

## Provision a Kubernetes cluster

### Create EC2 instances
- Create EC2 instances
   - `ansible-playbook create_instance.yml --vault-password-file vault.pass --tags create_ec2`
- Make `hosts` file
   - `ansible-playbook create_instance.yml --vault-password-file vault.pass --tags instance_info`

### Init Nodes
- `ansible-playbook init.yml -i hosts --vault-password-file vault.pass`

### Install Dependencies (docker, kube*-tools)
- `ansible-playbook kube-dependencies.yml -i hosts --vault-password-file vault.pass`

### Setup a Master Node
- `ansible-playbook master.yml -i hosts --vault-password-file vault.pass`
- In the master node, make sure that the Node is Ready by `kubectl get nodes`.

### Setup Worker Nodes
- `ansible-playbook workers.yml -i hosts --vault-password-file vault.pass`
- In the master node, make sure that the worker Nodes are Ready by `kubectl get nodes`.

## Build and push a Docker image of our app

- `ansible-playbook docker.yml --vault-password-file vault.pass`

## Deployment
- Initialize the deployment and the service (NodePort)
   - `ansible-playbook deploy.yml -i hosts --vault-password-file vault.pass --tags create`
- Check the created service
   - `ansible-playbook deploy.yml -i hosts --vault-password-file vault.pass --tags describe-nodeport`
   - `curl http://<worker_ip>:<node_port>`
- Deploy a new version of docker image
   1. edit `image_tag: <new_version_tag>` in `deploy.yml`
   2. `ansible-playbook deploy.yml -i hosts --vault-password-file vault.pass --tags update`
- Check the updated service
   - `curl http://<worker_ip>:<node_port>`
- Delete the deployment and the service
   - `ansible-playbook deploy.yml -i hosts --vault-password-file vault.pass --tags delete`
   

## References
- [Provisioning EC2 instances](https://medium.com/datadriveninvestor/devops-using-ansible-to-provision-aws-ec2-instances-3d70a1cb155f)
- [Creating a Kubernetes Cluster on Ubuntu18.04](https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04)
  - [on CentOS](https://github.com/ctienshi/kubernetes-ansible)
- [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
- [How to ignore ansible SSH authenticity checking?](https://stackoverflow.com/questions/32297456/how-to-ignore-ansible-ssh-authenticity-checking)
