package com.google.cloud.samples.helloendpoints;

import android.accounts.Account;
import android.accounts.AccountManager;
import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.appspot.endpoint_project_1076.helloworld.Helloworld;
import com.appspot.endpoint_project_1076.helloworld.Helloworld.Greetings.Authed;
import com.appspot.endpoint_project_1076.helloworld.Helloworld.Greetings.GetGreeting;
import com.appspot.endpoint_project_1076.helloworld.Helloworld.Greetings.Multiply;
import com.appspot.endpoint_project_1076.helloworld.model.HelloGreeting;
import com.google.android.gms.auth.GoogleAuthException;
import com.google.android.gms.auth.GoogleAuthUtil;
import com.google.android.gms.common.AccountPicker;
import com.google.api.client.googleapis.extensions.android.gms.auth.GoogleAccountCredential;
import com.google.common.base.Strings;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

import static com.google.cloud.samples.helloendpoints.BuildConfig.DEBUG;

public class MainActivity extends Activity {

    private static final String LOG_TAG = "MainActivity";
    private static final int ACTIVITY_RESULT_FROM_ACCOUNT_SELECTION = 1000;

    private AuthorizationCheckTask mAuthTask;
    private String mEmailAccount = "";
    private GreetingsDataAdapter mListAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Prevent the keyboard from being visible upon startup.
        getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN);

        ListView listView = (ListView)this.findViewById(R.id.greetings_list_view);
        mListAdapter = new GreetingsDataAdapter((Application)this.getApplication());
        listView.setAdapter(mListAdapter);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (mAuthTask!=null) {
            mAuthTask.cancel(true);
            mAuthTask = null;
        }
    }

    public void performAuthCheck(String emailAccount) {
        // Cancel previously running tasks.
        if (mAuthTask != null) {
            try {
                mAuthTask.cancel(true);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        new AuthorizationCheckTask().execute(emailAccount);
    }

    class AuthorizationCheckTask extends AsyncTask<String, Integer, Boolean> {
        @Override
        protected Boolean doInBackground(String... emailAccounts) {
            Log.i(LOG_TAG, "Background task started.");

            if (!AppConstants.checkGooglePlayServicesAvailable(MainActivity.this)) {
                return false;
            }

            String emailAccount = emailAccounts[0];
            // Ensure only one task is running at a time.
            mAuthTask = this;

            // Ensure an email was selected.
            if (Strings.isNullOrEmpty(emailAccount)) {
                publishProgress(R.string.toast_no_google_account_selected);
                // Failure.
                return false;
            }

            Log.d(LOG_TAG, "Attempting to get AuthToken for account: " + mEmailAccount);

            try {
                // If the application has the appropriate access then a token will be retrieved, otherwise
                // an error will be thrown.
                GoogleAccountCredential credential = GoogleAccountCredential.usingAudience(
                        MainActivity.this, AppConstants.AUDIENCE);
                credential.setSelectedAccountName(emailAccount);

                String accessToken = credential.getToken();

                Log.d(LOG_TAG, "AccessToken retrieved");

                // Success.
                return true;
            } catch (GoogleAuthException unrecoverableException) {
                Log.e(LOG_TAG, "Exception checking OAuth2 authentication.", unrecoverableException);
                publishProgress(R.string.toast_exception_checking_authorization);
                // Failure.
                return false;
            } catch (IOException ioException) {
                Log.e(LOG_TAG, "Exception checking OAuth2 authentication.", ioException);
                publishProgress(R.string.toast_exception_checking_authorization);
                // Failure or cancel request.
                return false;
            }
        }

        @Override
        protected void onProgressUpdate(Integer... stringIds) {
            // Toast only the most recent.
            Integer stringId = stringIds[0];
            Toast.makeText(MainActivity.this, stringId, Toast.LENGTH_SHORT).show();
        }

        @Override
        protected void onPreExecute() {
            mAuthTask = this;
        }

        @Override
        protected void onPostExecute(Boolean success) {
            TextView emailAddressTV = (TextView) MainActivity.this.findViewById(R.id.email_address_tv);
            if (success) {
                // Authorization check successful, set internal variable.
                mEmailAccount = emailAddressTV.getText().toString();
            } else {
                // Authorization check unsuccessful, reset TextView to empty.
                emailAddressTV.setText("");
            }
            mAuthTask = null;
        }

        @Override
        protected void onCancelled() {
            mAuthTask = null;
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == ACTIVITY_RESULT_FROM_ACCOUNT_SELECTION && resultCode == RESULT_OK) {
            // This path indicates the account selection activity resulted in the user selecting a
            // Google account and clicking OK.

            // Set the selected account.
            String accountName = data.getStringExtra(AccountManager.KEY_ACCOUNT_NAME);
            TextView emailAccountTextView = (TextView)this.findViewById(R.id.email_address_tv);
            emailAccountTextView.setText(accountName);

            // Fire off the authorization check for this account and OAuth2 scopes.
            performAuthCheck(accountName);
        }
    }

    public void onClickGetGreeting(View view) {
        View rootView = view.getRootView();
        TextView greetingIdInputTV = (TextView)rootView.findViewById(R.id.greeting_id_edit_text);
        if (greetingIdInputTV.getText()==null ||
                Strings.isNullOrEmpty(greetingIdInputTV.getText().toString())) {
            Toast.makeText(this, "Input a Greeting ID", Toast.LENGTH_SHORT).show();
            return;
        };

        String greetingIdString = greetingIdInputTV.getText().toString();
        int greetingId = Integer.parseInt(greetingIdString);


        AsyncTask<Integer, Void, HelloGreeting> getAndDisplayGreeting =
                new AsyncTask<Integer, Void, HelloGreeting> () {
                    @Override
                    protected HelloGreeting doInBackground(Integer... integers) {
                        // Retrieve service handle.
                        Helloworld apiServiceHandle = AppConstants.getApiServiceHandle(null);

                        try {
                            GetGreeting getGreetingCommand = apiServiceHandle.greetings().getGreeting(integers[0]);
                            HelloGreeting greeting = getGreetingCommand.execute();
                            return greeting;
                        } catch (IOException e) {
                            Log.e(LOG_TAG, "Exception during API call", e);
                        }
                        return null;
                    }

                    @Override
                    protected void onPostExecute(HelloGreeting greeting) {
                        if (greeting!=null) {
                            displayGreetings(greeting);
                        } else {
                            Log.e(LOG_TAG, "No greetings were returned by the API.");
                        }
                    }
                };

        getAndDisplayGreeting.execute(greetingId);
    }

    private void displayGreetings(HelloGreeting... greetings) {
        String msg;
        if (greetings==null || greetings.length < 1) {
            msg = "Greeting was not present";
            Toast.makeText(this, msg, Toast.LENGTH_LONG).show();
        } else {
            if (DEBUG) {
                Log.d(LOG_TAG, "Displaying " + greetings.length + " greetings.");
            }

            List<HelloGreeting> greetingsList = Arrays.asList(greetings);
            mListAdapter.replaceData(greetings);
        }
    }

    public void onClickSendGreetings(View view) {
        View rootView = view.getRootView();

        TextView greetingCountInputTV = (TextView)rootView.findViewById(R.id.greeting_count_edit_text);
        if (greetingCountInputTV.getText()==null ||
                Strings.isNullOrEmpty(greetingCountInputTV.getText().toString())) {
            Toast.makeText(this, "Input a Greeting Count", Toast.LENGTH_SHORT).show();
            return;
        };

        String greetingCountString = greetingCountInputTV.getText().toString();
        final int greetingCount = Integer.parseInt(greetingCountString);

        TextView greetingTextInputTV = (TextView)rootView.findViewById(R.id.greeting_text_edit_text);
        if (greetingTextInputTV.getText()==null ||
                Strings.isNullOrEmpty(greetingTextInputTV.getText().toString())) {
            Toast.makeText(this, "Input a Greeting Message", Toast.LENGTH_SHORT).show();
            return;
        };

        final String greetingMessageString = greetingTextInputTV.getText().toString();

        AsyncTask<Void, Void, HelloGreeting> sendGreetings = new AsyncTask<Void, Void, HelloGreeting> () {
            @Override
            protected HelloGreeting doInBackground(Void... unused) {
                // Retrieve service handle.
                Helloworld apiServiceHandle = AppConstants.getApiServiceHandle(null);

                try {
                    HelloGreeting greeting = new HelloGreeting();
                    greeting.setMessage(greetingMessageString);

                    Multiply multiplyGreetingCommand = apiServiceHandle.greetings().multiply(greetingCount,
                            greeting);
                    greeting = multiplyGreetingCommand.execute();
                    return greeting;
                } catch (IOException e) {
                    Log.e(LOG_TAG, "Exception during API call", e);
                }
                return null;
            }

            @Override
            protected void onPostExecute(HelloGreeting greeting) {
                if (greeting!=null) {
                    displayGreetings(greeting);
                } else {
                    Log.e(LOG_TAG, "No greetings were returned by the API.");
                }
            }
        };

        sendGreetings.execute((Void)null);
    }

    public void onClickGetAuthenticatedGreeting(View unused) {
        if (!isSignedIn()) {
            Toast.makeText(this, "You must sign in for this action.", Toast.LENGTH_LONG).show();
            return;
        }

        AsyncTask<Void, Void, HelloGreeting> getAuthedGreetingAndDisplay =
                new AsyncTask<Void, Void, HelloGreeting> () {
                    @Override
                    protected HelloGreeting doInBackground(Void... unused) {
                        if (!isSignedIn()) {
                            return null;
                        };

                        if (!AppConstants.checkGooglePlayServicesAvailable(MainActivity.this)) {
                            return null;
                        }

                        // Create a Google credential since this is an authenticated request to the API.
                        GoogleAccountCredential credential = GoogleAccountCredential.usingAudience(
                                MainActivity.this, AppConstants.AUDIENCE);
                        credential.setSelectedAccountName(mEmailAccount);

                        // Retrieve service handle using credential since this is an authenticated call.
                        Helloworld apiServiceHandle = AppConstants.getApiServiceHandle(credential);

                        try {
                            Authed getAuthedGreetingCommand = apiServiceHandle.greetings().authed();
                            HelloGreeting greeting = getAuthedGreetingCommand.execute();
                            return greeting;
                        } catch (IOException e) {
                            Log.e(LOG_TAG, "Exception during API call", e);
                        }
                        return null;
                    }

                    @Override
                    protected void onPostExecute(HelloGreeting greeting) {
                        if (greeting!=null) {
                            displayGreetings(greeting);
                        } else {
                            Log.e(LOG_TAG, "No greetings were returned by the API.");
                        }
                    }
                };

        getAuthedGreetingAndDisplay.execute((Void)null);
    }

    private boolean isSignedIn() {
        if (!Strings.isNullOrEmpty(mEmailAccount)) {
            return true;
        } else {
            return false;
        }
    }

    public void onClickSignIn(View view) {
        TextView emailAddressTV = (TextView) view.getRootView().findViewById(R.id.email_address_tv);
        // Check to see how many Google accounts are registered with the device.
        int googleAccounts = AppConstants.countGoogleAccounts(this);
        if (googleAccounts == 0) {
            // No accounts registered, nothing to do.
            Toast.makeText(this, R.string.toast_no_google_accounts_registered,
                    Toast.LENGTH_LONG).show();
        } else if (googleAccounts == 1) {
            // If only one account then select it.
            Toast.makeText(this, R.string.toast_only_one_google_account_registered,
                    Toast.LENGTH_LONG).show();
            AccountManager am = AccountManager.get(this);
            Account[] accounts = am.getAccountsByType(GoogleAuthUtil.GOOGLE_ACCOUNT_TYPE);
            if (accounts != null && accounts.length > 0) {
                // Select account and perform authorization check.
                emailAddressTV.setText(accounts[0].name);
                mEmailAccount = accounts[0].name;
                performAuthCheck(accounts[0].name);
            }
        } else {
            // More than one Google Account is present, a chooser is necessary.

            // Reset selected account.
            emailAddressTV.setText("");

            // Invoke an {@code Intent} to allow the user to select a Google account.
            Intent accountSelector = AccountPicker.newChooseAccountIntent(null, null,
                    new String[]{GoogleAuthUtil.GOOGLE_ACCOUNT_TYPE}, false,
                    "Select the account to access the HelloEndpoints API.", null, null, null);
            startActivityForResult(accountSelector,
                    ACTIVITY_RESULT_FROM_ACCOUNT_SELECTION);
        }

    }

    /**
     * ArrayAdaptor that uses a static class to ensure no references to the Activity exist.
     */
    static class GreetingsDataAdapter extends ArrayAdapter {
        GreetingsDataAdapter(Application application) {
            super(application.getApplicationContext(), android.R.layout.simple_list_item_1,
                    application.greetings);
        }

        void replaceData(HelloGreeting[] greetings) {
            clear();
            for (HelloGreeting greeting : greetings) {
                add(greeting);
            }
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            TextView view = (TextView)super.getView(position, convertView, parent);

            HelloGreeting greeting = (HelloGreeting)this.getItem(position);

            StringBuilder sb = new StringBuilder();

            Set<String> fields = greeting.keySet();
            boolean firstLoop = true;
            for (String fieldName : fields) {
                // Append next line chars to 2.. loop runs.
                if (firstLoop) {
                    firstLoop = false;
                } else {
                    sb.append("\n");
                }

                sb.append(fieldName)
                        .append(": ")
                        .append(greeting.get(fieldName));
            }

            view.setTextColor(Color.BLACK);
            view.setText(sb.toString());
            return view;
        }
    }
}