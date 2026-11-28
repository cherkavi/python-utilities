# TAPO TP Link REST API

## python example
### installation 
```sh
## installation 
pip3 install tapo
pip3 install opencv-python-headless # for camera only 
```

### tapo p110
```sh
## run application 
export TAPO_USERNAME=$(keepass-tech-get-user devices-smart-home/tapo)
export TAPO_PASSWORD=$(keepass-tech-get-pass devices-smart-home/tapo)
export IP_ADDRESS='192.168.178.54'

# python3 check.py
python3 p110.py
```

### tapo c210
```sh
## run application 
export TAPO_USERNAME=$(keepass-tech-get-user devices-smart-home/tapo)
export TAPO_PASSWORD=$(keepass-tech-get-pass devices-smart-home/tapo)

export TAPO_CAMERA_USERNAME=$(keepass-tech-get-user devices-smart-home/tapo-camera-01)
export TAPO_CAMERA_PASSWORD=$(keepass-tech-get-pass devices-smart-home/tapo-camera-01)
export IP_ADDRESS='192.168.178.31'

# python3 check.py

python3 c210-option1.py  # Camera -> Settings -> Advanced Settings -> Camera Account -> ON ( TAPO_CAMERA_USERNAME, TAPO_CAMERA_PASSWORD )
python3 c210-option2.py

identify c210*.jpg
```

## Trouble shootings
### check network 
```sh
export IP_ADDRESS='192.168.178.31'

# RTSP — expected to work
nc -vz $IP_ADDRESS 554

# HTTPS — currently failing
nc -vz $IP_ADDRESS 443

# HTTP — diagnostic only
nc -vz $IP_ADDRESS 80
```

### Errors 
if you see errors like:
```
Exception: Tapo(Unauthorized { kind: "HASH_MISMATCH", description: "The device response did not match the challenge issued by the library. Make sure that the password of your TP-Link account is correct - it is case-sensitive." })
```
**Tapo for Android:**
1. Open Me.
2. Select Third-Party Services.
3. Open Third-Party Compatibility.
4. Switch it ON.
5. Wait approximately 60 seconds.
6. Reboot camera to avoid ⤵️
```
DEBUG:tapo.api.protocol.tapo_protocol:Using AES SSL protocol (TPAP login failed: Unauthorized: SESSION_EXPIRED: Session has expired. Re-authentication is required.)...
DEBUG:tapo.api.protocol.aes_ssl_protocol:Performing handshake1...
DEBUG:reqwest.connect:starting new connection 'Some("192.168.178.31")'
DEBUG:tapo.api.protocol.aes_ssl_protocol:Handshake1 error code: -40401
DEBUG:tapo.api.protocol.aes_ssl_protocol:Expected INVALID_NONCE (-40413) during handshake1, got -40401
```

