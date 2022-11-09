[reCaptcha client code](https://developers.google.com/recaptcha/docs/v3)
[reCaptcha server code](https://developers.google.com/recaptcha/docs/verify)

# google key
site key: 6Ldo3dsZAAAAAIV
secret  : 6Ldo3dsZAAAAACH



```html
<html>
        <head>
                <script src="https://www.google.com/recaptcha/api.js?render=6Ldo3dsZAAAAAIV"></script>
          
<script>
      function onClick(e) {
        //e.preventDefault();     
              console.log("start captcha");
        grecaptcha.ready(function() {
          grecaptcha.execute('6Ldo3dsZAAAAAIV', {action: 'submit'}).then(function(token) {
              console.log(token);                                     
          });
        });
      }
  </script>

        </head>
        <body>
                <button title="captcha" onclick="onClick()" >captcha </button>
        </body>
</html>

```


```sh
# check UI key from server side
curl -X POST -F "secret=6Ldo3dsZAAAAACH" -F "response=FaMFS6E" https://www.google.com/recaptcha/api/siteverify
```
