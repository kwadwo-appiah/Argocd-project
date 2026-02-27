terraform {
    backend "s3" {
    bucket         = "redis-eks-terraform-state-prod"
    key            = "dev/eks/terraform.tfstate"
    region         = "us-west-2"
    use_lockfile = true
    encrypt        = true
  }
}
