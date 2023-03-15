# Cloud Computing with Amazon Web Services - Setup Instructions

These instructions walk you through creating an AWS EC2 instance (Elastic Compute) and S3 instance (Storage), install Anaconda Python, run a remote Jupyter notebook, and perform analysis in the AWS environment.

The instructions are very light on explanation. More context will be provided during class. The instructions are presented twice, once without screenshots, and once with screenshots. Many of the instructions (click "Blah Blah" link) are fairly straightforward, and can be followed without screenshots, so a quick run-through is provided first. If you have trouble following them, scroll down for a presentation with screenshots. Even if you use the screenshot version the first time, the no-screenshot version will be useful as quick guide after you have run through it once.

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
5. The PEM file will automatically download! Find it (may be in Downloads folder, depending on your browser settings) and move it to a place you will be able to remember. You could use your folder for this course, or create an `aws` folder in your home directory.
6. In the left-hand menu click Instances→Instances.
7. Click Launch Instances.
8. You will be taken to the "Launch an instance" page. Confirm or change the following settings. (Ignore sections not mentioned here.)
    * **Name:** This is the name that will appear in your list of instances, so name it something you will recognize. Naming it after a project or instance specification is common. You could name it "Big Geospatial Data" for this course, or "Ubuntu 22.02" for the operating system we will use, or anything else you would like.
    * **Application and OS Images:** Click Ubuntu and choose "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type" or the latest free tier eligible version.
    * **Instance Type** should default to t2.micro or another free tier eligible instance type.
    * **Key pair (login):** Select the name of key pair that you just created from the dropdown list.
    * **Configure storage:** Increase the storage size to 15 GB. We *may* need additional storage because the Anacoda Python environment will take up at least 4GB on its own. This is half of the 30GB of free tier storage for EBS containers. We will access additional free storage in S3 for our actual analysis data.

The instance should launch immediately and you should be taken to the list of instances. The instance should show its state as Running.

### Connect to an EC2 Instance, Install Python, and Transfer Files

### Create an S2 Instance


## AWS Instructions with Screenshots


