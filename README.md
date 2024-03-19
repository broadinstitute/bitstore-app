# bitstore-app
BITStore AppEngine App

This app displays a web interface for users to view filesystem/share usage.

<!-- BEGIN_TF_DOCS -->
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

## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_google"></a> [google](#requirement\_google) | 4.84.0 |
| <a name="requirement_google-beta"></a> [google-beta](#requirement\_google-beta) | 4.84.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | 3.51.1 |
| <a name="provider_google-beta"></a> [google-beta](#provider\_google-beta) | 3.51.1 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [google-beta_google_cloudbuild_trigger.build-docker-image](https://registry.terraform.io/providers/hashicorp/google-beta/4.84.0/docs/resources/google_cloudbuild_trigger) | resource |
| [google-beta_google_cloudbuild_trigger.deploy-app-trigger](https://registry.terraform.io/providers/hashicorp/google-beta/4.84.0/docs/resources/google_cloudbuild_trigger) | resource |
| [google_project.project](https://registry.terraform.io/providers/hashicorp/google/4.84.0/docs/resources/project) | resource |
| [google_project_iam_member.cloudbuild](https://registry.terraform.io/providers/hashicorp/google/4.84.0/docs/resources/project_iam_member) | resource |
| [google_project_service.services](https://registry.terraform.io/providers/hashicorp/google/4.84.0/docs/resources/project_service) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_billing_account"></a> [billing\_account](#input\_billing\_account) | n/a | `any` | n/a | yes |
| <a name="input_branch"></a> [branch](#input\_branch) | n/a | `any` | n/a | yes |
| <a name="input_costobject"></a> [costobject](#input\_costobject) | n/a | `any` | n/a | yes |
| <a name="input_env"></a> [env](#input\_env) | n/a | `any` | n/a | yes |
| <a name="input_folder_id"></a> [folder\_id](#input\_folder\_id) | n/a | `any` | n/a | yes |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | n/a | `any` | n/a | yes |
| <a name="input_project_name"></a> [project\_name](#input\_project\_name) | n/a | `any` | n/a | yes |
| <a name="input_region"></a> [region](#input\_region) | n/a | `any` | n/a | yes |
| <a name="input_repo"></a> [repo](#input\_repo) | n/a | `any` | n/a | yes |
| <a name="input_credentials_file"></a> [credentials\_file](#input\_credentials\_file) | n/a | `string` | `"etc/service_account.json"` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
