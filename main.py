import boto3
import configparser
import os


def get_aws_profiles():
    try:
        path = os.path.join(os.path.expanduser("~"), ".aws/config")
        parser = configparser.RawConfigParser()
        parser.read(path)

        profile_list = list()
        for profile in parser.sections():
            if "profile" in profile:
                profile_list.append(profile.replace("profile ", ""))

        return profile_list
    except:
        raise Exception(f"Error getting list of profiles from {path}")


def get_cidr_blocks():
    try:
        c_blocks = list()
        aws_regions = ["eu-west-1", "eu-west-2"]

        for aws_profile in get_aws_profiles():
            for region in aws_regions:
                sesssion = boto3.Session(profile_name=aws_profile, region_name=region)
                ec2_client = sesssion.client("ec2")

                r = ec2_client.describe_vpcs()
                for vpc in r["Vpcs"]:
                    for network in vpc["CidrBlockAssociationSet"]:
                        c_blocks.append(network["CidrBlock"])
        return c_blocks
    except:
        raise Exception("Error getting list of cidr blocks from aws")


def create_range():
    try:
        cidr_notation = 16
        starting_range = "10.0.0.0"
        upper_limit = 255
        starting_range_split = starting_range.split(".")
        r_count = 0
        range_used = True
        while range_used == True or r_count == 255:

            new_range = f"{starting_range_split[0]}.{r_count}.{starting_range_split[2]}.{starting_range_split[3]}/{cidr_notation}"

            if new_range in cidr_blocks:
                r_count += 1
            elif r_count > upper_limit:
                range_used = False
                raise Exception(
                    "I hoped this wouldn't ever happen, but we've reached the limits of this design"
                )
            else:
                range_used = False
                return new_range
    except:
        raise Exception("Error generating a new range")


if __name__ == "__main__":
    cidr_blocks = get_cidr_blocks()

    new_range = create_range()
    print(new_range)
