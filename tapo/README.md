# TAPO TP Link REST API

## python example
```sh
## installation 
pip3 install tapo


## run application 
export TAPO_USERNAME=$(keepass-tech-get-user devices-smart-home/tapo)
export TAPO_PASSWORD=$(keepass-tech-get-pass devices-smart-home/tapo)
export IP_ADDRESS='192.168.178.54'

python3 p110.py
```