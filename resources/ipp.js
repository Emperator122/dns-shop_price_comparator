      var navigator = {
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        platform: 'Win32',
        plugins: []
      }

      var window = {
        JSEncrypt: {},
        location: {
          hash: ''
        }
      }

      var JSEncrypt;

      var screen = {

      }

      var document = {
        set cookie(str) {
          var terms = str.split(';');
          this._cookie += terms[0] + '; ';
        },
        get cookie() {
          return this._cookie;
        },
        _cookie: '',

        body: {
            appendChild: function (lala) {},
            removeChild: function (lala) {},
            style: {

            },
        },
        getElementsByTagName: function (name) {
          return [
            {
            appendChild: function (lala) {},
            removeChild: function (lala) {},
            style: {

            },
          },
            {
            appendChild: function (lala) {},
            removeChild: function (lala) {},
            style: {

            },
          },
            {
            appendChild: function (lala) {},
            removeChild: function (lala) {},
            style: {

            },
          }
          ]
        },
        createElement: function (name) {
          return {
            appendChild: function (lala) {},
            removeChild: function (lala) {},
            style: {

            },
          }
        }
      }

      function setTimeout(handler, timeout) {
        if(typeof handler == 'function')
        {
          JSEncrypt = window.JSEncrypt;
          handler();
        }
      }
