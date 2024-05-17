import boto3

# Customizable tag variables
NameTag = 'Name'        # Tag key for the instance name (change if needed)
GroupTag = 'Environment' # Tag key for grouping instances (change if needed)
NameTagFilter = '*apache*'  # Filter pattern for instance names (supports wildcards)
GroupTagFilter = 'stage*'    # Filter pattern for groups (supports wildcards)

def generate_ansible_inventory():
    """
    Generates a dynamic Ansible inventory from AWS EC2 instances based on tag filters.

    Returns:
        list: A list of dictionaries representing each EC2 instance with relevant details.
    """
    ec2_client = boto3.client('ec2')

    instance_tags = {NameTag: NameTagFilter, GroupTag: GroupTagFilter}
    filters = [{'Name': 'instance-state-name', 'Values': ['running']}]
    for tag_key, tag_value in instance_tags.items():
        filters.append({'Name': f'tag:{tag_key}', 'Values': [tag_value]})

    inst_resp = ec2_client.describe_instances(Filters=filters)

    inventory = []
    for reservation in inst_resp['Reservations']:
        for instance in reservation['Instances']:
            public_ip = instance.get('PublicIpAddress', 'N/A')
            name = ''
            group = ''

            for tag in instance.get('Tags', []):
                if tag['Key'] == NameTag:
                    name = tag['Value']
                if tag['Key'] == GroupTag:
                    group = tag['Value']

            inventory.append({'Name': name, 'public_ip': public_ip, GroupTag: group})

    return inventory

def write_inventory_to_file(inventory, filename='ec2.ini'):
    """
    Writes the generated inventory to an INI file.

    Args:
        inventory: The list of EC2 instances from generate_ansible_inventory.
        filename: The name of the output file (default: ec2.ini).
    """
    with open(filename, 'w') as inventory_file:
        inventory_file.write("# Generated Ansible inventory\n\n")

        grouped_hosts = {}
        for host in inventory:
            group_name = host.get(GroupTag, 'default')  
            if group_name not in grouped_hosts:
                grouped_hosts[group_name] = []
            grouped_hosts[group_name].append(host)

        for group, hosts in grouped_hosts.items():
            inventory_file.write(f"[{group}]\n")
            for host in hosts:
                inventory_file.write(f"{host['Name']} ansible_host={host['public_ip']}\n")
            inventory_file.write("\n")

if __name__ == '__main__':
    inventory = generate_ansible_inventory()
    write_inventory_to_file(inventory)
    print("Done.")
