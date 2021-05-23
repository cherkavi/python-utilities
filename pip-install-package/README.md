copy package to current folder
```sh
rsync -avz -e "ssh -i /home/projects/my_project/integration-prototype-keys.pem" /home/projects/my_project/integration-prototype/airflow-dag/airflow_shopify/ ubuntu@ec2-3.compute-1.amazonaws.com:~/airflow/airflow-dag/wondersign_airflow_shopify/
```
install current package 
```sh
pip3 install -U ~/path/to/this/folder
```
