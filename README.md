# AWS EC2 Ansible Dynamic Inventory Generator

**TL;DR:** Quickly generate an Ansible inventory file (`ec2.ini`) that lists your Amazon EC2 instances, filtered and grouped by their tags.

This Python script generates a dynamic inventory for Ansible from your Amazon EC2 instances. It uses instance tags to filter and group instances for easier management in Ansible playbooks.

## Features

- **Tag-based filtering:** Easily customize which EC2 instances are included in the inventory by specifying tag key-value pairs.
- **Group by tag:**  Group your instances based on a specific tag key, making it simple to target groups of instances in your playbooks.
- **Customizable tags:**  Specify the tag keys used for instance names (`NameTag`) and grouping (`GroupTag`).
- **Output to INI file:** Creates a standard Ansible INI inventory file (`ec2.ini`) for direct use.

## Requirements

- **Python 3.x**
- **Boto3** (AWS SDK for Python): Install using `pip install boto3`
- **AWS Credentials:** Ensure your AWS credentials are configured correctly (e.g., in `~/.aws/credentials`)

## Usage

1. **Configure Tag Variables:**  Edit the `NameTag`, `GroupTag`, `NameTagFilter` and `GroupTagFilter` variables at the top of the script to match the tag keys you use in your AWS environment.

1. **Run the Script:** Execute the script from your terminal:

```Bash
python generate_inventory.py 
```
This will create the ec2.ini file in the same directory.

### Example ec2.ini Output
```
# Generated Ansible inventory

[prod]
webserver-01 ansible_host=54.12.34.56
webserver-02 ansible_host=54.87.65.43
```
