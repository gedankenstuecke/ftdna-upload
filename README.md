# A *FamilyTreeDNA* upload project for *Open Humans*

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

This is a Django project that is based on the [Open Humans Data Uploader](https://www.github.com/gedankenstuecke/oh_data_uploader). It uses the same general logic for setting up the project. But in addition to this it adds a simple *Celery* task that is enqueued as soon as a new file is uploaded.

This task grabs the newly uploaded file from *Open Humans* and performs some general verifications to test that it's a proper *FamilyTreeDNA* file. Invalid rows from the file are being deleted to ensure the privacy of participants. If the uploaded file is completely broken the file will be deleted and the user is getting a message notifying them about the problem.

## Deployment to *heroku*.

This is a 5-Step guide to get your own Open Humans data upload project up and running. It does not require neither programming nor command line experience.

### **Step 1**: Click the *deploy to heroku* button above.

Log in into your existing *heroku* account or create a new one. (This Uploader is designed to completely work with the free tier of *heroku*, so you don't have to give them any payment details).

### **Step 2**: Fill out the parameters that *heroku* asks you

(see screenshot below).

![](docs/deploy_heroku.png)

*heroku* asks you to give your app a name, for this demo we use `ohuploadertemplatetest`. Repeat this name below for the `HEROKUCONFIG_APP_NAME`. The second important parameter is the `ADMIN_PASSWORD`. You will later need this to connect your uploader to *Open Humans* and to customize your uploader. Once you have entered this information you click on *deploy app* and after a while you should get a success message.

If you have given `ohuploadertemplatetest` as the `HEROKUCONFIG_APP_NAME` your uploader should be available at `https://ohuploadertemplatetest.herokuapp.com/`.

### **Step 3**: Create your project on *Open Humans*

On *Open Humans* you can create a new project by [clicking on *create a new OAuth2 data request project*](https://www.openhumans.org/direct-sharing/projects/manage/).

![](docs/oh_config.png)

Fill out the form and enter all the required information. The most important to make sure that your uploader will work is the *Redirect URL*, which will be set depending on your *App name*. If your app's main page is `https://ohuploadertemplatetest.herokuapp.com/`, then the `REDIRECT URL` should be `https://ohuploadertemplatetest.herokuapp.com/complete`.

### **Step 4**: Grab your Oauth credentials from *Open Humans*

Once you click on save in **Step 3** you should come back to the list of all projects you are currently running. This should now contain your new project.

![](docs/oh_projects.png)

Click on the name of your new project and this new page you will see your `CLIENT ID` and `CLIENT SECRET`. This are the two missing bits of information that you will need to connect your new *heroku* Uploader app to *Open Humans*.

![](docs/oh_oauth.png)

### **Step 5**: Finalize your Uploader setup

You can now go to `https://HEROKUCONFIG_APP_NAME.herokuapp.com/project-admin/login` (replace `HEROKUCONFIG_APP_NAME` with the name you gave in *Step 2*) and use the `ADMIN_PASSWORD` you gave in *Step 2* to log in.

![](docs/template_setup.png)

Once logged in you will see a page that gives you all options to edit your template and make it work for your own project. As a most important, first step you should start by clicking `Edit Open Humans settings`. Here you can enter the `CLIENT ID` and `CLIENT SECRET` that you looked up in *Step 4*. Afterwards you can edit more things about your project like:
- the Title & Description
- the metadata used for the uploaded files
- all the texts that should appear on your uploader website.

This last bit is done [by writing Markdown formatted text right into the forms](https://help.github.com/articles/basic-writing-and-formatting-syntax/).

## Local Deployment and Development
The *Open Humans Uploader* is written in *Python 3.6+*, uses the *Django 2.0* framework and is designed to be ultimately deployed
to *Heroku*. You will need some additional modules and packages to locally experiment with this uploader template or to develop it further. A full step-by-step guide that should work for Mac OS (and with minor differences for Linux) [can be found in the INSTALL.md](https://github.com/gedankenstuecke/ftdna-upload/blob/master/INSTALL.md).


## Contributing
We'd love to get your contribution to this project, thanks so much for your interest in this! Please [read our `CONTRIBUTING.md`](https://github.com/gedankenstuecke/ftdna-upload/blob/master/CONTRIBUTING.md) to see how you can help and become part of our team! 🎉 Also have [a look at our `ROADMAP.md`](https://github.com/gedankenstuecke/ftdna-upload/blob/master/ROADMAP.md) to see what we want to work on in the future.
