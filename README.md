# kube-cluster-ec2
Ansible playbooks that provision Kubernetes cluster on AWS EC2

## Prerequisites
- install Ansible
- ssh-keygen -t rsa -b 4096 -f ~/.ssh/my_aws_key

- ansible-vault create pass.yml
   - this enables: ansible-playbook *.yml --ask-vault-pass
   - if you don't want to type passwd each times:
      - openssl rand -base64 2048 > vault.pass
      - ansible-vault create pass.yml --vault-password-file vault.pass

- input into the pass.yml like:

ec2_access_key: AAAAAAAAAAAAAABBBBBBBBBBBB
ec2_secret_key: afjdfadgf$fgajk5ragesfjgjsfdbtirhf

## Procedure

### Create EC2 instances
- ansible-playbook create_instance.yml --vault-password-file vault.pass --tags create_ec2
- ansible-playbook create_instance.yml --vault-password-file vault.pass --tags instance_info
   - this makes hosts file

### Init Nodes
- ansible-playbook init.yml --vault-password-file vault.pass
### Install Dependencies (docker, kube*-tools)
- ansible-playbook kube-dependencies.yml --vault-password-file vault.pass
### Setup a Master Node
- ansible-playbook master.yml --vault-password-file vault.pass
- In the master node, make sure that the Node is Ready by kubectl get nodes.
### Setup Worker Nodes
- ansible-playbook workers.yml --vault-password-file vault.pass
- In the master node, make sure that the worker Nodes are Ready by kubectl get nodes.

## Check the created cluster actually works.
- ssh ubuntu@master_ip
- kubectl create deployment nginx --image=nginx
- kubectl get deployments
- kubectl expose deploy nginx --port 80 --target-port 80 --type NodePort
- kubectl get services
- curl http://worker_ip:nginx_port
- kubectl delete service nginx
- kubectl delete deployment nginx

## References
- [Provisioning EC2 instances](https://medium.com/datadriveninvestor/devops-using-ansible-to-provision-aws-ec2-instances-3d70a1cb155f)
- [Creating a Kubernetes Cluster on Ubuntu18.04](https://www.digitalocean.com/community/tutorials/how-to-create-a-kubernetes-cluster-using-kubeadm-on-ubuntu-18-04)
  - [on CentOS](https://github.com/ctienshi/kubernetes-ansible)
- [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)