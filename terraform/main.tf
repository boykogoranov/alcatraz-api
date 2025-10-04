module "alcatraz" {
  source        = "./module"
  replicas      = var.replicas
  docker_image  = var.docker_image
}