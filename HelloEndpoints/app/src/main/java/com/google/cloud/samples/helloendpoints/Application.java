package com.google.cloud.samples.helloendpoints;

import com.appspot.endpoint_project_1076.helloworld.model.HelloGreeting;
import com.google.api.client.util.Lists;

import java.util.ArrayList;

/**
 * Dummy Application class that can hold static data for use only in sample applications.
 *
 * TODO(developer): Implement a proper data storage technique for your application.
 */
public class Application extends android.app.Application {
    ArrayList<HelloGreeting> greetings = Lists.newArrayList();
}
