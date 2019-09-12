# Plot Extractor Template
<img src="https://github.com/az-digitalag/Drone-Processing-Pipeline/raw/07b1edc34a1faea501c80f583beb07f9d6b290bb/resources/drone-pipeline.png" width="100" />

This code is intended to be used as a template for writing additional plot-level, RGB-based, phenomic extractors for the Drone Processing Pipeline.

Knowledge of the Python language and Docker images are necessary when using this template.

## Quick Start
1. Clone this repository into your own project
2. Edit the *configuration.py* file
3. Run do_config.py
4. Edit the *extractor.py* file and replace the contents of the compute() function with your algorithm
5. Test you algorithm by running *tester.py* specifying some [plot image files](https://drive.google.com/file/d/1xWRU0YgK3Y9aUy5TdRxj14gmjLlozGxo/view?usp=sharing)
6. Build the docker image for your extractor and make it available

## Overview

This templated code has been developed as an effort to make writing new extractors, and keeping them up to date, easier.
By isolating the algorithm code from the rest of the infrastructure needed by an extractor we've been able to reduce the lead time for producing a working extractor.

In this document we will be referring to a fictional extractor name of 'ruby'.
This name is used for illustrative purposes only and you should use your own extractor name.

The following steps are needed when using this template. Note that all the sections referenced can be found below.

1. Make a copy of this repository as outlined in the [Getting Started](#starting) section
2. Fill in the configuration.py file and create the needed files as described in the [Configuration](#configuration) section
3. Fill in the calculate() function as outlined in the [Adding Your Algorithm](#algorithm) section 
4. Test your algorithm as outlined in the [Testing your Algorithm](#testing) section
5. Create your Docker image and make it available as outined in the [Making a Docker Image](#docker) section

**Updating**
If you are updating your code from this repository, you must make sure you have secured a copy of your recent files.
Merging with or pulling from the template GitHub repository will change files and may cause loss of code - unless you have a backup.
The easiest approach is to make a local copy of `extractor.py`, `configuration.py`, and `Dockerfile`, update the source, then copy those files back.
If there's a breaking change (meaning one of the just listed files needs to be modified), you can use your local copy to more easily manage a merge when necessary.

## Getting Started <a name="starting"/>

Before you start, make sure to have your own respoitory in which you can make your changes.

At this point you will want to clone the template code.
Another option is to download a .zip of the repository and unzip it into your project; we will not be covering this approach.
If you are using [GitHub](https://github.com) you can clone the [repository](https://github.com/az-digitalag/Drone-Processing-Pipeline.git) as a [template](https://help.github.com/en/articles/creating-a-repository-from-a-template).

**Clone**: \
The advantage to cloning is that you have a stable copy of the code to change as you want.
The disadvantage of cloning is that when the template gets updated you will need to manually merge any changes.

To clone the template, open a command window and change to the location of your repository on disk (for example, `cd ~/my-repo`).
Next use git to clone the template project by running `git clone https://github.com/az-digitalag/dpp-extractor-plot.git extractor-ruby`.

At this time you may want to check your changes into source control.
Note that after running the [Generate Files](#generate) step we recommend deleting a file.
Depending upon your comfort level with the source control you use, you may want to wait until after that step to check files in.

## Configuration <a name="configuration"/>

There are two steps needed for configuration:
1. Update the file named "configuration.py" with your values
2. Run the "do_config.py" script - this requires Python to be installed

### Edit configuration.py <a name="configuration_py"/>

There are several fields that need to be filled in with values that are meaningful for your extractor.

**EXTRACTOR_NAME**

This is the name that your extractor will be known by.
The best choice is to pick a name that is descriptive of your algorithm, hasn't been used before in your environment, and isn't too long.
Sometimes your best name has been used already.
When this is the case, adding a short identifier can help.
For example, using your initials or adding a an adjective can help.

All alphanumeric characters are allowed, as are underscores.
The name you choose will be converted to lowercase in the code.
This means that "Ruby" is considered the same as "ruby" and "rUbY" 

**VERSION**

This is the reported version of your extractor.
It is important to increment this number every time you release an updated extractor.

There are two ways of updating the version number and it's up to you to determine which is best for your situation.
One way is to re-run the [do_config.py](#configuration) script as outlined below.
The other way is to edit the *extractor-info.json* file and update the version number there.

**DESCRIPTION**

A very short description of what your extractor does.

**AUTHOR_NAME**

This would be your name or the name of the principal contact.
The value entered here is used as part of the created docker image information as well as when the extractor is registered.

**AUTHOR_EMAIL**

This is the email address to use as a contact point.
It is used in conjunction with the AUTHOR_NAME field

**REPOSITORY**

Specify the full URL to your code repository.

**VARIABLE_NAMES** <a name="sub_variable_names"/>

The name of your variable or a comma-separated list of variable names.
These names are matched to the return value(s) of your algorithm.

### Generate files <a name="generate"/>

There are two principal files that are configuration based.
The `do_config.py` script generates these files for you based upon the values entered into the [configuration.py](#configuration_py) file.

The two files generated by the script:
* extractor_info.json: contains JSONLD information used to register the extractor
* Dockerfile: the commands to build a docker image of your extractor

To generate these files, first make sure your configuration.py file is up to date, then do the following:
1. Open a command shell and change to the folder containing the `do_config.py` script, or use a file browser to browse to the folder
2. Run the script by entering the following command in the command shell `./do_config.py`, or by running the file from the file browser (usually by double-clicking the name).

If you can't run the script, make sure you have Python installed.
Alternatively, with the command shell, you might need to specify the python version to run, as shown with the following command: `python3 ./do_config.py`.

If the script encounters a problem, an error is reported.
Correct the caause of the reported error and try running the command again.
If the problem is caused by the script itself you can enter an issue as well as ask on our Slack channel.

Once you are satisfied with the results you can delete the *\*.pyc* files.

This is another good point to save your files to source control.

## Adding Your Algorithm <a name="algorithm"/>

Your algorithm will reside in a separate file named `extractor.py`, in a function named `calculate`.
The *extractor.py* file copied from source control (as described in [Getting Started](#starting)) contains the outline of this function.
The *calculate* function receives a numpy array of RGB data representing a single plot.

You will need to modify *extractor.py* to import the modules you need and perform the actions for your algorithm.

The calling code expects a single value, list, tuple, or dictionary to be returned.
The returned value(s) can be a single string, a number value, or something.
It's important that the value returned has the accuracy needed.
For example, if only two decimal places are needed for a real number, it would be best to return a string that exactly represents the desired value.

When returning a list or tuple, the returned values are expected to be in the same order as the names defined in [VARIABLE_NAMES](#sub_variable_names) in the [Configuration](#configuration) section.

When returning a dict, the key names are matched to the names defined in [VARIABLE_NAMES](#sub_variable_names) in the [Configuration](#configuration) section.
The key names must exactly match the names defined in VARIABLE_NAMES.

When returning a list, tuple, or dict, the number of values returned must match the number of names defined in VARIABLE_NAMES.
It's considered an error when the number of values don't match the number of names.
On a technical note, a returned dict must contain at least the keys defined in VARIABLE_NAMES; it can contain additional key/value pairs without an error being raised.

Again, this is a good point to save your files to source control.

## Testing your Algorithm <a name="testing"/>

Some sample plot images are stored in the "sample_plot_images.zip" file on [Google Drive](https://drive.google.com/file/d/1xWRU0YgK3Y9aUy5TdRxj14gmjLlozGxo/view?usp=sharing).
Download the ZIP file and extract the image files to use them for testing.

We provide a script named "tester.py" to assist in testing your algorithm.
Running this script without any parameters will display information on how to use the script.

To test your algorithm against image files, run the tester.py script specifying command line parameters consisting of paths to images and paths to folders containing images.
It's possible to specify both images and folders on the command line.
The script will run and display lines of CSV consisting of the paths of image files as well as the output from your algorithm.
Error and other status information may be displayed as well.

For example, we are going to assume that there are images in a folder named sample_plot_images and that our algorithm returns the total number of pixels of the image.
Our command could be `./tester.py sample_plot_images`.
The following output would be produced:
```sample_plot_images/rgb_17_7_W.tif,7000
sample_plot_images/rgb_40_11_W.tif,7000
sample_plot_images/rgb_6_1_E.tif,7000
sample_plot_images/rgb_1_2_E.tif,7000
sample_plot_images/rgb_33_8_W.tif,7000
sample_plot_images/rgb_5_11_W.tif,7000
```

If you run into problems, the [Generate files](#generate) section above contains hints on running a python script.

If you have made changes based upon your testing, be sure to check them into source control.

## Making a Docker Image <a name="docker"/>

In the [Configuration](#configuration) section the `do_config.py` script generated a file named "Dockerfile".
This file has the basic configuration needed to build an extractor as a Docker image.

Before trying to build the Docker image, you should review the *Dockerfile* file for additional installation steps specific for your extractor.
If additional installation steps are needed, they can be added to the *Dockerfile* as needed.

Once the *Dockerfile* file is ready, run the `docker build` command to generate your image (that is not the complete command needed to build an image).
Refer to the Docker documentation and the `docker` application command line help for additional information on how to build an image.

Once your extractor is built, it's recommended that it's placed on [Docker Hub](https://hub.docker.com/) or on a similar repository.
