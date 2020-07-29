

A very simple scripts to suggest a cidr blocks.

Written to solve a minor problem of engineers deploying AWS VPCs with duplicate cidr blocks, and then VPC peering is required.

The cidr blocks are 10.{x}.0.0/16. Where x is incremented until an unused cidr bock is found or 10.255.0.0/16 is hit. This may cause a problem in the future, but I think we'll have bigger problems if we've got 255 VPCs.

# Running the script

```
pip install -r requirements.txt
```

```
python aws.py
```

## sample output

```
cidr_suggester git:(master) ✗ python main.py
10.55.0.0/16
```