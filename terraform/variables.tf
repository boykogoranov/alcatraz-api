variable "replicas" {
  description = "Number of replicas to deploy"
  type        = number
  default     = 1 
}

variable "docker_image" {
  description = "Docker image to deploy"
  type        = string
  default     = ""
}
