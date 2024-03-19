# bitstore-app

Terraform config for bitstore-app

[Terraform Docs](https://terraform-docs.io/) created by running:

```sh
docker run --rm \
    --volume "$(pwd):/terraform-docs" \
    -u $(id -u) \
    -w /terraform-docs \
    quay.io/terraform-docs/terraform-docs:latest --output-file /terraform-docs/README.md --output-mode inject /terraform-docs/terraform
```

Remember update the dependency lock file for different architectures:

```sh
terraform providers lock \
    -platform=linux_amd64 \
    -platform=darwin_amd64 \
    -platform=darwin_arm64 \
    -platform=windows_amd64
```
