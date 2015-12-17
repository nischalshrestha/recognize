/**
 * @fileoverview
 * Provides methods for the Hello Endpoints sample UI and interaction with the
 * Hello Endpoints API.
 */

/** google global namespace for Google projects. */
var google = google || {};

/** appengine namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

/** samples namespace for App Engine sample code. */
google.appengine.samples = google.appengine.samples || {};

/** hello namespace for this sample. */
google.appengine.samples.hello = google.appengine.samples.hello || {};
/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
// google.appengine.samples.hello.CLIENT_ID =
    // '141815902829-9brrjl3uhogcqhnl111uvm9u556op701.apps.googleusercontent.com';

/**
 * Scopes used by the application.
 * @type {string}
 */
// google.appengine.samples.hello.SCOPES =
//     'https://www.googleapis.com/auth/userinfo.email ' +
//     'https://www.googleapis.com/auth/plus.login';
/**
 * Whether or not the user is signed in.
 * @type {boolean}
 */
google.appengine.samples.hello.signedIn = false;

/**
 * Loads the application UI after the user has completed auth.
 */
// google.appengine.samples.hello.userAuthed = function() {
//   var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
//     if (!resp.code) {
//       google.appengine.samples.hello.signedIn = true;
//       document.querySelector('#signinButton').textContent = 'Sign out';
//       document.querySelector('#authedGreeting').disabled = false;
//     }
//   });
// };
/**
 * Handles the auth flow, with the given value for immediate mode.
 * @param {boolean} mode Whether or not to use immediate mode.
 * @param {Function} callback Callback to call on completion.
 */
// google.appengine.samples.hello.signin = function(mode, callback) {
//   gapi.auth.authorize({client_id: google.appengine.samples.hello.CLIENT_ID,
//       scope: google.appengine.samples.hello.SCOPES, immediate: mode},
//       callback);
// };
/**
 * Presents the user with the authorization popup.
 */
// google.appengine.samples.hello.auth = function() {
//   if (!google.appengine.samples.hello.signedIn) {
//     google.appengine.samples.hello.signin(false,
//         google.appengine.samples.hello.userAuthed);
//   } else {
//     google.appengine.samples.hello.signedIn = false;
//     document.querySelector('#signinButton').textContent = 'Sign in';
//     document.querySelector('#authedGreeting').disabled = true;
//   }
// };

/**
 * Signs the user out.
 */
google.appengine.samples.hello.signout = function() {
  document.getElementById('signinButtonContainer').classList.add('visible');
  document.getElementById('signedInStatus').classList.remove('visible');
  google.appengine.samples.hello.signedIn = false;
}

/**
 * Prints a greeting to the greeting log.
 * param {Object} greeting Greeting to print.
 */
google.appengine.samples.hello.print = function(greeting) {
  var element = document.createElement('div');
  element.classList.add('row');
  element.innerHTML = greeting.message;
  document.querySelector('#outputLog').appendChild(element);
};

/**
* Displays an image
*/
google.appengine.samples.hello.showImage = function(idx, src, alt) {
    var image = document.getElementById("album_image_"+idx);
    var downloadingImage = new Image();
    downloadingImage.onload = function(){
        image.src = this.src;
    };
    downloadingImage.src = src;
    downloadingImage.alt = alt;
};

/**
 * Gets a numbered greeting via the API.
 * @param {string} id ID of the greeting.
 */
google.appengine.samples.hello.getImages = function(id) {
  gapi.client.recognize.greetings.getImages({'id': id}).execute(
      function(resp) {
        if (!resp.code) {
          resp.items = resp.items || [];
          for (var i = 0; i < resp.items.length; i++) {
            google.appengine.samples.hello.showImage(i, resp.items[i].image_url, "test query");
          }
        }
      });
};

/**
 * Gets a numbered greeting via the API.
 * @param {string} id ID of the greeting.
 */
google.appengine.samples.hello.nextImageSet = function(image) {
  gapi.client.recognize.greetings.uploadImages({'image': image}).execute(
      function(resp) {
        if (!resp.code) {
          google.appengine.samples.hello.print(image);
          // google.appengine.samples.hello.showImage(resp.image_url, 250, 250, "Test Image");
          // console.log("Inside getGreeting in base.js!");
        }
      });
};

/**
 * Lists greetings via the API.
 */
google.appengine.samples.hello.listGreeting = function() {
  gapi.client.recognize.greetings.listGreeting().execute(
      function(resp) {
        if (!resp.code) {
          resp.items = resp.items || [];
          for (var i = 0; i < resp.items.length; i++) {
            google.appengine.samples.hello.print(resp.items[i]);
          }
        }
      });
};

/**
 * Gets a greeting a specified number of times.
 * @param {string} greeting Greeting to repeat.
 * @param {string} count Number of times to repeat it.
 */
google.appengine.samples.hello.multiplyGreeting = function(
    greeting, times) {
  gapi.client.helloworld.greetings.multiply({
      'message': greeting,
      'times': times
    }).execute(function(resp) {
      if (!resp.code) {
        google.appengine.samples.hello.print(resp);
      }
    });
};
/**
 * Greets the current user via the API.
 */
google.appengine.samples.hello.authedGreeting = function(id) {
  gapi.client.helloworld.greetings.authed().execute(
      function(resp) {
        google.appengine.samples.hello.print(resp);
      });
};
/**
 * Enables the button callbacks in the UI.
 */
google.appengine.samples.hello.enableButtons = function() {

  var getGreeting = document.querySelector('#getImages');
  getGreeting.addEventListener('click', function(e) {
    google.appengine.samples.hello.getImages(document.querySelector('#searchTerm').value);
  });

  // var getImage = document.querySelector('#upload_image');
  // getImage.addEventListener('click', function(e){
  //   google.appengine.samples.hello.uploadImage(
  //     document.querySelector('#album_image').value)
  // })

  // var listGreeting = document.querySelector('#listGreeting');
  // listGreeting.addEventListener('click',
  //     google.appengine.samples.hello.listGreeting);

  // var multiplyGreetings = document.querySelector('#multiplyGreetings');
  // multiplyGreetings.addEventListener('click', function(e) {
  //   google.appengine.samples.hello.multiplyGreeting(
  //       document.querySelector('#greeting').value,
  //       document.querySelector('#count').value);
  // });

  // var authedGreeting = document.querySelector('#authedGreeting');
  // authedGreeting.addEventListener('click',
  //     google.appengine.samples.hello.authedGreeting);

  
  // var signinButton = document.querySelector('#signinButton');
  // signinButton.addEventListener('click', google.appengine.samples.hello.auth);
};
/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
google.appengine.samples.hello.init = function(apiRoot, tokenEmail) {
  // Loads the OAuth and helloworld APIs asynchronously, and triggers login
  // when they have completed.
  // var apisToLoad;
  // var callback = function() {
  //   if (--apisToLoad == 0) {
      // google.appengine.samples.hello.signedIn = true;
      // document.getElementById('userLabel').innerHTML = tokenEmail;
      // google.appengine.samples.hello.signin(true,
      //     google.appengine.samples.hello.userAuthed);
  //   }
  // }
  var callback = function() {
    google.appengine.samples.hello.enableButtons();
    google.appengine.samples.hello.signedIn = true;
    if(tokenEmail != ""){
      document.getElementById('userLabel').innerHTML = tokenEmail;
    }
  }

  // apisToLoad = 1; // must match number of calls to gapi.client.load()
  gapi.client.load('recognize', 'v1', callback, apiRoot);
  // gapi.client.load('oauth2', 'v2', callback);
};