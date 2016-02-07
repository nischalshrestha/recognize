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
 * Whether or not the user is signed in.
 * @type {boolean}
 */
google.appengine.samples.hello.signedIn = false;


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
  element.innerHTML = greeting;
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
 * Gets a numbered greeting via the API.
 * @param {string} id ID of the greeting.
 */
google.appengine.samples.hello.getAlbums = function() { 
  gapi.client.recognize.albums.get().execute(
      function(resp) {
        if (!resp.code) {
          albums = resp.albums || [];
          for (var i = 0; i < albums.length; i++) {  
            album = albums[i];
            google.appengine.samples.hello.print("title: "+album.title
              +" category: "+album.category
              +" album_type: "+album.album_type
              +" date: "+album.date);
            questions = album.questions;
            for (var k = 0; k < questions.length; k++){ //List of questions
              images = questions[k].images;
              google.appengine.samples.hello.print("question "+k+" title: "+questions[k].title+" question "+k+" fact: "+questions[k].fact);
              for (var j = 0; j < images.length; j++){ //List of question's images
                document.getElementById("album_image_"+j).src = "data:image/png;base64,"+images[j].image_url;
              }
            }
          }
        }
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

  var getAlbums = document.querySelector('#getAlbums');
  getAlbums.addEventListener('click', function(e) {
    google.appengine.samples.hello.getAlbums();
  });

  // Tutorial stuff below

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

  // Tutorial code

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

  // apisToLoad = 2; // must match number of calls to gapi.client.load()
  gapi.client.load('recognize', 'v1', callback, apiRoot);
  auth2 = gapi.client.load('oauth2', 'v2', callback);
};