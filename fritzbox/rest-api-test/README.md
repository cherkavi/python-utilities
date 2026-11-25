# FRITZBOX REST API 
undocumented communication via REST API with FritzBox 
```sh
# export FRITZ_HOST=
export FRITZ_USER=$(keepass-tech-get-user devices-smart-home/fritzbox)
export FRITZ_PASSWORD=$(keepass-tech-get-pass devices-smart-home/fritzbox)

python3 fritzbox-rest-api-test.py > out.txt
```