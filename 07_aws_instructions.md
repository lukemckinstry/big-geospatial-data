# Cloud Computing with Amazon Web Services - Setup Instructions

These instructions walk you through creating an AWS EC2 instance (Elastic Compute) and S3 instance (Storage), install Anaconda Python, run a remote Jupyter notebook, and perform analysis in the AWS environment.

The instructions are very light on explanation. More context will be provided during class. The instructions are presented twice, once without screenshots, and once with screenshots. Many of the instructions (e.g. "Click 'Blah Blah' link") are fairly straightforward, and can be followed without screenshots, so a quick run-through is provided first. If you have trouble following them, scroll down for a presentation with screenshots. Even if you use the screenshot version the first time, the no-screenshot version will be useful as quick guide after you have run through it once.

## AWS Instructions without Screenshots

### Create an AWS Account

Go to <https://aws.amazon.com/> and click Create an AWS Account.

You do have to provide a credit card, but Amazon comes with 12 months of service at a free tier (low-power machines, small storage containers, etc.). You can choose to pay for certain options, but for this course we will only choose options in the free tier.

I recommend using your Temple email address. If you don't keep your TUmail account active after graduation you will probably want to cancel your AWS account. As we are using AWS for learning purposes, retaining the EC2 instances is not all that importatant. If you go on to use AWS professionally, you can create a new account with an organizational or personal email address in the future.

You will have to verify your email. It will then take a couple of minutes (for me it was less than 2 minutes) for the account to be validated. When you get the validation email, login to AWS using your email and password.

### Create an EC2 Instance

1. In the AWS Console, click on EC2, which should show up on the welcome page as a popular service. If you don't see it, click the Services menu in the upper left, go to All Services, and find the EC2 link.
2. In the left-hand menu click on Network & Security→Key Pairs.
3. Click Create key pair.
4. Give your key pair a name that will be easy to type in a terminal. I recommend using lowercase letters and avoiding spaces. I chose `big-geospatial-data`. The key pair type can be left at RSA (default), but the file format should be changed to "`.pem` For use with OpenSSH". Do not add tags. Click Create key pair.
5. The PEM file will automatically download! Find it (may be in Downloads folder, depending on your browser settings) and move it to a place you will be able to remember. You could use your course folder (*NOT* the course repo), or create an `aws` folder in your home directory. This file can give someone access to your Amazon instance, so never store it in a code repository. You don't want to accidentally end up uploading it to GitHub.
6. Create appropriate permissions on the PEM file. (This is not necessary to create the instance, but will be necessary to connect to it later, so we might as well do it now.) In the terminal (Mac/Linx) or Windows PowerShell, `cd` to the folder with the PEM file.
    1. **On Mac:** Enter the following command in the terminal:
        ```sh
        chmod 400 big-geospatial-data.pem
        ````
    2. **On Windows:** Enter the following commands in PowerShell:
        ```sh
        icacls.exe big-geospatial-data.pem /reset
        icacls.exe big-geospatial-data.pem /grant:r "$($env:username):(r)"
        icacls.exe big-geospatial-data.pem /inheritance:r
        ```
7. In the left-hand menu click Instances→Instances.
8. Click Launch Instances.
9. You will be taken to the "Launch an instance" page. Confirm or change the following settings. (Ignore sections not mentioned here.)
    * **Name:** This is the name that will appear in your list of instances, so name it something you will recognize. Naming it after a project or instance specification is common. You could name it "Big Geospatial Data" for this course, or "Ubuntu 22.02" for the operating system we will use, or anything else you would like.
    * **Application and OS Images:** Click Ubuntu and choose "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type" or the latest free tier eligible version.
    * **Instance Type** should default to t2.micro or another free tier eligible instance type.
    * **Key pair (login):** Select the name of key pair that you just created from the dropdown list.
    * **Configure storage:** Increase the storage size to 15 GB. We *may* need additional storage because the Anacoda Python environment will take up at least 4GB on its own. This is half of the 30GB of free tier storage for EBS containers. We will access additional free storage in S3 for our actual analysis data.
    * **Advanced details:** In order to access data in an S3 container you need to use an IAM instance profile. If you have a profile with appropriate permissions, you can select it from the IAM instance profile dropdown list. If not, you can click Create new IAM profile to create one now. You can also skip this step and attach an IAM instance profile later. I recommend creating it now.
        1. Click Create new IAM profile. A new browser tab will open to the Roles page of the Identity and Access Management (IAM) Console.
        2. Click Create role.
        3. Choose AWS service as the trusted entity type and EC2 as the use case. Click Next.
        4. In Permissions policies search for "S3" and click "AmazonS3FullAccess" in the list of policy names. Click Next.
        5. Name the policy something easily recognizable like "full_S3_access_from_EC2". Complete the process by clicking Create role.
        6. Close the IAM browser tab. You should be back on the Launch an instance tab.
        7. Click the refresh arrow next to the IAM instance profile and select "full_S3_access_from_EC2".
10. Click Launch instance.

The instance should launch immediately, and you should be taken to the list of instances. The instance should show its state as Running.

### Create an S3 Bucket

1. On the AWS web page, go to Services→Storage→S3.
2. Click Create bucket in the upper right
3. Name your bucket. Bucket names can consist only of lowercase letters, numbers, dots (.), and hyphens (-). ***Bucket names must be globally unique across all AWS accounts.*** Unsurprisingly, the name `my-data` is already taken. I am going to use a combination of a personal name and a storage purpose. The bucket will be named `geospatial-lee`.

While we're at it, let's upload the data we will use for this lab exercise. The data is trip data from the New York City's CitiBike bike share program.

1. Go to <https://s3.amazonaws.com/tripdata/index.html> in your web browser.
2. Select a month of data that you are interested in and download it to your local computer. In order to not have the analysis take too long to run, I would recommend picking one of the smaller files. Look for one of the earlier years (2013-2015) and/or a Winter month. Unzip it locally.
3. In the list S3 buckets, click on your bucket (e.g. `geospatial-lee`). Click the Upload button.
4. Click Add files and navigate to the unzipped CSV of CitiBike trip data. (You can upload multiple files, or folders of files, at the same time.)
5. Click Upload. After the upload completes, click Close.
6. Your bucket should now show the file in the list of objects, including it's type (csv) and size.

#### What if you didn't attach the IAM role to your EC2 instance?

The instructions shown above for creating an EC2 instance also show you how to create and attach an IAM role that specifically allows an EC2 instance to access *all* S3 buckets created in the same AWS account. If you did not do this, you have to create the IAM role now and attach it to the instance.

1. Go to Services→Security→IAM (Identity and Access Management).
2. In the left-hand menu click Roles. Then click Create role.
3. Choose AWS service as the trusted entity type and EC2 as the use case. Click Next.
4. In Permissions policies search for "S3" and click "AmazonS3FullAccess" in the list of policy names. Click Next.
5. Name the policy something easily recognizable like "full_S3_access_from_EC2". Complete the process by clicking Create role.
6. Go to Services→EC2 and select Instances in the left-hand menu.
7. Check the instance that you want to modify and choose Actions→Security→Modify IAM role. ***You can modify the IAM role on a currently running instance.***
8. Choose "full_S3_access_from_EC2" in the IAM role dropdown and click Update IAM role.

### Connect to an EC2 Instance

Install Python, and Transfer Files

Now that the EC2 instance has been created, we are going to connect to it and run some remote commands.

1. Select (check) the instance in the list, then in the upper right click the Connect button. This does not connect you immediately, but takes you to an instruction page.
2. On the "Connect to instance" page, click the SSH client tab. This will show you the public DNS associated with your instance. ***A new public DNS is generated every time your restart an instance, so do not bother saving this anywhere!***
3. Copy the example ssh call. In my case it looked like this:
    ```sh
    ssh -i "big-geospatial-data.pem" ubuntu@ec2-3-142-69-67.us-east-2.compute.amazonaws.com
    ```
4. Paste this command into your terminal. Note that this assumes your terminal is still open and the working directory is the one with the PEM file. If you have changed directories or restarted the terminal, you will have to navigate back to the PEM file or provide a full path.

You should get a welcome message (e.g. "Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.0-1028-aws x86_64)") and the prompt should change to reflect the username (`ubuntu`) and host (the instance's private IP address, which is different from the public IP address we used to connect to it). In my case it looks like this:

```sh
ubuntu@ip-172-31-42-59:~$ 
```

In class, I will demo some basic Linux commands including filesystem navigation.

**Do not do this yet:** Keeping an EC2 instance running costs money. In our case, we are using a free tier, but we don't want to get in the habit of leaving EC2 instances running when we aren't using them. When you are done doing analysis in your EC2 instance you should log off and stop the instance.

1. Log off by typing `exit` at the remote prompt. Your should see at "Connection closed" message, and the prompt should revert to your local system prompt (e.g. `C:\>` on Windows).
2. In your web browser go to the Instance state button on the upper right and choose "Stop instance". Note that stopping the instance will keep it in your instance list and you can start it again in the future. If you "Terminate instance", it will be destroyed. You will have to connect to a different instance in the future.

But leave the instance running for now so that we can continue to use it.

### Install Python

We want to run Python in EC2. Before we can do that, we have to install it, and before we install it we have to download it.

We will download and install Miniconda Python. The instructions below use a link which should automatically install the latest version of Python for Linux (Python 3.10 as of March 2023). If this link does not work, go to <https://docs.conda.io/en/latest/miniconda.html> in your web browser and copy the link for the latest version of Miniconda3 Linux 64-bit.

At the remote prompt, enter the following command. The first command downloads the installer, the second command runs the installer, and the third command modifies the remote prompt so that it displays the current conda environment at the beginning of the command line.

```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
```

Now that Python installed, we will use `conda` to create a Python environment.

```sh
conda create -n geospatial python=3.8 geopandas rasterio descartes jupyter matplotlib sqlalchemy psycopg2 boto3 smart_open
```

This command will take several minutes to run. After it has completed, you can activate the new environment with:

```sh
conda activate geospatial
```

After confirming that Anaconda Python is installed (if the above `conda` commands run, you installed it successfully), you should delete the installer, as the EC2 instance does not have very much storage space:

```sh
rm Miniconda3-latest-Linux-x86_64.sh
```

If the deletion doesn't work, make sure you haven't changed directories.

Now that you have installed Python, you can confirm that you can connect to the S3 bucket (created previously) within Python. At the console, type `python`. Issue the following commands. (You will have to enter the lines one by one. If you paste it into the Python console, the indentation won't be preserved.)

```python
import boto3
s3 = bot3.resource("s3")
for bucket in s3.buckets.all():
    print(bucket.name)

```

You will have to hit Enter twice after the last line to complete the for-loop. If you have followed these instructions you should see the name of one bucket, the one you created in the last section (in my case, `geospatial-lee`). If you have created additional buckets, they will display here as well.

Use `exit()` to exit the Python console.

### Connect to a Jupyter Notebook Running on EC2

We are already familiar with running Jupyter notebooks on our local machine. Now we are going to run an Jupyter server on our EC2 instance and connect to it from a web browser on our local machine. In order to do this we will use SSH **local port forwarding** to open our web browser and redirect an HTTP request on local port 8888 to the Jupyter server running on EC2.

1. In your EC2 prompt, start the Jupyter server with the following command:
    ```sh
    jupyter notebook --no-browser
    ```
2. At the bottom should be a message like the following. Copy *only* the **token**, which is the alphanumeric string that appears after `token=` in the URL.
    ```sh
    To access the notebook, open this file in a browser:
        file:///home/ubuntu/.local/share/jupyter/runtime/nbserver-2459-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=92d0f7fb2975c9ada65ca4eae9aa24a509050600fc982542
     or http://127.0.0.1:8888/?token=92d0f7fb2975c9ada65ca4eae9aa24a509050600fc982542
    ```
3. Open a new terminal or PowerShell prompt *on your local machine*.
4. Navigate to the folder with your PEM file. Issue the appropriate SSH command to connect to your EC2 instance. This command is the same as the previous SSH command that you used to connect to EC2 *except* that it includes the `-L` switch to establish local port forwarding. *Remember that the PEM filename has to match **your** PEM file and the DNS has to match the DNS of **your** EC2 instance.*
    ```sh
    ssh -i "big-geospatial-data.pem" -L 8157:localhost:8888 ubuntu@ec2-3-142-69-67.us-east-2.compute.amazonaws.com
    ```
5. In your web browser, go to <http://localhost:8157>.
6. In the login page, paste the token that you copied when you launched the remote Jupyter server. Hit log in.
7. You should now be at the familiar Jupyter web page. You can create a new notebook to test it, or move on to the next step, where we will upload an existing IPython notebook.

Note that when we run Jupyter notebook locally, the web page opens to <http://localhost:8888>. We are using port forwarding to direct an unused port (8157) to our EC2 instance. What this means is that you could *also* run Jupyter locally and connect to it on the usual port, 8888. This can be useful if you ever want to run an analysis on EC2 while you are also doing work on your local computer.

### Transfer Files to and from EC2

There are a number of ways to transfer files between your local machine and your EC2 instance. Those who prefer command line tools will use `scp` (secure copy). If you have to upload and download multiple files, providing the PEM file and DSN name every time will rapidly grow tedious. I prefer using GUI tools for this as you can set up the connection once and use it until you stop the instance.

I prefer [FileZilla](https://filezilla-project.org/index.php), an open source, cross-platfrom (S)FTP tool. However, I am going to demo WinSCP because it is already available on the PSM laptops. It is Windows-only, so if you are using Mac, try FileZilla instead.

1. Launch WinSCP from the Windows Start Menu. WinSCP should immediately open to a Login dialog. As you have no saved sites, you will have to configure a New Site.
2. The **file protocol** should be set to SFTP (probably the default).
3. The **host name** is the public DNS of your EC2 instance. This should begin with `ec2` and should *not* include the username, e.g. `ec2-3-142-69-67.us-east-2.compute.amazonaws.com`.
4. The **username** is `ubuntu`.
5. Click Advanced and go to SSH→Authentication.
6. Under **private key file**, use the file chooser to find your PEM file. You will have to change the file types to display All Private Key Files (it will default to showing only PPK files). When you select it, you will be asked if you want to convert the OpenSSH private key to PuTTY format. Hit OK. Then hit Save.
7. Hit OK in the Advanced Site Settings dialog.
8. Hit Save to save the site settings. Give your site an easily readable name. I used "AWS EC2 big-geospatial-data". Hit OK.
9. Hit Login. Confirm connecting to the server. You should now see a two-pane display of your local file system (left) and your remote filesystem (right).
10. In your local filesystem (left pane), find the file "07-2_citibike_analysis_aws_ec2_s3.ipynb". Drag it from the left pane to the right pane. The file will be uploaded to EC2.
11. Switch back to the Jupyter notebook tab in your web browser. The notebook list should show the newly uploaded file. If it does not, hit the Refresh notebook list button (circular arrows) in the upper right.

If you restart the instance, the public DNS will change. You can edit the site settings to add the new public DNS while keeping all of the other settings.

## AWS Instructions with Screenshots




