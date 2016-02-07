// Copyright 2013 Google Inc. All Rights Reserved.

/**
 * @fileoverview
 * Provides methods for the utility methods needed to render the Google+
 * Sign-In button.
 *
 * @author dhermes@google.com (Danny Hermes)
 */

/** google global namespace for Google projects. */
var google = google || {};

/** devrel namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

/** samples namespace for DevRel sample code. */
google.appengine.samples = google.appengine.samples || {};

/** TicTacToe namespace for this sample. */
google.appengine.samples.hello = google.appengine.samples.hello || {};

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
google.appengine.samples.hello.CLIENT_ID =
    '1176089533-lbhj1m9vbukaqtn0p55lg35coaova4hc.apps.googleusercontent.com';

/**
 * Scopes used by the application.
 * @type {string}
 */
google.appengine.samples.hello.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email ' +
    'https://www.googleapis.com/auth/plus.login';

/**
 * Parses email from the claim set of a JWT ID token.
 *
 * NOTE: We are not validating the ID token since from a trusted source.
 *       We are simply parsed the value from the JWT.
 *
 * See http://www.tbray.org/ongoing/When/201x/2013/04/04/ID-Tokens
 * or
 * http://openid.net/specs/openid-connect-messages-1_0.html#StandardClaims
 * for more info.
 *
 * @param {string} idToken A base64 JWT containing a user ID token.
 * @return {string} The email parsed from the claim set, else undefined
 *                  if one can't be parsed.
 */
google.appengine.samples.hello.getEmailFromIDToken = function(idToken) {

  if (typeof idToken !== 'string') {
    return;
  }

  var segments = idToken.split('.');
  if (segments.length !== 3) {
    return;
  }

  try {
    var claimSet = JSON.parse(atob(segments[1]));
  } catch (e) {
    return;
  }

  if (claimSet.email && typeof claimSet.email === 'string') {
    return claimSet.email;
  }
}

/**
 * Handles the Google+ Sign In response.
 *
 * Success calls google.appengine.samples.hello.init. Failure makes the Sign-In
 * button visible.
 *
 * @param {Object} authResult The contents returned from the Google+
 *                            Sign In attempt.
 */
google.appengine.samples.hello.signinCallback = function(authResult) {

  var tokenEmail = google.appengine.samples.hello.getEmailFromIDToken(
      authResult.id_token);
  if (authResult.access_token && tokenEmail) {
    console.log(tokenEmail);
    google.appengine.samples.hello.init('//' + window.location.host + '/_ah/api',
                                   tokenEmail);

    document.getElementById('signinButtonContainer').classList.remove(
        'visible');
    document.getElementById('signedInStatus').classList.add('visible');
  } else {
    document.getElementById('signinButtonContainer').classList.add('visible');
    document.getElementById('signedInStatus').classList.remove('visible');
    if (!authResult.error) {
      console.log('Unexpected result');
      console.log(authResult);
    } else if (authResult.error !== 'immediate_failed') {
      console.log('Unexpected error occured: ' + authResult.error);
    } else {
      console.log('Immediate mode failed, user needs to click Sign In.');
    }
  }
};

/**
 * Renders the Google+ Sign-in button using auth parameters.
 */
google.appengine.samples.hello.render = function() {
  gapi.signin.render('signinButton', {
    'callback': google.appengine.samples.hello.signinCallback,
    'clientid': google.appengine.samples.hello.CLIENT_ID,
    'cookiepolicy': 'single_host_origin',
    'requestvisibleactions': 'http://schemas.google.com/AddActivity',
    'scope': google.appengine.samples.hello.SCOPES
  });
};

// A quirk of the JSONP callback of the plusone client makes it so
// our callback must exist as an element in window.
window['google.appengine.samples.hello.render'] = google.appengine.samples.hello.render;

// Recommended code to load Google+ JS library.
(function() {
    // console.log("here!");
    var newScriptElement = document.createElement('script');
    newScriptElement.type = 'text/javascript';
    newScriptElement.async = true;
    newScriptElement.src = 'https://apis.google.com/js/client:plusone.js' +
                           '?onload=google.appengine.samples.hello.render';
    var firstScriptElement = document.getElementsByTagName('script')[0];
    firstScriptElement.parentNode.insertBefore(newScriptElement,
                                               firstScriptElement);
 
})();
